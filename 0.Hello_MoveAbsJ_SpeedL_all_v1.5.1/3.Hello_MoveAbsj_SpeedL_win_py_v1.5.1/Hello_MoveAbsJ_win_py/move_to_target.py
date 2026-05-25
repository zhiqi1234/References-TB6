"""
TB6 机械臂 - 关节角度目标运动
J1=35° J2=0° J3=0° J4=-90° J5=90° J6=0°
安全特性：回车急停、运动结束自动 Stop+Disable
"""
import rpc
import random
import time
import threading

# 目标关节角度（度）
TARGET_ANGLES = {
    "J1": 35,
    "J2": 0,
    "J3": 0,
    "J4": -90,
    "J5": 90,
    "J6": 0,
}

IP = "192.168.50.1"
PORT = 5868
SETRATE = 15  # 全局速度百分比（10-30，越小越安全）

# TB6 关节限位（弧度）
JOINT_LIMITS = [
    (-3.1416, 3.1416),   # J1
    (-3.1416, 3.1416),   # J2
    (-2.8623, 2.8623),   # J3
    (-3.1416, 3.1416),   # J4
    (-3.1416, 3.1416),   # J5
    (-3.1416, 3.1416),   # J6
]

_stop_event = threading.Event()


def check_joint_limits(joints_deg):
    """检查关节角度是否在限位内（输入为度）。返回违规列表。"""
    import math
    violations = []
    for i, (j_deg, (lo, hi)) in enumerate(zip(joints_deg, JOINT_LIMITS)):
        j_rad = math.radians(j_deg)
        if j_rad < lo - 0.01 or j_rad > hi + 0.01:
            violations.append(
                f"J{i+1}={j_deg}° ({j_rad:.3f} rad), limit=[{lo:.3f}, {hi:.3f}] rad")
    return violations


def estop_listener(client):
    """回车键 → 急停（Stop + Disable）"""
    input()
    _stop_event.set()
    print("\n>>> 急停触发！")
    try:
        for cmd in ["{Stop}", "{Disable}"]:
            msg = rpc.Msg(cmd)
            msg.setMsgID(10001)
            msg.setMsgSeqID(random.randint(1, 10000))
            client.CallAwait(msg, 3000)
        print(">>> 机械臂已停止并下电")
    except Exception as ex:
        print(f">>> 急停发送异常: {ex}")
        print(">>> 请使用物理急停按钮！")


def send_cmd(client, cmd_str, timeout_ms=500):
    """发送单条 RPC 指令。返回 (status, resp_list)。"""
    if _stop_event.is_set():
        return -1, []
    msg = rpc.Msg(cmd_str)
    msg.setMsgID(10001)
    msg.setMsgSeqID(random.randint(1, 10000))
    status, resp_list = client.CallAwait(msg, timeout_ms)
    if status == 0:
        for r in resp_list:
            if r.code != 0:
                print(f"  [ERR({r.code})] {r.message}")
    else:
        print(f"  [FAIL] status={status}")
    return status, resp_list


def send_cmds(client, cmd_list, timeout_ms=500, sleep_s=0.1):
    """顺序发送多条 RPC 指令。"""
    for cmd in cmd_list:
        if _stop_event.is_set():
            return False
        status, _ = send_cmd(client, cmd, timeout_ms)
        if status != 0:
            print(f"  [WARN] 重试 ClearErr...")
            send_cmd(client, "{Clear}", 500)
        time.sleep(sleep_s)
    return True


def e_stop(client):
    """Stop + Disable 机械臂。"""
    print(">>> 执行 Stop + Disable ...")
    for cmd in ["{Stop}", "{Disable}"]:
        msg = rpc.Msg(cmd)
        msg.setMsgID(10001)
        msg.setMsgSeqID(random.randint(1, 10000))
        client.CallAwait(msg, 3000)
    print(">>> 机械臂已停止并下电")


def main():
    target_joints = [
        TARGET_ANGLES["J1"],
        TARGET_ANGLES["J2"],
        TARGET_ANGLES["J3"],
        TARGET_ANGLES["J4"],
        TARGET_ANGLES["J5"],
        TARGET_ANGLES["J6"],
    ]

    print("=" * 50)
    print("TB6 机械臂 - 目标关节角度运动")
    print(f"J1={TARGET_ANGLES['J1']}° J2={TARGET_ANGLES['J2']}° "
          f"J3={TARGET_ANGLES['J3']}°")
    print(f"J4={TARGET_ANGLES['J4']}° J5={TARGET_ANGLES['J5']}° "
          f"J6={TARGET_ANGLES['J6']}°")
    print(f"SetRate={SETRATE}")
    print("随时按回车急停")
    print("=" * 50)

    # 关节限位检查
    violations = check_joint_limits(target_joints)
    if violations:
        print("\n!!! 关节限位违规 !!!")
        for v in violations:
            print(f"    {v}")
        print("请修正目标角度后重试。")
        return

    # 连接机械臂
    print(f"\nConnecting to {IP}:{PORT}...")
    client = rpc.CPPClient(IP, PORT)
    print("Connected!")

    # 启动急停监听线程
    listener = threading.Thread(target=estop_listener, args=(client,), daemon=True)
    listener.start()

    try:
        # ================================================================
        # STEP 1: 初始化
        # ================================================================
        print("\n>>> STEP 1: 初始化 TB6 ...")
        init_cmds = [
            "{Clear}",
            "{Disable}",
            "{Mode}",
            "{SetMaxToq}",
            "{Recover}",
            f"{{SetRate {SETRATE}}}",
            "{Enable}",
            "{Var --clear}",
            "{Recover}",
            "{Start}",
        ]
        if not send_cmds(client, init_cmds, 500, 0.1):
            e_stop(client)
            return
        print("[TB6] 初始化完成，已上使能。")

        if _stop_event.is_set():
            e_stop(client)
            return

        # ================================================================
        # STEP 2: 定义目标关节变量
        # ================================================================
        print("\n>>> STEP 2: 定义目标关节变量 ...")
        joint_value = "{%d,%d,%d,%d,%d,%d,0,0,0,0}" % tuple(target_joints)
        var_cmd = "{Var --type=jointtarget --name=j_target --value=%s --degree_unit=1}" % joint_value
        status, _ = send_cmd(client, var_cmd, 500)
        if status != 0:
            print("[ERROR] 关节变量定义失败！")
            e_stop(client)
            return

        if _stop_event.is_set():
            e_stop(client)
            return

        # ================================================================
        # STEP 3: 运动到目标点
        # ================================================================
        print("\n>>> STEP 3: 运动到目标关节角度 ...")
        print("    确保工作空间无障碍！")
        status, _ = send_cmd(client, "{MoveAbsJ --jointtarget_var=j_target}", 60000)
        if status != 0:
            print("[ERROR] MoveAbsJ 运动失败！")
            e_stop(client)
            return
        print("[TB6] 已到达目标位置。")

    except KeyboardInterrupt:
        print("\n用户中断。")
    except Exception as ex:
        print(f"\nERROR: {ex}")
        import traceback
        traceback.print_exc()
    finally:
        # ================================================================
        # 无论正常/异常/急停，始终执行 Stop + Disable
        # ================================================================
        _stop_event.set()
        try:
            e_stop(client)
        except Exception:
            pass
        print("\n" + "=" * 50)
        print("运动结束。机械臂已 Stop + Disable（安全状态）。")
        print("=" * 50)


if __name__ == "__main__":
    main()

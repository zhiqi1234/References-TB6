import rpc
import random
import time

# 目标关节角度（度）
TARGET_ANGLES = {
    "J1": 35,
    "J2": 0,
    "J3": 0,
    "J4": 90,
    "J5": 90,
    "J6": 0,
}

IP = "192.168.50.1"
PORT = 5868


def send_rpcsy(client, cmd_list, timeout_ms, sleep_time_s):
    for cmd in cmd_list:
        msg = rpc.Msg(cmd)
        msg.setMsgID(10001)
        msg.setMsgSeqID(random.randint(1, 10000))
        status, resp_list = client.CallAwait(msg, timeout_ms)

        if status == 0:
            for r in resp_list:
                code = "OK" if r.code == 0 else f"ERR({r.code})"
                print(f"  [{code}] {r.message}")
        else:
            print(f"  [FAIL] status={status}")
            client.ClearErr()

        time.sleep(sleep_time_s)


def main():
    print("=" * 50)
    print("TB6 机械臂 - 目标关节角度运动")
    print(f"J1={TARGET_ANGLES['J1']}° J2={TARGET_ANGLES['J2']}° J3={TARGET_ANGLES['J3']}° "
          f"J4={TARGET_ANGLES['J4']}° J5={TARGET_ANGLES['J5']}° J6={TARGET_ANGLES['J6']}°")
    print("=" * 50)

    # 连接机械臂
    print("Connecting...")
    client = rpc.CPPClient(IP, PORT)
    print("Connected!")

    # 构建关节目标值 {J1, J2, J3, J4, J5, J6, J7, J8, J9, J10}
    joint_value = "{%d,%d,%d,%d,%d,%d,0,0,0,0}" % (
        TARGET_ANGLES["J1"],
        TARGET_ANGLES["J2"],
        TARGET_ANGLES["J3"],
        TARGET_ANGLES["J4"],
        TARGET_ANGLES["J5"],
        TARGET_ANGLES["J6"],
    )

    # 初始化指令列表
    init_cmds = [
        "{Clear}",
        "{Disable}",
        "{Mode}",
        "{SetMaxToq}",
        "{Recover}",
        "{SetRate}",
        "{Enable}",
        "{Var --clear}",
        "{Recover}",
        "{Var --type=jointtarget --name=j0 --value=%s --degree_unit=1}" % joint_value,
    ]

    # 初始化
    print(">>> 初始化中...")
    send_rpcsy(client, init_cmds, 500, 0.1)

    # 运动到目标点
    print(">>> 运动到目标关节角度...")
    send_rpcsy(client, ["{MoveAbsJ --jointtarget_var=j0}"], 50000, 0.01)

    print(">>> 运动完成！")
    print(">>> 按 Ctrl+C 退出")

    # 保持连接
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n>>> 退出")
        send_rpcsy(client, ["{Stop}", "{Disable}"], 3000, 0.1)


if __name__ == "__main__":
    main()

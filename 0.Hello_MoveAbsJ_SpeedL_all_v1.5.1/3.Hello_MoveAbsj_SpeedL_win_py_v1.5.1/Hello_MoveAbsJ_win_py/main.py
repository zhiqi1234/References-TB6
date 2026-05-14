import rpc
import random
import time
import threading

# 急停事件
stop_event = threading.Event(
)

# 初始化命令列表
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
    "{Var --type=jointtarget --name=j0 --value={0,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j1 --value={0.1,-1.5,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j2 --value={0.2,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j3 --value={-0.1,0,0,0,0,0,0,0,0,0}}",
    "{Var --type=jointtarget --name=j4 --value={-0.2,0,0,0,0,0,0,0,0,0}}",
]

# 动作序列：定义点位 + 停留时间(秒)
action_sequence = [
    ("j1", 1.0),
    ("j2", 1.0),
    ("j3", 1.0),
    ("j4", 1.0),
    ("j0", 0.0),  # 最后回到零点
]

# 急停指令
estop_cmds = [
    "{Stop}",
    "{Disable}",
]


def wait_for_enter():
    """按回车触发急停"""
    input()
    stop_event.set()
    print("\n>>> 急停触发！")


def e_stop(client):
    """执行急停"""
    print(">>> 发送 Stop + Disable ...")
    for cmd in estop_cmds:
        msg = rpc.Msg(cmd)
        msg.setMsgID(10001)
        msg.setMsgSeqID(random.randint(1, 10000))
        client.CallAwait(msg, 3000)
    print(">>> 机械臂已停止并下电")


def main():
    # 启动急停监听线程
    listener = threading.Thread(target=wait_for_enter, daemon=True)
    listener.start()

    print("Connecting...")
    client = rpc.CPPClient("192.168.50.1", 5868)
    print("Connected!")

    # 初始化
    print(">>> 初始化中...")
    send_rpcsy(client, init_cmds, 500, 0.1)

    # 先回零点
    if stop_event.is_set():
        e_stop(client)
        return
    print(">>> 回零点 (j0)")
    send_rpcsy(client, ["{MoveAbsJ --jointtarget_var=j0}"], 50000, 0.01)

    # 执行动作序列
    for target, stay in action_sequence:
        if stop_event.is_set():
            e_stop(client)
            return

        print(f">>> 移动到 {target}，停留 {stay}s")
        cmd = f"{{MoveAbsJ --jointtarget_var={target}}}"
        send_rpcsy(client, [cmd], 50000, 0.01)

        if stay > 0 and not stop_event.is_set():
            time.sleep(stay)

    print(">>> 动作序列完成！按 Ctrl+C 退出")
    print(">>> (随时按回车可以急停)")

    # 保持连接，等待退出
    try:
        while True:
            if stop_event.is_set():
                e_stop(client)
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        e_stop(client)


def send_rpcsy(client, cmd_list, timeout_ms, sleep_time_s):
    for cmd in cmd_list:
        if stop_event.is_set():
            return

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


if __name__ == "__main__":
    print("=" * 50)
    print("TB6 机械臂动作演示")
    print("随时按回车急停")
    print("=" * 50)
    main()

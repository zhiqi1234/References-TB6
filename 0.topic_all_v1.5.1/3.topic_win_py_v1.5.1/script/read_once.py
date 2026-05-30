import time
import sys
import topic
import message
import threading

done = threading.Event()
result = {"robottarget": None, "jointtarget": None}

def on_rtstate(tt: topic.SystemRtState):
    parm_rt = message.SystemStateData()
    message.display_rt(tt, parm_rt)
    if parm_rt.models_current_points:
        cp = parm_rt.models_current_points[0]
        result["robottarget"] = list(cp.robottarget)
        result["jointtarget"] = list(cp.jointtarget)
    # 计算关节位置
    if parm_rt.models and parm_rt.models_joints:
        joints_per_model = len(parm_rt.models_joints) // len(parm_rt.models)
        positions = []
        for j_idx in range(joints_per_model):
            positions.append(parm_rt.models_joints[j_idx].position)
        result["joint_positions"] = positions

    print("\n" + "=" * 60)
    print("Robot Target (x,y,z,qx,qy,qz,qw):")
    print(f"  {result['robottarget']}")
    print(f"\nJoint Target:")
    print(f"  {result['jointtarget']}")
    print(f"\nJoint Positions (rad):")
    print(f"  {result.get('joint_positions', 'N/A')}")

    # 格式化为可直接用的 Var 命令
    rt = result["robottarget"]
    if rt:
        print(f"\n>>> 可直接用的命令:")
        print(f'Var --name=mypos --type=robottarget --value={{{rt[0]:.4f},{rt[1]:.4f},{rt[2]:.4f},{rt[3]:.4f},{rt[4]:.4f},{rt[5]:.4f},{rt[6]:.4f}}}')
        print(f'MoveJ --robottarget_var=mypos --speed=v30')
    print("=" * 60)
    done.set()

system_topic_options = topic.NodeOptions()
system_topic_options.node_name = 'read_once'
system_topic_options.sub_url = 'tcp://192.168.50.1:19091'

print(f"Connecting to {system_topic_options.sub_url} ...")
system_topic_node = topic.Node(system_topic_options)
if not system_topic_node.Start():
    print("Failed to start node.")
    sys.exit(1)

print("Node started, waiting for data...")
sub = system_topic_node.CreateSubscriptionRT("system_rtstate", on_rtstate)

try:
    done.wait(timeout=5)
    if not done.is_set():
        print("Timeout: no data received within 5 seconds.")
except KeyboardInterrupt:
    pass
finally:
    system_topic_node.Shutdown()

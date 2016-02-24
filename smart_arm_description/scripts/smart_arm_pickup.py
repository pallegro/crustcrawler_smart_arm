#!/usr/bin/env python2
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

prev_secs = 0;  arm_state = 0
def JointState_cb(msg):
  global prev_secs, arm_state
  if msg.header.stamp.secs > prev_secs + 2:
    print(msg); prev_secs = msg.header.stamp.secs
    if   arm_state==0: arm_state=1;  return
    elif arm_state==1: arm_state=2;  shoulder(0.35);    elbow(-1.0);        return
    elif arm_state==2: arm_state=3;  left_finger(-0.1); right_finger(0.1);  return
    elif arm_state==3: arm_state=4;  shoulder(1.0); return
    else: rospy.signal_shutdown("Done :)")

if __name__=="__main__":
  pub = [rospy.Publisher('/smart_arm/%s_controller/command'%s, Float64, queue_size=2) \
         for s in 'shoulder_pan shoulder_pitch elbow_flex wrist_roll left_finger right_finger'.split()]
  base,shoulder,elbow,wrist,left_finger,right_finger = [p.publish for p in pub]
  rospy.init_node('smart_arm_pickup')
  rospy.Subscriber('/smart_arm/joint_states', JointState, JointState_cb)
  rospy.spin()

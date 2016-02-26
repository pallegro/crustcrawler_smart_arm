#!/usr/bin/env python2
import rospy, cv2, numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState, Image

t0=0;  ready=False;  at_block=False;  holding_block=False;  fwd=1.
def JointState_cb(msg):
  global t0, ready, at_block, holding_block, fwd
  t1 = msg.header.stamp.secs + msg.header.stamp.nsecs * 1E-9
  if t0==0: t0=t1; return
  if not ready:
    shoulder(0.35);  elbow(-1.0);  ready=True;  t0=t1;  print(msg);  return
  if not at_block:
    if t0+5>t1 and (abs(msg.position[4] - 0.35) > 0.03 or abs(msg.position[0]+1.0) > 0.03): return
    at_block=True;  left_finger(-0.1*fwd); right_finger(0.1*fwd);  t0=t1;  print(msg);  return
  if (fwd>0 and holding_block==False) or (fwd<0 and holding_block==True):
    if t0+5>t1 and (abs(msg.position[1]+0.1*fwd)>0.02 or abs(msg.position[2]-0.1*fwd)>0.02): return
    holding_block=not holding_block;  shoulder(1.0);  t0=t1;  print(msg);  return
  if t0+5>t1 and abs(msg.position[4]-1) > 0.1: return
  t0=t1;  fwd = -fwd;  ready=False;  at_block=False

def Image_cb(msg):
  I = np.fromstring(msg.data, np.uint8).reshape(msg.height,msg.width,3)
  cv2.imshow("Camera", I[:,:,::-1])
  cv2.waitKey(1)

if __name__=="__main__":
  pub = [rospy.Publisher('/smart_arm/%s_controller/command'%s, Float64, queue_size=2) \
         for s in 'shoulder_pan shoulder_pitch elbow_flex wrist_roll left_finger right_finger'.split()]
  base,shoulder,elbow,wrist,left_finger,right_finger = [p.publish for p in pub]
  rospy.init_node('smart_arm_pickup')
  rospy.rostime.wallsleep(0.5)
  rospy.Subscriber('/smart_arm/joint_states', JointState, JointState_cb, queue_size=1)
  rospy.Subscriber('/camera1/image_raw', Image, Image_cb, queue_size=1)
  rospy.spin()
'''
  try:
    while not rospy.core.is_shutdown():
      rospy.rostime.wallsleep(0.5)
  except KeyboardInterrupt:
    logdebug("keyboard interrupt, shutting down")
    for p in pub: p.publish(0.0)
    rospy.rostime.wallsleep(0.5)
    rospy.core.signal_shutdown('keyboard interrupt')
'''

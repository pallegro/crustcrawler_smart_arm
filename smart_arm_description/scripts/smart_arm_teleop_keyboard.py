#!/usr/bin/env python2
import rospy
from std_msgs.msg import Float64
import sys, select, termios, tty

msg = """

   base shoulder elbow wrist grip
+1 q w e r t
 0 a s d f g
-1 z x c v b

anything else : stop all motors

CTRL-C to quit
"""

bindings = {c:(i,3.1415/2*(j-(i!=1))) for j,cs in enumerate(('zxcvb','asdfg','qwert')) for i,c in enumerate(cs) }

def getKey():
  tty.setraw(sys.stdin.fileno())
  select.select([sys.stdin], [], [], 0)
  key = sys.stdin.read(1)
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
  return key

if __name__=="__main__":
  settings = termios.tcgetattr(sys.stdin)
  
  pub = [rospy.Publisher('/smart_arm/%s_controller/command'%s, Float64, queue_size=2) \
         for s in ('shoulder_pan', 'shoulder_pitch', 'elbow_flex',
                   'wrist_roll', 'left_finger', 'right_finger')]
  rospy.init_node('smart_arm_teleop_keyboard')
  try:
    print msg
    while(1):
      key = getKey()
      if key in bindings:
        i,j = bindings[key]
        pub[i].publish(Float64(j))
        if i==4: pub[5].publish(Float64(-j))
      else:
        for p in pub: p.publish(Float64(0.0))
        if key=='\x03': break
  except:
    print e
  finally:
    for p in pub: p.publish(Float64(0.0))
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

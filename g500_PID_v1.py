# A# Author: Ignacio Carlucho
# Date: 24/04/2017
# makes the uwsim with the girona submarine, and the scene: pipeFollowing_turns.xml
# To run:
# run: 
#   roscore
# then you have to run a dynamic simulation
#   roslaunch underwater_vehicle_dynamics UWSim_g500_dynamics.launch
# 
# I had trouble running roslaunch so I did 
# $ cd uwsim_ws
# $ source devel/setup.bash 
# and it worked
# also the configuration files are mentioned in: 
# uwsim_ws/src/underwater_simulation/underwater_vehicle_dynamics/launch/UWSim_g500_dynamics.launch
# here the scene used and the dynamic info of the auv are described.
# regarding the position, it is configured both in the scene xml as in the dynamic yaml
# so you need to change it in both files. 

# this script will read the speed of the dvl, and using a pid control the speed in the x axis


import rospy
# I knew that the thrusters were controlled by an array
from std_msgs.msg import Float64MultiArray
# rostopic type on /g500/camera1
from sensor_msgs.msg import Image
from underwater_sensor_msgs.msg import DVL

from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2

vel_v = 0

bridge = CvBridge()






def callback(msg):
  #http://answers.ros.org/question/210294/ros-python-save-snapshot-from-camera/
  print("Received an image!")
  try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
  except CvBridgeError, e:
        print(e)
  else:
        # Save your OpenCV2 image as a jpeg 
        cv2.imwrite('camera_image.jpeg', cv2_img)
        cv2_bw = cv2.cvtColor(cv2.resize(cv2_img, (80, 80)), cv2.COLOR_BGR2GRAY)
        cv2.imwrite('camera_image_black_white.jpeg', cv2_bw)
        # threshold. 
        #ret, cv2_bw_th = cv2.threshold(cv2_bw,1,255,cv2.THRESH_BINARY)
        #cv2.imwrite('camera_image_black_white_treshold.jpeg', cv2_bw_th)
       
        # print the image in your screen
        #cv2.imshow('image',cv2_img)
        #cv2.waitKey(1)
        #cv2.destroyAllWindows()

def callback_dvl(vel_msg):
  global vel_v
  #print('velocity reading', vel_msg.bi_x_axis)
  vel_v = vel_msg.bi_x_axis

def limit(value,limit):
  limited = value
  if value>limit:
    limited=limit
  if value< (-limit):
    limited = -limit
  return limited

def talker():
  
  print('starting node')
  
  # Publishers

  # here I am creating the publisher, you need to insert the topic name of the submarine
  pub = rospy.Publisher('/g500/thrusters_input', Float64MultiArray, queue_size=10) 
  # since this is a node, it needs to have a name
  rospy.init_node('talker', anonymous=False)
  rate = rospy.Rate(10) # 10hz
  

  # Now here I create a message, move odometry, from the twiststamped type of message
  msg = Float64MultiArray()
  
  msg.data = [0, 0, 0, 0, 0]
  
  # Reference velocity
  v_ref = 0.5 # m/s
  # Initialization values
  '''
  k1 = 0.0098
  k2 = 0.005
  k3 = 0.001
  '''
  Kp = 1
  Ti = 1
  Td = 0.001
  dt = 0.1
  k1=Kp*(1+Td/dt);
  k2=-Kp*(1+2*Td/dt-dt/Ti);
  k3=Kp*(Td/Ti);
  
  v0 = 0
  error_v0 = 0
  error_v1 = 0
  error_v2 = 0

  rospy.Subscriber('/g500/camera1', Image, callback, queue_size = 1)
  rospy.Subscriber('/g500/dvl', DVL, callback_dvl, queue_size = 1)      
  while not rospy.is_shutdown():
    
    
    
    # for now I dont pay attention to the camera
     
    print('velocity in x', vel_v)

    error_v2 = error_v1
    error_v1 = error_v0
    error_v0 = v_ref - vel_v
    control_v = v0 + k1*error_v0 + k2*error_v1+ k3* error_v2
    control_v = limit(control_v,1.0)
    msg.data[0] = control_v
    msg.data[1] = control_v
    v0 = control_v
    

    pub.publish(msg)
    rate.sleep()

  # when rospy has been shutdown (ctrl + c )stop turtlebot
  rospy.loginfo("Stop")
  print('Stopping node')
  # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
  pub.publish(msg)
  # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
  rospy.sleep(1)
  print('node stopped')




if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass

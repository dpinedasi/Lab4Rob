import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from math import pi
from getkey import getkey, keys

def joint_publisher():
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)
    aux=[0,0,0,0,0]
    while not rospy.is_shutdown():
        key=input()
        #if KeyboardInterrupt:
        #    key=getkey()
        state = JointTrajectory()
        state.header.stamp = rospy.Time.now()
        state.joint_names = ["joint_1","joint_2","joint_3","joint_4","joint_5"]
        point = JointTrajectoryPoint()
        if key == 'q':
            aux = [0,0,0,0,0]
            key=' '
        if key == 'a':
            aux = [-20*pi/180,20*pi/180,-20*pi/180,20*pi/180,0]
            key=' '
        elif key == 's':
            aux = [30*pi/180,-30*pi/180,30*pi/180,-30*pi/180,0]
            key=' '
        elif key == 'd':
            aux = [-90*pi/180,15*pi/180,-55*pi/180,17*pi/180,0]
            key=' '
        elif key == 'f':
            aux = [-90*pi/180,45*pi/180,-55*pi/180,45*pi/180,10*pi/180]   
            key=' ' 
        elif key == 'h':
            aux = point.positions = [0, -pi/2, pi/2, pi/4, 0]    
            key=' '     

        point.positions = aux   
        point.time_from_start = rospy.Duration(0.5)
        state.points.append(point)
        pub.publish(state)
        print('published command')
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        joint_publisher()
    except rospy.ROSInterruptException:
        pass
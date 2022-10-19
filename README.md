<h1 align="center"; style="text-align:center;">Laboratory 4: Direct kinematics - Phantom X - ROS</h1>
<p align="center";style="font-size:50px; text-align:center; line-height : 50px;  margin-top : 0; margin-bottom : 0; "> <br> Universidad Nacional de Colombia</p>
<p align="center";style="font-size:50px; text-align:center; line-height : 50px;  margin-top : 0; margin-bottom : 0; "> <br> Robotics</p>
<p align="center";style="font-size:50px; text-align:center; line-height : 40px;  margin-top : 0; margin-bottom : 0; "> <br> Santiago Mariño (samrinoj) - Daniel Pineda (dpinedasi)</p>


<p align="center"; style="font-size:50px; text-align:center; line-height : 30px; margin-top : 0; "> <br>October 19  2022</p>

<a href="http://www.dukelearntoprogram.com/" target="blank_">Duke Learn to Program </a>


## Solution Description

### Measurements
With the help of a caliper, the length of the links, which are found in figure 1, is measured. With these lengths and the angles of the Home position, the DHst table is made.

![Measurements](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/LINKS.png)

In the case of L1, two meassurements had to be done as the link has a L shape. Then the Pythagoras theorem was applied in order to find the minimum distance between the two join axes.

![DH parameters](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/dhstd.png)

With the previous table and through the Peter Corke library, the orientation of each joint can be shown:
![Home position](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q1PC.png)

### ROS-Dynamixel-Python

After that, the next task was to follow the instruccions described in the <a href="https://github.com/fegonzalez7/rob_unal_clase3" target="blank_">laboratory guide</a>. From wich the <a href="https://github.com/fegonzalez7/dynamixel_one_motor.git" target="blank_">Dynamixel_one_motor</a> was cloned. 

We use the Dynamixel wizard to test the operation of the motors and their joint ranges, from this a code is made in python to be able to control the robot through ROS.

The jointCommand function is defined, which initializes a node, and the interaction with the Dynamixel services is created, so that the ID of the joint is delivered, the addr_name, which is the action to be carried out, the value to change or target, and time. The command variable is left as a blank string.

```
def jointCommand(command, id_num, addr_name, value, time):
    #rospy.init_node('joint_node', anonymous=False)
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))

if __name__ == '__main__':
    try:
        # Goal_Position (0,1023)
        # Torque_Limit (0,1023)
        jointCommand('', 1, 'Torque_Limit', 400, 0)
        jointCommand('', 1, 'Goal_Position', 512, 0.5)
        time.sleep(0.5)
        jointCommand('', 1, 'Goal_Position', 255, 0.5)
    except rospy.ROSInterruptException:
        pass
```

The following lines of code are the ones that allow interlocking the keyboard command and the dynamixel services. By means of a while(), the action is executed indefinitely until the process is terminated with the 'ESC' key.

In this cycle the main idea is to give the functions to the keys 'q', 'a', 'd', 'f', 'h', which will represent each desired pose of the robot:
* q represents q1=[ 0 0 0 0]
* a represents q2=[-20pi/180,20pi/180,-20pi/180,20pi/180,0]
* d represents q3=[30pi/180,-30pi/180,30pi/180,-30pi/180,0]
* f represents q4= [-90pi/180,45pi/180,-55pi/180,45pi/180,10pi/180] 
* h represents q5= [0, -pi/2, pi/2, pi/4, 0]   

```
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
```
## Demonstration video
### LabSir Implementation
[![Implementation](http://img.youtube.com/vi/wPWUIFMu8iU/0.jpg)](https://www.youtube.com/watch?v=wPWUIFMu8iU&ab_channel=DanielPineda)

## Toolbox
The visualization of the robots is presented with the help of Peter Corke's toolbox in mathlab and it is compared with what is obtained from the physical implementation:
* For q1
![Home position](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q1PC.png)
* For q2
![q2](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q2PC.png)
* For q3
![q3](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q3PC.png)
* For q4
![q4](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q4PC.png)
* For q5
![q5](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q5PC.png)

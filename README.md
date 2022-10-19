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

Con la anterior tabla y por medio de la libreria de Peter Corke se puede mostrar la orientación de cada articulación:

![Home position](https://github.com/dpinedasi/Lab4Rob/blob/main/imagenes/q1PC.png)

### ROS-Dynamixel-Python

After that, the next task was to follow the instruccions described in the <a href="https://github.com/fegonzalez7/rob_unal_clase3" target="blank_">laboratory guide</a>. From wich the <a href="https://github.com/fegonzalez7/dynamixel_one_motor.git" target="blank_">Dynamixel_one_motor</a> was cloned. 

Usamos Dynamixel wizard para probar el funcionamiento de los motores y sus rangos articulares, apartir de esto se realiza un codigo en python para poder controlar el robot por medio de ROS .

Se define la función jointCommand, la cual inicializa un nodo, y se crea la interacción con los servicios de Dynamixel, de forma que se entrega el ID de la articulación, el addr_name, que es la acción que se va a realizar, el valor a cambiar u objetivo, y el tiempo. La variable command se deja como un string en blanco. 

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

Las siguientes líneas de código son las que permiten entrelazar el mando por teclado y los servicios de dynamixel. Por medio de un while(), se ejecuta la acción indefinida mente hasta que se termine el proceso con la tecla 'ESC'. 

En este ciclo la idea principal es brindar las funciones a las teclas 'q', 'a', 'd', 'f','h', las cuales represenatrán cada pose deseada del robot:
* q representa q1=[ 0 0 0 0]
* a representa q2=[-20pi/180,20pi/180,-20pi/180,20pi/180,0]
* d representa q3=[30pi/180,-30pi/180,30pi/180,-30pi/180,0]
* f representa q4= [-90pi/180,45pi/180,-55pi/180,45pi/180,10pi/180] 
* h representa q5= [0, -pi/2, pi/2, pi/4, 0]   

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



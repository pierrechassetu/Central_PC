# Central_PC
Code for the central PC to use with https://github.com/lalaorome/SycaBot_ros

# Connection from Motive to Central PC using VRPN:

- Make sure to source ROS
- Make sure that the PC’s are both connected to the server
- Make sure to launch roscore by using the `roscore` command
- In another terminal use (source ROS aswell) :

```powershell
roslaunch vrpn_client_ros sample.launch server:=192.168.1.2 # To establish the connection
# Name of the topic : vrpn_client_node/SycaBot[n]/pose
```

**WARNING : A connection established log doesn’t mean that the data is being transmitted.** 

```powershell
# The following messages should appear if the connection is well established : 
[INFO][...] : Connection established
[INFO][...] : Found new sender : **...**
[INFO][...] : Creating new tracker **...**
```

- You can always try to check the connection using the cmd :

```powershell
vrpn_print_devices <name2track>@<server_address>
```

# Connection from motive to central PC using Mocap_Optitrack:

- Make sure to source ROS
- Make sure that the PC’s are both connected to the server
- Make sure to launch roscore using the `roscore` command
- In another terminal use (source ROS aswell) :

```powershell
roslaunch mocap_optitrack mocap.launch mocap_config_file:=<path_to_filename.yaml> # To establish the connection
```

- Topics name are the one that you wrote in the config file e.g. **/mocap_node/RigidBody1Name/pose**

---

## Example of a config.yaml file

```powershell
rigid_bodies:
    ['1':
        pose: RigidBody1Name/pose
        pose2d: RigidBodyName/ground_pose
        child_frame_id: RigidBodyName/base_link
        parent_frame_id: world]
    ['2':
        pose: RigidBody2Name/pose
        pose2d: RigidBody2Name/ground_pose
        child_frame_id: RigidBody2Name/base_link
        parent_frame_id: world]
		
optitrack_config:
        multicast_address: 224.0.0.1 #Should be the same as the one in Motive
				command_port: 1510 # Should be the same as the one in motive
				data_port: 1511 #Should be the same as the one in motive

```

# Bridging ROS1 and ROS2 to listen to ROS topics

- Terminal 1 :
    - 1st : Source ROS
    - 2nd : Source ROS2
    - Input the command : `ros2 run ros1_bridge dynamic_bridge`
- To test the connection with ROS2 :
    - Open a new terminal and input : ros2 topic echo <topic_name> <topic_type>
        
        **WARNING : you have to specifiy the type whereas the echo command doesn’t work because the bridge is made only when a subscriber exists for the topic.**

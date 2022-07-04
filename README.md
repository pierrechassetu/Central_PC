# Central_PC
Code for the central PC to use with https://github.com/lalaorome/SycaBot_ros

Please don't hesitate to read the report.pdf file for further informations.

Have a look at ROS2_Toolkit if you want a catch up on ROS2 basics.

## How to launch the execution ?

Clone this package : 
```powershell
git clone https://github.com/lalaorome/Central_PC
```

### Step 1 : Build the package 

Build the package using colcon :

```powershell
source /opt/ros/foxy/setup.bash
cd ~/path_to_centralPC/
colcon build --symlink-install
```
Close the terminal.

### Step 2 : Launch fast-rtps discovery server

In one terminal input command : `fastrtps discovery -i 0 `

### Step 3 : Launch vrpn communication to get positions of robots and init ROS1->ROS2 bridge

In another terminal : `source ~/path_to_centralPC/init_roscore.sh`
In a new terminal : `source ~/path_to_centralPC/init_vrpn.sh`
In a third terminal : `source ~/path_to_centralPC/init_bridge.sh`

Keep the three terminals running.

WARNING : you should use wireshark to check that the robots are well aware of the discovery server before initialising these nodes. 

To do so : 
- Launch wireshark and start analysing the network on which the jetbots are connected to
- Filter the ip adress of the robot
- Check that the communication alternate well and smoothly between Client and Server
[Picture yet to come]

### Step 4 : Start the central PC node

In another terminal source local setup of central PC, init the environment variables for the discovery server and run the node : 
```powershell
source ~/path_to_centralPC/setup_ROS.sh --srv id --pkg central_pc #Where id is the last number 192.168.1.x of the ip adress of the computer on wlan0
ros2 run central_pc start
```

### Step 5 (temporary) : Use the node of Sycabot_ros package

clone Sycabot_ros package and build it :

```powershell
git clone https://github.com/lalaorome/SycaBot_ros
cd ~/path_to_SycaBot-ros/
source /opt/ros/foxy/setup.bash
colcon build --symlink-install
```
Close the previous terminal. Open a new terminal and launch the node :

```powershell
cd ~/path_to_SycaBot-ros/
source setup_ROS.sh --srv id #Where id is the last number 192.168.1.x of the ip adress of the computer on wlan0
ros2 launch jetbot motors.launch.py
```
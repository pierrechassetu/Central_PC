#!/bin/bash

source /opt/ros/noetic/setup.bash
export ROS_IP=192.168.1.5
export ROS_HOSTNAME=192.168.1.5
export ROS_MASTER_URI=http://192.168.1.5:11311
rosclean
roscore

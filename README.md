# How to

Using this python script you can control the velocity of the girona auv in the uwsim simulator.  
This script will read the speed of the auv, taken from the dvl, and control Vx using a PID controller.  
This version is not correctly tuned but it works as a demo.  

## 1. Install Ubuntu

install ubuntu 14.04 , because it is compatible with ros indigo and uwsim. 

I prefer xubuntu 14.04.02:
https://xubuntu.org/news/14-04-release/

## 2. Install ros Indigo:

http://wiki.ros.org/indigo/Installation/Ubuntu

You can use the next commands: 

`sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' `
`sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116`  
`sudo apt-get update`  
`sudo apt-get install ros-indigo-desktop-full`  
`sudo rosdep init`  
`rosdep update`  
`echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc`  
`source ~/.bashrc`  


## 3. Install uwsim: 

Following this steps: 

http://www.irs.uji.es/uwsim/wiki/index.php?title=Let%27s_do_it:_Pipe_following

Don't forget to:   

`cd ~/uwsim_ws/src/underwater_simulation/uwsim`  
`./data/scenes/installScene -s pipeFollowing_basic.uws`   
`./data/scenes/installScene -s pipeFollowing_turns.uws`  
`./data/scenes/installScene -s pipeFollowing_heights.uws`  



If you followed the steps correctly


- 1st terminal:   
 `roscore`

- 2nd terminal:   
 `cd uwsim_ws  
 rosrun uwsim uwsim --configfile uwsim_ws/src/underwater_simulation/uwsim/data/scenes/pipeFollowing_turns.xml`

- 3rd you can see the camera:    
`cd uwsim_ws  
rosrun image_view image_view image:=/g500/camera1`  

- 4th I can send commands to the submarine:  

`cd uwsim_ws  
rosrun uwsim setVehicleVelocity /dataNavigator 0.2 0 0 0 0 0`  

- The simulation parameters can be chaged with:  

/uwsim_ws/src/underwater_simulation/uwsim/data/scenes/pipeFollowing_turns.xml


## 4. Clone this repo:

`cd folder_that_you_want_to_store_this`  
`git clone https://github.com/IgnacioCarlucho/PID_uwsim`   

## 5. Now you can set the velocity with the PID-python node

`cd to_file_location`  
`python g500_PID_v1.py`  






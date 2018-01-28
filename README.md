# How to

Using this python script you can control the velocity of the girona auv in the uwsim simulator.  
This script will read the speed of the auv, taken from the dvl, and control Vx using a PID controller.  
This version is not correctly tuned but it works as a demo.  


## 1. Install uwsim: 

Following this steps: 

http://www.irs.uji.es/uwsim/wiki/index.php?title=Let%27s_do_it:_Pipe_following

You should also install the scenes:   

`cd ~/uwsim_ws/src/underwater_simulation/uwsim`  
`./data/scenes/installScene -s pipeFollowing_basic.uws`   
`./data/scenes/installScene -s pipeFollowing_turns.uws`  
`./data/scenes/installScene -s pipeFollowing_heights.uws`  
`cd ~/uwsim_ws/ `  
`catkin_make install `  


If you followed the steps correctly


- 1st terminal:   
 `roscore`

- 2nd terminal:   
 ```cd uwsim_ws
 rosrun uwsim uwsim --configfile uwsim_ws/src/underwater_simulation/uwsim/data/scenes/pipeFollowing_turns.xml
 ```

- 3rd you can see the camera:    
```
cd uwsim_ws 
rosrun image_view image_view image:=/g500/camera1
 ```  

- 4th I can send commands to the submarine:  

```
cd uwsim_ws  
rosrun uwsim setVehicleVelocity /dataNavigator 0.2 0 0 0 0 0
```

- The simulation parameters can be chaged with:  
```
/uwsim_ws/src/underwater_simulation/uwsim/data/scenes/pipeFollowing_turns.xml
```

## 2. Clone this repo:

`cd folder_that_you_want_to_store_this`  
`git clone https://github.com/IgnacioCarlucho/PID_uwsim`   

## 3. Now to do a dynamic simulation:

`roslaunch underwater_vehicle_dynamics UWSim_g500_dynamics.launch`


## 4. Disable keyboard control:

This is necessary because if not, the keyboard will be sending Zeros to the thruster controller, and therefore interfering with the  PID controller. So you need to do :   

`gedit uwsim_ws/src/underwater_simulation/underwater_vehicle_dynamics/launch/UWSim_g500_dynamics.launch`  

and comment the line: 

`<node name="keyboard_command" pkg="underwater_vehicle_dynamics" type="keyboard.py" args="$(arg thrusters_topic)" output="screen" respawn="false"/>`  

Comments in xml are done like this: 

`<!--node name="keyboard_command" pkg="underwater_vehicle_dynamics" type="keyboard.py" args="$(arg thrusters_topic)" output="screen" respawn="false"/-->`

if you have questions just check this link: 

- [Creating matlab controler Uwsim](http://www.irs.uji.es/uwsim/wiki/index.php?title=First_steps:_Creating_a_controller_with_Matlab_-_Simulink)

## 5. Now you can set the velocity with the PID-python node

`cd to_file_location`  
`python g500_PID_v1.py`  

## 6. Change scenery

Now this dynamic simulation will happen inside the tank of the girona lab.  
You can change the scene by modifiying the file:   

uwsim_ws/src/underwater_simulation/underwater_vehicle_dynamics/launch/UWSim_g500_dynamics.launch    
from: 
`<arg name="scene" default="circs.xml" />`  
to  
`<arg name="scene" default="pipeFollowing_turns.xml" />`  
or wathever scenery you like  

If you do this, also take in to account that you may need to change the position of the AUV. And this needs to be done on two files: 

```
uwsim_ws/src/underwater_simulation/underwater_vehicle_dynamics/config/dynamics_g500.yaml
```
In here position is the line 

`g500/dynamics/initial_pose: [0.0, 0.0, 5.0, 0, 0, 1.57]` 

and put the same position as you put in the last one in: 

```
src/underwater_simulation/uwsim/data/scenes/pipeFollowing_turns.xml
```
This way the Auv will start in a give position, without the markers saying that it moved. 




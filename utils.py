containers = {
    "test": [
        "ros-dev-macos"
    ],

    "base":
        ["Work"],

    "fast-lio-ros1":
        ["dual-docker"],

    "fast-lio-ros2":
        ["Work"],

    "fast-livo":
        ["Work", "dual-docker3"],

    "camera-detection":
        ["Work"],

    "perception-reconstruction":
        ["Work"],

    "dnn":
        ["Work"],

}

LOCAL_HOSTNAME = "192.168.68.72"
REMOTE_HOSTNAME = "192.168.68.86"
HOSTNAME = "192.168.68.86"
USERNAME = "junchi"
PASSWORD = "helloworld"

options = {
    "base": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": r"""
         docker start  Work
         docker exec Work bash -c "source install/setup.bash && ros2 launch isaac_ros_argus_camera isaac_ros_argus_camera_stereo.launch.py" &
         docker exec Work bash -c "source install/setup.bash && ros2 launch livox_ros_driver2 msg_MID360_launch.py"      
"""
    },

    "fast-lio-ros1": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": f"""
            docker start  dual-docker && docker exec dual-docker bash -c "export ROS_IP={REMOTE_HOSTNAME} &&export ROS_HOSTNAME={REMOTE_HOSTNAME} && export ROS_MASTER_URI=http://{REMOTE_HOSTNAME}:11311 && source noetic/ros1/catkin_ws/devel/setup.bash && roslaunch fast_lio mapping_mid360.launch rviz:=false"   &    
            sleep 5
            docker start  dual-docker && docker exec dual-docker bash -c "source noetic/ros1/devel/setup.bash && roslaunch livox_ros_driver2 msg_MID360.launch" 
            """
    },

    "fast-lio-ros2": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": r"""
            docker start  Work
            docker exec Work bash -c "source install/setup.bash && ros2 launch livox_ros_driver2 msg_custom_mid360.py" &
            docker exec Work bash -c "source install/setup.bash && ros2 launch fast_lio mapping.launch.py rviz:=false" 
"""
    },

    "fast-livo": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": f"""
            docker start  Work && docker start dual-docker3
            docker exec Work bash -c "source install/setup.bash && ros2 launch isaac_ros_argus_camera isaac_ros_argus_camera_stereo.launch.py"   &
            sleep 5
            docker exec dual-docker3 bash -c "source noetic/ros1/devel/setup.bash && roslaunch livox_ros_driver2 msg_MID360.launch" &
            sleep 5
            docker exec dual-docker3 bash -c "source noetic/ros1/devel/setup.bash && source noetic/install_isolated/setup.bash && rosparam load isaac_ros-dev/src/ros1_bridge/bridge.yaml && source isaac_ros-dev/install/setup.bash && ros2 run ros1_bridge parameter_bridge" & 
            sleep 5
            docker exec dual-docker3 bash -c "export ROS_IP={REMOTE_HOSTNAME} && export ROS_HOSTNAME={REMOTE_HOSTNAME} && export ROS_MASTER_URI=http://{REMOTE_HOSTNAME}:11311 && source noetic/ros1/catkin_ws/devel/setup.bash && roslaunch fast_livo mapping_mid360.launch" 
"""
    },

    "dnn": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": r"""
            docker start Work
            docker exec Work bash -c "source install/setup.bash && ros2 launch isaac_ros_examples isaac_ros_examples.launch.py launch_fragments:=argus_stereo,rectify_stereo,ess_disparity \
engine_file_path:=/workspaces/isaac_ros-dev/isaac_ros_assets/models/dnn_stereo_disparity/dnn_stereo_disparity_v4.0.0/ess.engine \ threshold:=0.35" 
    """
    },

    "camera-detection": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": r"""
             docker start  Work
             docker exec -it Work -c "source install/setup.bash && ros2 launch isaac_ros_examples isaac_ros_examples.launch.py launch_fragments:=argus_stereo,rectify_stereo,ess_disparity \
engine_file_path:=${ISAAC_ROS_WS}/isaac_ros_assets/models/dnn_stereo_disparity/dnn_stereo_disparity_v4.0.0/ess.engine \ threshold:=0.35" 
    """
    },

    "perception-reconstruction": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": r"""
             docker start  Work
             docker exec Work -c "source install/setup.bash && ros2 launch isaac_ros_examples isaac_ros_examples.launch.py launch_fragments:=argus_stereo,rectify_stereo,ess_disparity \
engine_file_path:=${ISAAC_ROS_WS}/isaac_ros_assets/models/dnn_stereo_disparity/dnn_stereo_disparity_v4.0.0/ess.engine \ threshold:=0.35" 
    """
    },

    # "test": {
    #     "hostname": "localhost",
    #     "username": "xinyuli",
    #     "password": "1998!1204",
    #     "command": r"""
    #         source .zshrc
    #         docker start ros-dev-macos
    #         echo "start talker" && docker exec ros-dev-macos bash -c "source ros_entrypoint.sh && ros2 run demo_nodes_cpp talker" &
    #         echo "start listener" && docker exec ros-dev-macos bash -c "source ros_entrypoint.sh && ros2 run demo_nodes_cpp listener"
    #     """
    #
    # },
}

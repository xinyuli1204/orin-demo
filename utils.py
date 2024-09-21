
containers = {
    "base": ["Work"],
    "dnn": ["Work"],
    "fast-lio-ros1": ["dual-docker"],
    "fast-lio-ros2": ["Work"],
    "fast-livo": ["Work", "dual-docker3"],
    "camera-detection": ["yolo3D", "Work"],
    "perception-reconstruction": ["Work"],
    "bev-fusion": ["yolo3D", "Work"]
}

# Host configurations
LOCAL_HOSTNAME = "192.168.68.72"  # laptop ip , please change
REMOTE_HOSTNAME = "192.168.68.86"  # orin ip , please change
HOSTNAME = REMOTE_HOSTNAME  # Set the active hostname
USERNAME = "junchi"  # orin username , please change
PASSWORD = "helloworld"  # orin password , please change


# Command templates
def base_command():
    return """
        docker start  Work
        docker exec Work bash -c "source install/setup.bash && ros2 launch isaac_ros_argus_camera isaac_ros_argus_camera_stereo.launch.py" &
        docker exec Work bash -c "source install/setup.bash && ros2 launch livox_ros_driver2 msg_MID360_launch.py"  
    """


def fast_lio_ros1_command():
    return f"""
        docker start dual-docker
        docker exec dual-docker bash -c "source noetic/ros1/devel/setup.bash && \
            roslaunch livox_ros_driver2 msg_MID360.launch" &
        sleep 5
        docker exec dual-docker bash -c "export ROS_IP={REMOTE_HOSTNAME} && \
            export ROS_HOSTNAME={REMOTE_HOSTNAME} && \
            export ROS_MASTER_URI=http://{REMOTE_HOSTNAME}:11311 && \
            source noetic/ros1/catkin_ws/devel/setup.bash && \
            roslaunch fast_lio mapping_mid360.launch rviz:=false"    
      
    """


def fast_lio_ros2_command():
    return """
        docker start Work
        docker exec Work bash -c "source install/setup.bash && \
            ros2 launch livox_ros_driver2 msg_custom_mid360.py" &
        docker exec Work bash -c "source install/setup.bash && \
            ros2 launch fast_lio mapping.launch.py rviz:=false"
    """


def fast_livo_command():
    return f"""
        docker start Work && docker start dual-docker3
        docker exec Work bash -c "source install/setup.bash && \
            ros2 launch isaac_ros_argus_camera isaac_ros_argus_camera_stereo.launch.py" &    
        sleep 5
        docker exec dual-docker3 bash -c "source noetic/ros1/devel/setup.bash && \
            roslaunch livox_ros_driver2 msg_MID360.launch" &
        sleep 5
        docker exec dual-docker3 bash -c "source noetic/ros1/devel/setup.bash && \
            source noetic/install_isolated/setup.bash && \
            rosparam load isaac_ros-dev/src/ros1_bridge/bridge.yaml && \
            source isaac_ros-dev/install/setup.bash && \
            ros2 run ros1_bridge parameter_bridge" &
        sleep 5
        docker exec dual-docker3 bash -c "export ROS_IP={REMOTE_HOSTNAME} && \
            export ROS_HOSTNAME={REMOTE_HOSTNAME} && \
            export ROS_MASTER_URI=http://{REMOTE_HOSTNAME}:11311 && \
            source noetic/ros1/catkin_ws/devel/setup.bash && \
            roslaunch fast_livo mapping_mid360.launch"
    """


def dnn_command():
    return """
        docker start Work
        docker exec Work bash -c "source install/setup.bash && ros2 launch isaac_ros_examples isaac_ros_examples.launch.py launch_fragments:=argus_stereo,rectify_stereo,ess_disparity \
            engine_file_path:=/workspaces/isaac_ros-dev/isaac_ros_assets/models/dnn_stereo_disparity/dnn_stereo_disparity_v4.0.0/ess.engine threshold:=0.35"
    """


def camera_detection_command():
    return """
        docker start Work && docker start yolo3D
        docker exec Work bash -c "source install/setup.bash && \
            ros2 launch isaac_ros_examples isaac_ros_examples.launch.py launch_fragments:=argus_stereo" &
        docker exec Work bash -c "source install/setup.bash && ros2 launch livox_ros_driver2 msg_MID360_launch.py" &
        docker exec yolo3D bash -c "source install/setup.bash && \
            ros2 launch ultralytics_ros tracker_with_cloud.launch.xml debug:=true device:="cuda:0" \
            camera_info_topic:=/left/camera_info lidar_topic:=/livox/lidar \
            yolo_result_topic:=/yolo_image yolo_3d_result_topic:=/yolo_result" 
    """


def perception_reconstruction_command():
    return """
        docker start Work
        docker exec Work bash -c "source install/setup.bash && ./src/detection.sh"
    """


def bev_fusion_command():
    return """
        docker start yldocker
        docker exec yldocker bash -c "source install/setup.bash && \
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/workspaces/isaac_ros-dev/src/BEVFusion-ROS-TensorRT/third_party/3DSparseConvolution/libspconv/lib/aarch64 && \
            ros2 bag play {path/to/your/ros2bag} -l &  \
            ros2 run bevfusion bevfusion_node 
    """


# Mapping container names to options
options = {
    "base": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": base_command(),
    },

    "dnn": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": dnn_command(),
    },

    "fast-lio-ros1": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": fast_lio_ros1_command(),
    },
    "fast-lio-ros2": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": fast_lio_ros2_command(),
    },
    "fast-livo": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": fast_livo_command(),
    },

    "camera-detection": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": camera_detection_command(),
    },

    "perception-reconstruction": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": perception_reconstruction_command(),
    },


    # using public dataset! replace HOSTNAME USERNAME PASSWORD to ECU HOSTNAME, USERNAME, PASSWORD
    "bev-fusion": {
        "hostname": HOSTNAME,
        "username": USERNAME,
        "password": PASSWORD,
        "command": bev_fusion_command(),
    },
}

RVIZ_TEMPLATE = {
    "base": "/rviz_config/base.rviz",
    "dnn": "/rviz_config/dnn.rviz",
    "fast-lio-ros1": "/rviz_config/fastlio_ros1.rviz",
    "fast-lio-ros2": "/rviz_config/fastlio.rviz",
    "fast-livo": "/rviz_config/loam_livox.rviz",
    "camera-detection": "/rviz_config/yolov8.rviz",
    "perception-reconstruction": "",
    "bev-fusion": "/rviz_config/composite_image.rviz",
}

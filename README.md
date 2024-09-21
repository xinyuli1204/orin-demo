# Launch Demo Script and Calibration

To run the demo, execute the following command:

```bash
./launch_demo.sh
```
The launch_demo.sh script is located at /home/xinyu/

### Notes

1. When using the DNN model and trying to open RViz, it might quit immediately due to the depth information not being ready. Please wait for a moment or add the depth topic manually, see video in the Desktop. And unclick the Normalization range 

2. For the calibration process, navigate to ~/livox_calib_script and run the following scripts in order:

    - First, run save_image.sh and wait for around 15 seconds. It will stop automatically:  `./save_image.sh`
    - Second, run fast_lio_save.sh. Use Ctrl+C to stop saving the PCD file:`./fast_lio_save.sh`

    Third, launch a new terminal and run: `./livox_calib_launch.sh`
    This will start the calibration.

You can find configuration files in the mounted workspaces directory at:

`/mnt/nova_ssd/workspaces/noetic/ros1/catkin_ws/src/livox_camera_calib/config/`

To view the contents of customcalib.yaml, run:

`cat customcalib.yaml`

```
common:
    image_file: "/workspaces/isaac_ros-dev/left_resize_image.jpg"
    pcd_file: "/workspaces/noetic/ros1/catkin_ws/src/FAST_LIO/PCD/scans.pcd"
    result_file: "/workspaces/noetic/ros1/catkin_ws/src/livox_camera_calib/result/extrinsic.txt"
```

After calibration, the latest results can be found in:

```
/mnt/nova_ssd/workspaces/noetic/ros1/catkin_ws/src/livox_camera_calib/result/extrinsic.txt
```
Finally, update the extrinsic parameters in FAST_LIVO package:

```
/mnt/nova_ssd/workspaces/noetic/ros1/catkin_ws/src/FAST-LIVO/config/mid360.yml
```

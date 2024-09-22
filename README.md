# Launch Demo Script and Calibration

To run the demo, execute the following command:

```bash
./launch_demo.sh
```
The launch_demo.sh script is located at /home/xinyu/

### Notes
#### DNN model
When using the DNN model and trying to open RViz, it might quit immediately due to the depth information not being ready. Please wait for a moment or add the depth topic manually, see video in the Desktop. And unclick the Normalization range 
####  Calibration + Fast livo
For the calibration process, navigate to ~/livox_calib_script folder and run the following scripts in order:

- First, run save_image.sh and wait for around 15 seconds. It will stop automatically:  `./save_image.sh` the left_resize_image.jpg will be saved in `/workspaces/isaac_ros-dev/left_resize_image.jpg`.
- Second, run fast_lio_save.sh. Use Ctrl+C to stop saving the PCD file:`./fast_lio_save.sh` scans.pcd will be saved under `/workspaces/noetic/ros1/catkin_ws/src/FAST_LIO/PCD/`

- Third, launch a new terminal and run: `./livox_calib_launch.sh`
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


customcalib.yaml points to config_indoor.yaml

https://github.com/hku-mars/livox_camera_calib/blob/master/config/config_indoor.yaml

original ExtrinsicMat: !!opencv-matrix is looks like this
```
  data: [0.0,   -1.0,   0.0,    0.0,
         0.0,  0.0,  -1.0,    0.0,
         1.0,   0.0,    0.0,    0.0,
         0.0,   0.0,    0.0,    1.0]
```

_**not sure if we need to change this  ExtrinsicMat_** 

After calibration, the latest results can be found in:

```
/mnt/nova_ssd/workspaces/noetic/ros1/catkin_ws/src/livox_camera_calib/result/extrinsic.txt
```

Extrinsic calibration result looks like this with rotational matrix and translational matrix:
```
0.212305,0.160953,0.963857,-2.05332
0.0466092,-0.986888,0.154533,1.89354
0.976091,0.0121166,-0.217023,0.0249478
0,0,0,1
```


Finally, update the extrinsic parameters in FAST_LIVO package:

```
/mnt/nova_ssd/workspaces/noetic/ros1/catkin_ws/src/FAST-LIVO/config/mid360.yml
```

first 3  x 3 matrix  is RCL : 
```
0.212305,0.160953,0.963857
0.0466092,-0.986888,0.154533
0.976091,0.0121166,-0.217023
```
last column is PCL :
```Pcl: [-2.05332, 1.89354,0.0249478]```

#### Fast Lio
in `/workspaces/isaac_ros-dev/src/fast_lio/config/mid360.yaml`, may need to change blind, the parameter blind controls the minimum distance fast-lio use
the default is set to 0.5.
```
 preprocess:
    lidar_type: 1 
    scan_line:  4
    blind: 0.5
    timestamp_unit: 3
    scan_rate: 10
```


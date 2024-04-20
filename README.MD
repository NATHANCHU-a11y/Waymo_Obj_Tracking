
## Waymo Object Tracking Dataset to COCO Format
Used package from github to convert Waymo Object Tracking Dataset to COCO format.
```angular2html
conda create -n waymococo python=3.7
conda activate waymococo
pip install tensorflow==2.1.0
git clone https://github.com/shinya7y/WaymoCOCO.git
cd WaymoCOCO
```
Transform tfrecord to coco format for testing data.
Volidation data and Training data are similar with below.
```angular2html
python3 convert_waymo_to_coco.py \
--tfrecord_dir ~/Waymo_Obj_Tracking/dataset/testing/ \
--work_dir ~/Waymo_Obj_Tracking/data/testing/ \
--image_dirname val2020 \
--image_filename_prefix val \
--label_filename instances_val2020.json \
--add_waymo_info
```
The dataset is now in COCO format. The dataset contains the following classes:
```angular2html
TYPE_VEHICLE
TYPE_PEDESTRIAN
TYPE_CYCLIST
```
## Transform COCO Format to YOLO Format
In order to train YOLOv8 on the dataset, we need to convert the COCO format to YOLO format. The data store in `/data` folder.
```angular2html
python3 convert_coco_to_yolo.py
```
## Object Detection with YOLOv8
In order to use SORT to track the objects, we need to detect the objects first. 
In this step, we will train YOLOv8 on the dataset. Used pre-trained weights from YOLOv8. Then, I trained the model on the Waymo Open Dataset.
Both code are write in Jupyter Notebook. The result is shown in folder `runs/detect/`.
The example of output is shown below.

## Object Tracking with SORT
After detecting the objects, we can use SORT to track the objects.
I used Yolov8's output to track the objects, which includes the bounding box and the class of the object.
And tuned parameter to get the best result.
The code is also writen in Jupyter Notebook.
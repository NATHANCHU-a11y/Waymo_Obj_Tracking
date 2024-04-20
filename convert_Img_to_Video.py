import cv2
import os
import glob

files = glob.glob('generated_imgs/sort_output_images/*.jpg')
# files = glob.glob('generated_imgs/yolo_output_images/*.jpg')

files.sort(key=os.path.getmtime)

img = cv2.imread(files[0])
height, width, _ = img.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('videos/sort_output.mp4', fourcc, 20.0, (width, height))
# out = cv2.VideoWriter('videos/yolo_output.mp4', fourcc, 10.0, (width, height))

for file in files:
    img = cv2.imread(file)
    out.write(img)

out.release()

import cv2
import os
import glob

files = glob.glob('testing/camera1/*.jpg')

files.sort(key=os.path.getmtime)

img = cv2.imread(files[0])
height, width, _ = img.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_images/output.mp4', fourcc, 20.0, (width, height))

for file in files:
    img = cv2.imread(file)
    out.write(img)

out.release()
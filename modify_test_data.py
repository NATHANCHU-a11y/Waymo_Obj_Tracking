import os
import shutil

files = os.listdir('datasets/data/testing/val2020')

for file in files:
    filename_without_ext = os.path.splitext(file)[0]
    camera_number = int(filename_without_ext.split('_')[-1].replace('camera', ''))
    os.makedirs(f'datasets/data/testing/val2020/camera{camera_number}', exist_ok=True)
    shutil.move(f'datasets/data/testing/val2020/{file}',
                f'datasets/testing/camera{camera_number}/{file}')
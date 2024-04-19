import os
import shutil

# List all files in the 'test/val' directory
files = os.listdir('data/testing/val2020')

# Move files to the corresponding directories
for file in files:
    # Remove the file extension
    filename_without_ext = os.path.splitext(file)[0]

    # Extract the camera number from the file name
    camera_number = int(filename_without_ext.split('_')[-1].replace('camera', ''))

    # Create directory for this camera if it doesn't exist
    os.makedirs(f'data/testing/val2020/camera{camera_number}', exist_ok=True)

    # Move the file to the corresponding directory
    shutil.move(f'data/testing/val2020/{file}',
                f'testing/camera{camera_number}/{file}')
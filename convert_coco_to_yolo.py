import json
import os
import shutil
import yaml


def convert_to_yolo(input_images_path, input_json_path, output_images_path, output_labels_path):
    f = open(input_json_path)
    data = json.load(f)
    f.close()

    os.makedirs(output_images_path, exist_ok=True)
    os.makedirs(output_labels_path, exist_ok=True)

    file_names = []
    for filename in os.listdir(input_images_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            source = os.path.join(input_images_path, filename)
            destination = os.path.join(output_images_path, filename)
            shutil.copy(source, destination)
            file_names.append(filename)

    def get_img_ann(image_id):
        return [ann for ann in data['annotations'] if ann['image_id'] == image_id]

    def get_img(filename):
        return next((img for img in data['images'] if img['file_name'] == filename), None)

    for filename in file_names:
        img = get_img(filename)
        img_id = img['id']
        img_w = img['width']
        img_h = img['height']
        img_ann = get_img_ann(img_id)

        if img_ann:
            with open(os.path.join(output_labels_path, f"{os.path.splitext(filename)[0]}.txt"), "a") as file_object:
                for ann in img_ann:
                    if 'segmentation' in ann and ann['segmentation'] is not None:
                        current_category = ann['category_id'] - 1
                        polygon = ann['segmentation'][0]
                        normalized_polygon = [format(coord / img_w if i % 2 == 0 else coord / img_h, '.6f') for i, coord
                                              in
                                              enumerate(polygon)]
                        file_object.write(f"{current_category} " + " ".join(normalized_polygon) + "\n")
                    else:
                        bbox = ann['bbox']
                        x_center = bbox[0] + bbox[2] / 2
                        y_center = bbox[1] + bbox[3] / 2
                        width = bbox[2]
                        height = bbox[3]
                        normalized_bbox = [x_center / img_w, y_center / img_h, width / img_w, height / img_h]
                        current_category = ann['category_id'] - 1
                        file_object.write(f"{current_category} " + " ".join(map(str, normalized_bbox)) + "\n")


def create_yaml(input_json_path, output_yaml_path, train_path, val_path, test_path):
    with open(input_json_path) as f:
        data = json.load(f)

    names = [category['name'] for category in data['categories']]

    nc = len(names)

    yaml_data = {
        'names': names,
        'nc': nc,
        'test': test_path if test_path else '',
        'train': train_path,
        'val': val_path
    }

    # Write the dictionary to a YAML file
    with open(output_yaml_path, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False)


if __name__ == "__main__":
    base_input_path = "datasets/data/"
    base_output_path = "datasets/yolo_dataset/"

    # Processing validation dataset (if needed)
    convert_to_yolo(
        input_images_path=os.path.join(base_input_path, "validation/val2020"),
        input_json_path=os.path.join(base_input_path, "validation/annotations/instances_val2020.json"),
        output_images_path=os.path.join(base_output_path, "validation/images"),
        output_labels_path=os.path.join(base_output_path, "validation/labels")
    )

    # Processing training dataset
    convert_to_yolo(
        input_images_path=os.path.join(base_input_path, "training/val2020"),
        input_json_path=os.path.join(base_input_path, "training/annotations/instances_val2020.json"),
        output_images_path=os.path.join(base_output_path, "training/images"),
        output_labels_path=os.path.join(base_output_path, "training/labels")
    )

    # Creating the YAML configuration file
    create_yaml(
        input_json_path=os.path.join(base_input_path, "training/annotations/instances_val2020.json"),
        output_yaml_path=os.path.join(base_output_path, "data.yaml"),
        train_path="training/images",
        val_path="validation/images",
        test_path=None
    )

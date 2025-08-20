# Imports
from ultralytics import YOLO
import os
from pathlib import Path
import skimage as ski
from typing import List, Optional, Union

proj_path = os.getcwd()

# Create YOLO 1.1 formated directory

def create_yolo_1_1_dir(
    class_names: list,
    datasets=['train', 'val', 'test'],
    output_dir=Path(proj_path),
):
    # Create dataset directories
    for dataset in datasets: 
        output_dir.mkdir()
        
    # Write config.yaml
    config_yaml = [
        '\n',
        f'path: {proj_path}\n',
        'train: train\n',
        'val: val\n',
        'test: test\n',
        '\n',
        '# Classes\n',
        f'nc: {len(class_names)}\n'
    ]
    with open('config.yaml', 'w') as f:
        for line in config_yaml:
            f.write(line)
        f.write('names:\n')
        for i, name in enumerate(class_names):
            f.write(f' {i}: {name}\n')
    
    # Write obj.data
    data=[
        'classes = 12',
        'names = obj.names',
        'train = train.txt',
        'val = val.txt',
        'test = test.txt'
    ]
    with open('obj.data', 'w') as f:
        for line in data:
            f.write(line+'\n')

    # Write obj.names
    with open('obj.names', 'w') as f:
        for name in class_names:
            f.write(f'{name}\n')


# Function to generate new train/val/test.txt file for model directory in YOLO 1.1 format.
# dataset_type: 'val' | 'train' | 'test'
def gen_txt_file(dataset_type):

    dataset_folder = Path(f'{os.getcwd()}/{dataset_type}')
    
    with open(f'{dataset_type}.txt', 'w') as f:
        for file in dataset_folder.iterdir():
            if file.suffix == '.png':
                f.write(f'{dataset_type}/{file.name}\n')


# Function is adapted from Ultralytics, auto annotate images using pretrained YOLO model and the YOLO 1.1 format
# Note: This adaption removes the SAM metadata for seamless import to CVAT
def auto_annotate_no_SAM(
    data: Union[str, Path],
    det_model: str = "yolo11x.pt",
    device: str = "",
    conf: float = 0.25,
    iou: float = 0.45,
    imgsz: int = 640,
    max_det: int = 300,
    classes: Optional[List[int]] = None,
    output_dir: Optional[Union[str, Path]] = None,
) -> None:
    
    det_model = YOLO(det_model)

    data = Path(data)
    
    if not output_dir:
        output_dir = data.parent / f"{data.stem}_auto_annotate_labels"
    Path(output_dir).mkdir(exist_ok=True, parents=True)

    det_results = det_model(
        data, stream=True, device=device, conf=conf, iou=iou, imgsz=imgsz, max_det=max_det, classes=classes
    )

    
    
    for result in det_results:
        class_ids = result.boxes.cls.int().tolist()  # class indices
        boxes_xyxy = result.boxes.xyxy  # shape: [N, 4] with [x1, y1, x2, y2]
        img_w, img_h = result.orig_shape[1], result.orig_shape[0]  # width, height

        yolo_boxes = []
        # Convert to YOLO format: [class_id, x_center, y_center, width, height] normalized
        for cls_id, box in zip(class_ids, boxes_xyxy):
            x1, y1, x2, y2 = box.tolist()
            x_center = ((x1 + x2) / 2) / img_w
            y_center = ((y1 + y2) / 2) / img_h
            width = (x2 - x1) / img_w
            height = (y2 - y1) / img_h
            yolo_boxes.append(f'{cls_id} {x_center} {y_center} {width} {height}\n')
        
        # if not yolo_boxes: # Does not create .txt file for a photo with "no detections"
        #     continue
            
        with open(f"{Path(output_dir) / Path(result.path).stem}.txt", "w", encoding="utf-8") as f:
            for box in yolo_boxes:
                f.write(box)

# Function to expedite the naming and counting of images by class for a dataset 
def count_images_by_class(class_name:str):
    naming_folder = Path(proj_path)
    numbers = list(range(1, 16))
    class_name = class_name
    for file in naming_folder.iterdir():
        if file.suffix == '.png':
            new_file = file.with_stem(f'{class_name}_{numbers.pop(0)}')
            file.rename(new_file)

# This function generates 5x new images per original for augmentation.
# - Rotates image  90 degrees, 3x
# - Blurs image, 2x

def gen_aug(img_folder_name:str):
    img_folder = Path(f'{proj_path}/{img_folder_name}')
    new_image_folder = f'{proj_path}/{img_folder_name}/aug_photos'

    # Rotates photo 90 degrees, 3x
    def get_aug_rotate(image, file):
        for angle in [90,180,270]:
            new_image = ski.transform.rotate(image,angle=angle, resize=True)
            new_image_uint8 = ski.img_as_ubyte(new_image)  # Converts float64 [0.0, 1.0] to uint8 [0, 255]
            ski.io.imsave(file.stem + str(f'({angle})') + '.png',new_image_uint8)

    # Blurs photo 2x
    def get_aug_gaussian(image, file):
        for sigma in [4,6]:
            new_image = ski.filters.gaussian(image,sigma=sigma, channel_axis=-1)
            new_image = new_image / new_image.max()  # Normalize to [0.0, 1.0]
            new_image_uint8 = ski.img_as_ubyte(new_image)  # Converts float64 [0.0, 1.0] to uint8 [0, 255]
            ski.io.imsave(file.stem + str(f'({sigma})') + '.png',new_image_uint8)
    
    # Iterate through original image folder and generate augmentation photos.
    os.chdir(f'{proj_path}/{img_folder_name}/aug_photos') # Change dir to save images 

    for file in img_folder.iterdir():
        if file.is_file() and file.suffix.lower() == '.png':
            image = ski.io.imread(file)
            get_aug_rotate(image, file)
            get_aug_gaussian(image, file)

    os.chdir(proj_path) # Change dir back to project location
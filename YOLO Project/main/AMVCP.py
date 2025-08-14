# Step 1: Functions generate 5x new photos used for augmenting source photos for dataset.

from pathlib import Path
import skimage as ski


# Rotates photo 3x
def get_aug_rotate(image, file):
    # Add lines to pwd, chdir and then add parameter for target directory.
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


# Function to generate new .txt file for YOLO format
from pathlib import Path
import os

def gen_txt(dataset_type, path):
# dataset_type = 'valid' | 'train' | 'test'
# path = '/Users/snowgtyler/Desktop/validation_photos/'
    
    dataset_folder = Path(path)
    os.chdir(path)
    
    with open(f'{dataset_type}.txt', 'w') as f:
        for file in dataset_folder.iterdir():
            if file.suffix == '.png':
                f.write(f'obj_{dataset_type}_data/' + file.name + '\n')

# Expedited the naming and counting of photos for dataset 
def name_photos_by_cls(path: str, class_name:str):
    naming_folder = Path(path) # i.e. '/Users/snowgtyler/Desktop/validation_photos/new_photos/'
    numbers = list(range(1, 16)) # Consider counting files in directory
    for file in naming_folder.iterdir():
        if file.suffix == '.png':
            new_file = file.with_stem(f'{class_name}_{numbers.pop(0)}')
            file.rename(new_file)
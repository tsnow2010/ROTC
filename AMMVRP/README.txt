README

# General Notes:

# Use this CLI command on Mac to zip folder correctly for CVAT: % zip -r archive_test2.zip test2 -x "*/__MACOSX/*" "*/.DS_Store"

# IDEAS TO IMPROVE MODEL:
# - Use OBB training model: https://docs.ultralytics.com/tasks/obb/
# - Find ways to increase quality of your bounding boxes.  Is the training dataset throwing the model off?  https://sodevelopment.medium.com/top-5-tips-for-training-yolo-mastering-object-detection-with-confidence-463e54b2a7a7
#       https://yolov8architecture.com/how-to-annotate-images-for-yolov8-training/
# - Validation performance is showing signs of overfitting.  Try 10 and 20 epochs and compare.
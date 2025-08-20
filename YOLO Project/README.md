# Advanced Multi-class Military Vehicle Recognition Project (AMMVRP) 

### Purpose: To use Ultralytics YOLOv11 to test the viability of using computer vision (CV) to recognize over 12 classes of military vehicles using bounding boxes.  The project will answer whether accuracy will improve with greater classes and whether computer vision will be able to recognize key features distinguishing military vehicles with different purposes.  
> - Previous work was done by <<name of other developer>> in which only <<4>> classes were classified, but I recognized the usefulness of being able to further discriminate the types of military vehicles.
> - In the current project, all classes have clearly differentiable features, such as small, large cylinders, flat surfaces, tracked or wheeled capability, etc.

### Method: 
#### CV Model and Tools:
> - Ultralytics YOLO v11 for its computer vision modeling capabilities.
> - Computer Vision Annotation Tool (CVAT) (https://www.cvat.ai/)

#### Datasets:
> - Custom training dataset (498 photos) that was manually scrapped from internet and annotated with bounding boxes.
> - Validation dataset was manually scrapped but annotated using Ultralytics auto_annotate().
>   - The actual function was a modified version of the above but with the Segment Augmentation Model (SAM) capability removed, since masking was not necessary.

#### Classification:
#### I attempt to identify military vehicles into (12) different classes:
> - Tank: TNK
> - Armored Personnel Carrier: APC
> - Intercontinental Ballistic Missile: ICBM
> - Infantry Mobility Vehicle: IMV
> - Self-Propelled Howitzer: SPH
> - Multiple Rocket Launcher System: MRLS
> - Short Range Ballistic Missile: SRBM
> - Unmanned Aerial Vehicle Carrier: UAVC
> - Surface-to-Air Missile: SAM
> - Infantry Fighting Vehicle: IFV
> - Cargo Truck: CT
> - Scout Car: SC

#### Results: 

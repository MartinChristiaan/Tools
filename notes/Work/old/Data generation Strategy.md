* Changed tracker script to generate frame based annotations for tharde. 
* Make it reusable for marnehuizen
* Looked up Havendagen -> reprocessed it

Why I did it this way

Mindset
Things will not go well in one go. We will need to be fast and be able to iterate.
A lot of variation is needed, so preferably a large number of datasets.

-
* Loading data from diskstation is too slow - Will slow down experiments

* Loading Copying the data from all the videosets locally would require large file transfers and use up a lot of disk space. Only a small portion of the data is needed usually.

* Initial strategy was to use TYOLO dataloader.  Compatibility with existing TYOLO datasets AOI and VIRAT from Wiliam.

* Data needs to be checked for errors. Datasets such as Singapore, 

* Marnehuizen and CEGR contain errors which need to be removed. 
* Compatibility with YOLO Dataset
* I needed to go through a lot of data to see if the annotations where correct. In the case of tharde, several people wandering around in unannotated sequences. 

## Dataset Pre-processing

#### Introduction
The primary objective of dataset preprocessing was to combine multiple sparsely annotated video datasets into a unified dataset that could offer a diverse array of challenging samples containing moving small objects. The existing datasets primarily provided annotations for large objects, necessitating extensive processing to enable effective training for small object recognition. In order to maintain reasonable training times, we further sought to reduce the demand on hard disk bandwidth by preemptively applying operations such as cropping and resizing. These measures were implemented to optimize the dataset for efficient and effective small object training while managing computational resources effectively. 

#### The Dataset format

The dataset is comprised of several constituent datasets, each further segmented into distinct image sequences. Image format was selected for file representation, as it allows for significantly faster random sampling compared to video files. This dataset was specifically designed to support training utilizing both the YOLO dataloader and the Mediamanager data loader, enabling versatile and efficient data handling during the training process. 

#### Scaling 
  
In many instances, the objects present in video datasets are not of a sufficiently small size to effectively test the model's ability to detect small objects. To address this limitation, we made the decision to resize the images, thereby emulating smaller objects within the Maritime and UAV datasets. In order to maintain the visual fidelity of the data and avoid aliasing artifacts, a gaussian blur is applied to the images prior to the scaling operation, enhancing the realism of the generated data. To minimize the computational burden arising from loading high-resolution images from storage, the downsizing of the data is carried out during the dataset creation process.

#### Cropping and tiling

Tiling is another feature aimed at reducing the overhead of disk transfers. Often large parts of the image do not contain relevant content and can be discarded. To facilitate this process, the high resolution datasets are subdivided into a grid. Subsequently, time instances are selected where objects enter a cell on this grid to produce sequences for the dataset. 

#### IR Normalization
Parts of the data originate from infrared recordings and  are saved in a 16 bit format and need to be converted so that objects become visible. We determine constants for a simple min-max normalization from the first image in the sequence. Afterwards, the rest of the sequence is normalized accordingly.

#### Tracking annotations

Some datasets are annotated sparsely so that annotations are unavailable for certain frames. To maintain the densely annotated format we apply the OPENCV KCF object tracker to the annotations in forward and backward directions. This method provides reliably produces a few seconds worth of extra annotations as long as the objects do not become occluded.

#### Pruning

Many datatsets do not contain annotations for objects other than their target class. So for instance, the data from tharde often contains moving people in their sequences yet fail to provide annotations. As a counter measure, these sequences have to be manually removed from the dataset through visual inspection. Additionally, annotation errors are common in video datasets which makes it paramount to apply some pruning. 

#### Motion models

Global motion may impair the capability of the motion based models to detect small objects. To counteract this, motion compensation and warping can be applied during training to limit the motion to moving objects.  By computing these motion models ahead of time, we can prevent a lot of CPU processing overhead during training. 

#### Dataloader

To account for variations in database sizes and sequence lengths within the dataset, the Dataloader employs a weighted random selection strategy. The computation of these weights ensures an optimal diversity of circumstances during training. Specifically, the weights are designed in a manner that ensures equal occurrence of each database, thus mitigating any bias arising from differences in database sizes. Furthermore, the samples within each database are also weighted to ensure that every sequence within the database is equally represented, contributing to a balanced and unbiased training process.



# Dalia and Arthur
* Discuss possible approaches
	* Single frame (Mask RCNN, Transformer model)
	* TYOLO
	* MOD
* Do we need to have data in a common format. (How can we integrate videoset data)*
* Build more Augmentations
* How to get precise bounding boxes.
	* Segmentation Mask
		* Directly from model
		* Using post-process
			* SAM model?
* How to compare results
	* Standard evaluation procedure?
	* Michel small object script?
* 

# Brainstorm Multiframe Datareader

Hoi allemaal,

Voor L3 Harris gaan we aan de gang met small-object detection.  Een van de uitdagingen van small object detection is dat je graag wilt trainen met meerdere frames omdat de verschillen in frames vaak informatie bevatten die goed van pas komen bij het detecteren van kleine objecten. Maar het trainen van dit soort detectoren vereist een nog grotere hoeveelheid data omdat je voor elk input van je model meerdere frames van een video opname nodig hebt.  Hiervoor willen we graag de grote hoeveelheid videodata die we op de diskstation hebben kunnen toepassen. 

Ik ben zelf voor meerdere projecten (Panoptes en Mantis) bezig met small object detection en daarom ben ik in samenwerking met Jan, Hugo en Jan-Erik bezig geweest om een aantal handige tools op te zetten die we hierbij kunnen gebruiken. 

Zo zijn we bijvoorbeeld bezig om een lezer te maken op basis van de media manager die met behulp van caching er voor zorgt dat de data van de diskstation op een handige manier gebruikt kan worden tijdens training. Daarnaast werk ik ook aan een systeem waarmee we handig transforms kunnen toepassen voor multiframe training. Hoewel Albumentations dit tot een bepaald niveau ondersteund, bied het nog niet de benodigde flexibiliteit voor onze use-case.

Ik zou graag deze brainstorm willen gebruiken hoe we deze functies verder uit kunnen werken en toe kunnen passen in het project.  

Groeten,
Martin









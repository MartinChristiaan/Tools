Hoi Ella,

Leuk dat je wil meewerken aan small object detection. Zoals besproken heb ik hieronder een aantal dingen om alvast mee aan de slag te gaan. 
## Docker omgeving

De eerste stap is om een omgeving te maken waarin je wil werken. Hiervoor heb je een aantal keuzes.

1. Gebruik mijn docker (Zie [docker · dev · intelligent_imaging / python / deep_learning / yolo-plugins · GitLab (tno.nl)](https://gitlab.tsn.tno.nl/intelligent_imaging/python/deep_learning/yolo-plugins/-/tree/dev/docker)) Het idee is dat je hiermee je home directory naar binnen mapt zodat je direct git/ssh kunt gebruiken. Maak voor de zekerheid even een backup van je home directorie als je dit doet.
2. Maak je eigen docker
3. Gebruik je locale omgeving.
Het is handing als je in ieder geval vscode kunt opzetten in de omgeving die je kiest. Als je daar nog meer over zoekt zie [Visual studio code · Wiki · intelligent_imaging / documentation · GitLab (tno.nl)](https://gitlab.tsn.tno.nl/intelligent_imaging/documentation/-/wikis/Visual-studio-code)


## Pytorch

Als je nog niet eerder met Pytorch hebt gewerkt, raad ik je aan om even de Pytorch tutorial te doen [Learning PyTorch with Examples — PyTorch Tutorials 2.1.1+cu121 documentation](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html)

### Pytorch Lightning

Als je je eigen model gaat maken, kan ik je aanraden om Pytorch lightning te gebruiken. Dit versimpeld het trainingsprocess namelijk aanzienlijk door dingen zoals optimizers en logging te regelen. 

* Werp een blik op de BBox toolbox [bboxtoolbox/bboxtoolbox/bbox.py · master · intelligent_imaging / python / Toolboxes · GitLab (tno.nl)](https://gitlab.tsn.tno.nl/intelligent_imaging/python/toolboxes/-/blob/master/bboxtoolbox/bboxtoolbox/bbox.py)
Handig om te weten wat we al beschikbaar hebben om met bboxes te werken. Kijk ook naar de 
[trackertoolbox/trackertoolbox/detections.py · master · intelligent_imaging / python / Toolboxes · GitLab (tno.nl)](https://gitlab.tsn.tno.nl/intelligent_imaging/python/toolboxes/-/blob/master/trackertoolbox/trackertoolbox/detections.py?ref_type=heads)
Ik gebruik de detection class ook vaak in mijn systeem.

## Albumentations
[Albumentations: fast and flexible image augmentations](https://albumentations.ai/)
[Albumentations Demo](https://demo.albumentations.ai/)
Ik gebruik albumentations voor voorverwerking en augmentaties. 

# DLUtils-II

DL utils is mijn package waarmee ik deep learning met behulp van de videosets faciliteer. Ik heb in de yolo-plugins een example.py staan om dit uit te proberen. Je kunt alvast kijken of je dit aan de praat krijgt. 








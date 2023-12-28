* [[DL Tools]]
* Pathlib extension to 
	* Automatically create dir when copying
	* Selecting all leaf directories
* Create application to quickly change folder structures...
	* Analyse folder and understand labels?
	* Structure is
		1. Glob to get all paths
		2. disect path (How to automate?)
			1. Joinsep as path extension?
		3. New filename (easily copy with SPATH?)
	* Not a lot of work but might be easiest to create a python factory for this using chatgpt
* Make it easier to create snippets
	* Made initial script but need te extend it with functionality to copy from the clipboard
* Easier nohup execution tool
	* Goal is to easily manage the processes.
		* Logfile should be the name of the process id
* Generate CSV based on dataclass -> function which takes in a dataclass and generates. 
Function description
* Take in python dataclass + path to csv file
* If csv file does not already exist
	* Generate a csv file with headers from dataclass at a given path if it does not exist yet.
	* print status
	* open the csv using xdg-open

Easy installer to install all tools and extensions into new environment
* argparse runner
* bg_runner
* explorer...
* Run python tool


Control data in dataset
* Filter out some stuff
* CSV filters -> create new csv

* ArgParse runner

 
 * For argparse, save combinations to a CSV file stored locally...
	* create tool which takes in python script and looks at recent usage...
	* how to modify argparse

CSV file reader
* quickly view csv files on the command line
* FZF sorting
* plot quickly using fzf
* colorize items

Hoi Leo,
Afgelopen weken ben ik veel bezig geweest met de DLA voor Mantis en gewerkt aan de ondersteuning voor YOLOv8.
Inmiddels heb ik hierbij wat vooruitgang weten te boeken. 
Ik zou graag dit moment even willen pakken om je bij te praten en te overleggen wat de beste volgende stappen zouden kunnen zijn. 

Groeten,
Martin

* DLA in eerste instantie matig.
* Test gedaan met convoluties van individuele lagen en int8 quantizatie -> Veel betere prestaties bij k=3 en int8 quantizatie. 
* YOLOv8 werkt beter
* Initiele testen lijken erop te wijzen dat quantizatie de prestaties niet al te erg verslechteren. 

Mogelijke volgende stappen
* T2-YOLO quantizeren
* Nieuw model proberen te trainen met V8
	* Handig werk voor andere projecten (mogelijke samenwerking met Panoptes)
* Verslag maken

[[Processing Media Manager]]
[[Click Utils]] 
[[Refactor OS Explorer]]
[[ChatGPT CLI]]
[[Installer for tools]]




# Generic program structure

CSV file With config
(->
Argparse) 
->
Main fun with Dataclass

What we need
* Better ways to edit the csv files (especially when long paths are involved)
* First row as default?
* Flipped editing
* Store Configs -> default in configs folder

### How Should querry work?

* SQL query file?
* Personal pseudocode?
* Python?

DATAFRAME extended?
Easily open config? -> FZF command?
How to select config (argparse -c)

template cli for common program types
### How to be more efficient at communication

Templating system
Routines...


#!/bin/bash
apt install wget -y
SCRIPTS=http://diskstationii1.tsn.tno.nl/webdata/docker/installers
for script in initialize.bash linuxtools.bash python3.bash rda.bash fonts.bash timezone.bash cleanup.bash; do
	wget $SCRIPTS/latest/$script 
	bash -e $script 
	rm $script
done





#!/bin/bash

ssh-copy-id -p 1140 -i ~/.ssh/id_rsa.pub tno@srv.delftdynamics.nl
ssh-copy-id -p 1142 -i ~/.ssh/id_rsa.pub tno@srv.delftdynamics.nl
ssh-copy-id -p 1144 -i ~/.ssh/id_rsa.pub tno@srv.delftdynamics.nl
rsync  -azP -e 'ssh -p 1142'  tno@srv.delftdynamics.nl:/home/tno/data/spear/pipeline/ /data/leeuwenmcv/diskstation/spear/data/TestRuns/20230630_testday5/blue --exclude *IR*
rsync  -azP -e 'ssh -p 1140'  tno@srv.delftdynamics.nl:/home/tno/data/spear/pipeline/ /data/leeuwenmcv/diskstation/spear/data/TestRuns/20230630_testday5/green --exclude *IR*
rsync  -azP -e 'ssh -p 1144'  tno@srv.delftdynamics.nl:/home/tno/data/spear/pipeline/ /data/leeuwenmcv/diskstation/spear/data/TestRuns/20230630_testday5/yellow --exclude *IR*

import os
import glob
import sys

home = os.path.expanduser('~')
program = sys.argv[1]

with open(f'{home}/Tools/QuickOpen/quick_folders','r') as f:
    folders = f.readlines()

combined_dirs = []

for folder in folders:
    folder = folder.replace('\n','')
    #print(folder)
    #print(os.listdir(folder))
    folder = folder+"/*"
    combined_dirs += [x for x in glob.glob(folder) if os.path.isdir(x)]

with open('/tmp/interesting_dirs','w') as f:
    f.write("\n".join(combined_dirs))

cmd= f'{program} $(cat /tmp/interesting_dirs | fzf)'
os.system(cmd)








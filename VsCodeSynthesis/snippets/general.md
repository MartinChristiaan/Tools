# argparse
parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--filename',type=str,default=default)
parser.add_argument('-v', '--verbose',action='store_true')
args = parser.parse_args()

# folder read

${1:folder} = "${2:path}"
for filename in os.listdir(${1:folder}):
    with open(f'{${1:folder}}/{filename}', 'r') as f:
        text = f.read()

# Logger

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# videoshow

vid = cv2.VideoCapture(${1:0})
while(True):
    ret, frame = vid.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()


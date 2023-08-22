import time
import numpy as np
import pickle 
N = 8000
random_array = np.random.random((N,128))
with open('pklout.pkl','wb') as f:
	pickle.dump(random_array,f)

for j in range(N):
	out_arr = random_array[j]
	with open(f'{j}.pkl','wb') as f :
		pickle.dump(out_arr,f)
t0 = time.time()
with open('pklout.pkl','rb') as f:
	# text = f.read()
	t0 = time.time()
	d = pickle.load(f)
t1 = time.time()
print(t1-t0)

for j in range(N):
	with open(f'{j}.pkl','rb') as f :
		pickle.load(f)

t2 = time.time()
print(t2-t1)
	
import random,os
home = os.path.expanduser('~')
with open(f'{home}/notes/small_talk_questions.md','r') as f:
	print(random.choice([x for x in f.readlines() if len(x.replace("\n","")) > 0]))
import os
home = os.path.expanduser('~')
git_dir= f"{home}/git"
git_repos = os.listdir(git_dir)
for repo in git_repos:
	x = os.system(f"cd {git_dir}/{repo} && git status | grep modified")
	if x > 0:
		print(f"{repo} ok")
	else:
		print(f"{repo} has changes")

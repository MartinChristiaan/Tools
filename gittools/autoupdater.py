# service which automatically pulls from git and pushes any changes to git at a fixed interval
# git repos are registered in a config file. Config file is saved in the same directory as the script
# config file is a text file contianing a list of git repos to pull from and push to.

from time import sleep
import loguru
import os
from pathlib import Path
import loguru
import os
from pathlib import Path
import subprocess

INTERVAL_SECONDS = 60 * 10  # 10 minutes


class GitUpdater:
    def __init__(self) -> None:
        self.git_repos = self.read_config()

    def read_config(self):
        git_repos = []
        config_path = Path(os.path.dirname(os.path.abspath(__file__))) / "config.txt"
        with open(config_path, "r") as f:
            for line in f:
                git_repos.append(line.strip())
        return git_repos

    def update_repo(self, path):
        loguru.logger.info(f"updating repo at {path}")
        try:
            subprocess.check_output(
                f"cd {path} && git pull", shell=True, stderr=subprocess.STDOUT
            )
            subprocess.check_output(
                f"cd {path} && git add .", shell=True, stderr=subprocess.STDOUT
            )
            subprocess.check_output(
                f'cd {path} && git commit -m "auto commit"',
                shell=True,
                stderr=subprocess.STDOUT,
            )
            subprocess.check_output(
                f"cd {path} && git push", shell=True, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            loguru.logger.error(
                f"Failed to execute command in {path}. Error: {e.output.decode()}"
            )

    def __call__(self):
        while True:
            for repo in self.git_repos:
                self.update_repo(repo)
            sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    GitUpdater()()

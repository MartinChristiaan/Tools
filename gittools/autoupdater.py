# service which automatically pulls from git and pushes any changes to git at a fixed interval
# git repos are registered in a config file. Config file is saved in the same directory as the script
# config file is a text file contianing a list of git repos to pull from and push to.

import os
import subprocess
from pathlib import Path
from time import sleep

INTERVAL_SECONDS = 60 * 10  # 10 minutes

from loguru import logger

# add file handler for logger
home = os.path.expanduser("~")
logger.add(
    f"{home}/tool_updater_log.txt",
    rotation="1 week",
    retention="10 days",
    level="INFO",
    format="{time} {level} {message}",
)


class GitUpdater:
    def __init__(self) -> None:
        self.git_repos_auto = self.read_config()
        self.git_repos_pull_only = Path(home).glob("*")

    def read_config(self):
        git_repos = []
        config_path = Path(os.path.dirname(os.path.abspath(__file__))) / "config.txt"
        with open(config_path, "r") as f:
            for line in f:
                git_repos.append(line.strip())

        return git_repos

    def update_repo(self, path):
        logger.info(f"updating repo at {path}")
        try:
            subprocess.check_output(
                f"cd {path} && git pull", shell=True, stderr=subprocess.STDOUT
            )
            subprocess.check_output(
                f"cd {path} && git add .", shell=True, stderr=subprocess.STDOUT
            )
            subprocess.check_output(
                f'cd {path} && git commit -am "auto commit"',
                shell=True,
                stderr=subprocess.STDOUT,
            )

            subprocess.check_output(
                f'cd {path} && git commit -am "auto commit"',
                shell=True,
                stderr=subprocess.STDOUT,
            )
            subprocess.check_output(
                f"cd {path} && git push", shell=True, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Failed to execute command in {path}. Error: {e.output.decode()}"
            )

    def __call__(self):
        while True:
            had_error = False
            for repo in self.git_repos_auto:
                error = self.update_repo(repo)
                if error:
                    had_error = True
            if not had_error:
                logger.info("Succesfully updated all repos")
            else:
                logger.info("Failed to  update")
            for repo in self.git_repos_pull_only:
                logger.info(f"pulling {repo}")
                os.system(f"cd {repo} && git pull")
            sleep(INTERVAL_SECONDS)


sleep(5)
if __name__ == "__main__":
    GitUpdater()()

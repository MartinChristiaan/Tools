import argparse
import os
import subprocess
import sys

import click
import git
import yaml
from loguru import logger
from termcolor import colored

# GIt cli tool to sync local and remote repositories. Git repositories can be registered in a yaml conifg file using the commandline tool.
# Using another command, all registered repositories can be pulled, commits can be made and pushed to the remote repository.
# The config file is located in the home directory of the user and is named .gitsync.yml
# The yaml file should specify the path to the local repository and wether it is active or not. It can be activated using the cli tool.


HOME = os.path.expanduser("~")
CONFIG_FILE = os.path.join(HOME, ".gitsync.yml")

# Argument parser
parser = argparse.ArgumentParser(
    description="Sync your local git repositories with the remote"
)
parser.add_argument(
    "-a",
    "--add",
    dest="add",
    action="store_true",
    help="Add a repository to the config file",
)
parser.add_argument(
    "-ac",
    "--activate",
    dest="activate",
    action="store_true",
    help="Activate a repository in the config file",
)
parser.add_argument(
    "-l",
    "--list",
    dest="list",
    action="store_true",
    help="List all repositories in the config file",
)
parser.add_argument(
    "-r",
    "--remove",
    dest="remove",
    action="store_true",
    help="Remove a repository from the config file",
)
parser.add_argument(
    "-s",
    "--sync",
    dest="sync",
    action="store_true",
    help="Sync all repositories in the config file",
)
parser.add_argument(
    "-se",
    "--search",
    dest="search",
    action="store_true",
    help="Search for a repository in the config file",
)


# implementation of the add command
def add_repo(repo_path):
    logger.info(f"Adding repository {repo_path}")
    # Check if the path exists
    if not os.path.exists(repo_path):
        logger.error(f"Path {repo_path} does not exist")
        sys.exit(1)
    # Check if the path is a git repository
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        logger.error(f"Path {repo_path} is not a git repository")
        sys.exit(1)
    # Check if the repository is already registered
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        if repo_path in config["repos"]:
            logger.error(f"Repository {repo_path} is already registered")
            sys.exit(1)
    # Add the repository to the config file
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        config["repos"].append({"path": repo_path, "active": True})
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f)
    else:
        config = {}
        config["repos"] = []
        config["repos"].append({"path": repo_path, "active": True})
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f)


# implementation of the activate command


def activate_repo(repo_path):
    logger.info(f"Activating repository {repo_path}")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        for repo in config["repos"]:
            if repo["path"] == repo_path:
                repo["active"] = True
                with open(CONFIG_FILE, "w") as f:
                    yaml.dump(config, f)
                return
        logger.error(f"Repository {repo_path} is not registered")
        sys.exit(1)
    else:
        logger.error("No repositories registered")
        sys.exit(1)


# implementation of the list command


def list_repos():
    logger.info("Listing all registered repositories")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        for repo in config["repos"]:
            repo_path = repo["path"]
            active = repo["active"]
            sync_available = False

            # Check if the path exists
            if not os.path.exists(repo_path):
                logger.error(f"Path {repo_path} does not exist")
                sys.exit(1)

            # Check if the path is a git repository
            if not os.path.isdir(os.path.join(repo_path, ".git")):
                logger.error(f"Path {repo_path} is not a git repository")
                sys.exit(1)

            # Check if sync is available
            repo = git.Repo(repo_path)
            if repo.is_dirty(untracked_files=True) or repo.untracked_files:
                sync_available = True

            def print_repo_info(repo_path, active, sync_available):
                path_color = "white" if os.path.exists(repo_path) else "red"
                active_color = "green" if active else "red"
                updates_color = "yellow" if sync_available else "green"

                path_text = colored(f"Path: {repo_path}", path_color)
                active_text = colored(f"Active: {active}", active_color)
                updates_text = colored(
                    f"Sync available: {sync_available}", updates_color
                )

                print(f"{path_text}, {active_text}, {updates_text}")

            # Usage:
            print_repo_info(repo_path, active, sync_available)

    else:
        logger.error("No repositories registered")
        sys.exit(1)


# implementation of the remove command


def remove_repo(repo_path):
    logger.info(f"Removing repository {repo_path}")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        if repo_path in config["repos"]:
            config["repos"].remove(repo_path)
            with open(CONFIG_FILE, "w") as f:
                yaml.dump(config, f)
        else:
            logger.error(f"Repository {repo_path} is not registered")
            sys.exit(1)
    else:
        logger.error("No repositories registered")
        sys.exit(1)


# implementation of the sync command
def sync_repos():
    logger.info("Syncing all repositories")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        for repo in config["repos"]:
            if repo["active"]:
                os.chdir(repo["path"])
                logger.info(f"Syncing repository {repo['path']}")
                try:
                    subprocess.run(["git", "pull"], check=True)
                    subprocess.run(["git", "status"])
                    click.echo("Do you want to add all changes? (y/n)")
                    user_input = click.getchar()

                    click.echo("Do you want to change the commit message? (y/n)")
                    commit_message = (
                        input("Add commit message : ")
                        if click.getchar() == "y"
                        else "Sync"
                    )

                    if user_input.lower() == "y":
                        subprocess.run(["git", "add", "."])
                        subprocess.run(["git", "commit", "-m", f"{commit_message}"])
                        subprocess.run(["git", "push"])
                    else:
                        logger.info("Skipping git add")
                except subprocess.CalledProcessError:
                    logger.error(
                        f"Error occurred while syncing repository {repo['path']}"
                    )
    else:
        logger.error("No repositories registered")
        sys.exit(1)


# parse args and execute the add command
args = parser.parse_args()
if args.add:
    add_repo(os.getcwd())
if args.list:
    list_repos()
if args.remove:
    remove_repo(os.getcwd())
if args.activate:
    activate_repo(os.getcwd())
if args.sync:
    sync_repos()

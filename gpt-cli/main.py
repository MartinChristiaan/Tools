import os
import re
import sys
from pathlib import Path

import click
import openai
import yaml
from key import key
from pyperclip import copy, paste

from utils.charmenu import charmenu

home = os.path.expanduser("~")


class GPTCLI:
    def __init__(self) -> None:
        pass

    def create_function(self):
        template = "Create a python function to "
        functionality = input(template)
        question = template + functionality + ". Do not include an explanation"
        self.request_code(question)

    def request_code(self, question):
        openai.api_key = key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python code generation assistant.",
                },
                {"role": "user", "content": question},
            ],
        )
        result = response["choices"][0]["message"]["content"]
        python_code = re.search(r"```python(.*?)```", result, re.DOTALL)
        if python_code:
            extracted_code = python_code.group(1).strip()
            print(extracted_code)
            copy(extracted_code)
            return extracted_code
        else:
            print("No Python code found.")

    def modify_function(self):
        code = paste()
        text = f"{code} \n Modify to "
        modification = input(text)
        if len(modification):
            self.request_code(modification)

    def create_test(self):
        code = paste()
        print(code + "\n continue? (y/.)")
        if not click.getchar() == "y":
            return
        question = "create a test for the function below \n" + code
        self.request_code(question)

    def create_examples(self):
        code = paste()
        print(code + "\n continue? (y/.)")
        if not click.getchar() == "y":
            return
        question = "create a few brief examples for the code below \n" + code
        code = self.request_code(question)
        example_db = Path(f"{home}/git/tools/gpt-cli/example-db.yaml")
        examples = {}
        if example_db.exists():
            with open(example_db) as f:
                examples = yaml.load(f, yaml.SafeLoader)
        name = input("example_name : ")
        examples[name] = code
        with open(example_db, "w") as yaml_file:
            yaml.dump(examples, yaml_file)

    def __call__(self):
        while True:
            actions = {
                "q": sys.exit,
                "f": self.create_function,
                "t": self.create_test,
                "m": self.modify_function,
                "e": self.create_examples,
            }

            charmenu(actions)


if __name__ == "__main__":
    cli = GPTCLI()
    cli()

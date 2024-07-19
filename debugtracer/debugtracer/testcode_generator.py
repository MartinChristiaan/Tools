import os
from pathlib import Path
import pickle
from debugtracer.function_data import FunctionData

base_code = """
import pickle
import pandas as pd
from debugtracer.function_data import FunctionData
"""

method_call_template = """
    obj = function_data.args[0]
    rem_args = function_data.args[1:]
    result = obj.{name}(*rem_args, **function_data.kwargs)
"""

fn_call_template = """
    result = {name}(*function_data.args, **function_data.kwargs)
"""

auto_docstring_template = """
    \"\"\"
    Tests if {name}({args},**{kwargs}) == {result}
    \"\"\""""
docstring_template = """
    \"\"\"
    {description}
    \"\"\"
"""
test_template = """
from {module} import *
def test_{testname}():
    {docstring}
    function_data = pickle.load(open("{data_path}", "rb"))
    {fn_call}
    if type(result) == pd.DataFrame:
        function_data.result = function_data.result.reset_index(drop=True, inplace=True)
    assert result == function_data.result
"""


class TestGenerator:
    def __init__(self) -> None:
        self.test_dir = Path("./tests")
        self.test_data_dir = Path("/data/testdata/")

    def generate_test_from_function_data(
        self,
        testname,
        description,
        fndata: FunctionData,
    ):

        if fndata.is_method:
            fn_call = method_call_template.format(name=fndata.name)
        else:
            fn_call = fn_call_template.format(name=fndata.name)
        if description == "auto":
            docstring = auto_docstring_template.format(
                args=fndata.args,
                kwargs=fndata.kwargs,
                result=fndata.result,
                name=fndata.name,
            )
        else:
            docstring = docstring_template.format(description=description)

        test_data_path = self.test_data_dir / fndata.name / (testname + ".pkl")
        test_data_path.parent.mkdir(exist_ok=True, parents=True)
        with open(test_data_path, "wb") as f:
            pickle.dump(fndata, f)

        test_code = test_template.format(
            module=fndata.module,
            testname=testname,
            docstring=docstring,
            data_path=test_data_path,
            fn_call=fn_call,
        )
        test_file = self.get_test_file(fndata.name)
        with open(test_file, "a") as f:
            f.write(test_code)

    def get_test_file(self, name):
        test_file = Path(self.test_dir) / f"test_{name}.py"
        if test_file.exists():
            return test_file
        test_file.parent.mkdir(parents=True, exist_ok=True)
        with open(test_file, "w") as f:
            f.write(base_code)
        os.system(f"touch {self.test_dir}/__init__.py")
        return test_file

from pathlib import Path
from pydoc import doc

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
	\"\"\"

"""
docstring_template = """
	\"\"\"
	{description}
	\"\"\"
"""
test_template = """
from {module} import *
def {testname}():
	{docstring}
	function_data = pickle.load(open("{input_data_path}", "rb"))

	{fn_call}
	if type(result) == pd.DataFrame:
		function_data.result = function_data.result.reset_index(drop=True, inplace=True)
	assert result == function_data.result
"""


class TestGenerator:
    def __init__(self) -> None:
        self.test_dir = Path("./tests")

    def generate_test_from_function_data(
        self,
        name,
        module,
        is_method,
        testname,
        args,
        kwargs,
        result,
        input_data_path,
        description="auto",
    ):
        if is_method:
            fn_call = method_call_template.format(name=name)
        else:
            fn_call = fn_call_template.format(name=name)
        if description == "auto":
            docstring = auto_docstring_template.format(
                args=args, kwargs=kwargs, result=result
            )
        else:
            docstring = docstring_template.format(description=description)

        test_code = test_template.format(
            module=module,
            testname=testname,
            docstring=docstring,
            input_data_path=input_data_path,
            fn_call=fn_call,
        )
        test_file = self.get_test_file(name)
        with open(test_file, "a") as f:
            f.write(test_code)

    def get_test_file(self, name):
        test_file = Path(self.test_dir) / f"test_{name}.py"
        if test_file.exists():
            return test_file
        test_file.parent.mkdir(parents=True, exist_ok=True)
        base_code = f"""
import pickle
import pandas as pd
		"""
        with open(test_file, "w") as f:
            f.write(base_code)
        return test_file

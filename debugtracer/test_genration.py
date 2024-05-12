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
    def _generate_test_from_function_data(
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

        return test_template.format(
            module=module,
            testname=testname,
            docstring=docstring,
            input_data_path=input_data_path,
            fn_call=fn_call,
        )

    def generate(self):
        test_file = Path(self.test_code_dir) / f"test_{self.name}.py"
        test_file.parent.mkdir(parents=True, exist_ok=True)

        python_code = f"""
import pickle
import pandas as pd
		"""

        for i, function_data in enumerate(exec_data[self.name]):
            try:
                pickle.dump(function_data, open(self.test_data_dir / f"{i}.pkl", "wb"))
                python_code += self._generate_test_from_function_data(function_data, i)
            except Exception as e:
                logger.error(f"failed at {function_data.name}")
                logger.error(str(e))

        with open(test_file, "w") as f:
            f.write(python_code)

        # logger.info(
        #     f"Generated tests in {test_file}$, test data in {test_data_file} with size {test_data_file.stat().st_size//1024} kbytes"
        # )

import pickle
import pandas as pd

from library.sub_library import *
from debugtracer.function_data import FunctionData


def test_generated_test():
    """
    Tests if my_sum([2, 3],**{'mode': 'test'}) == 7
    """
    function_data = pickle.load(open("/data/testdata/my_sum/generated_test.pkl", "rb"))

    result = my_sum(*function_data.args, **function_data.kwargs)

    if type(result) == pd.DataFrame:
        function_data.result = function_data.result.reset_index(drop=True, inplace=True)
    assert result == function_data.result

from library.sub_library import *
def test_another_test():
    
    """
    custom_description
    """

    function_data = pickle.load(open("/data/testdata/my_sum/another_test.pkl", "rb"))
    
    result = my_sum(*function_data.args, **function_data.kwargs)

    if type(result) == pd.DataFrame:
        function_data.result = function_data.result.reset_index(drop=True, inplace=True)
    assert result == function_data.result

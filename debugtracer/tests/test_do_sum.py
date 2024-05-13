
import pickle
import pandas as pd
		
from library.sub_library import *
def test_example():
    
    """
    Tests if do_sum([ObjectExample(a=6, b=8)],**{'mode': 'eval'}) == 16
    """
    function_data = pickle.load(open("/data/testdata/do_sum/example.pkl", "rb"))
    
    obj = function_data.args[0]
    rem_args = function_data.args[1:]
    result = obj.do_sum(*rem_args, **function_data.kwargs)

    if type(result) == pd.DataFrame:
        function_data.result = function_data.result.reset_index(drop=True, inplace=True)
    assert result == function_data.result

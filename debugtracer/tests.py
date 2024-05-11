
import pickle
exec_data = pickle.load(open("/data/testdata/main.pkl", "rb"))
        
from library.sub_library import * 
def test_my_sum_0():
    function_data = exec_data[0]
    result = my_sum(*function_data.args, **function_data.kwargs)
    assert result == function_data.result
            
from library.sub_library import * 
def test_do_sum_1():
    function_data = exec_data[1]
    obj = function_data.args[0]
    rem_args = function_data.args[1:]
    result = obj.do_sum(*rem_args, **function_data.kwargs)
    assert result == function_data.result
            
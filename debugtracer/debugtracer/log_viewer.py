# streamlit app
# select functions using selectbox
# automatically show IO
import pickle
import streamlit as st
from pathlib import Path

path = st.text_input("path", "/data/trace_data")

scripts = list(Path(path).glob("*"))
script = st.selectbox("script", [x.stem for x in scripts])
script_path = [x for x in scripts if script == x.stem][0]

functions = list(script_path.glob("*"))
function = st.selectbox("function", [x.stem for x in functions])
function_path = [x for x in functions if function == x.stem][0]
iteration = st.number_input("iteration", min_value=0, value=0)


for io in ["input", "output"]:
    # input_path = f"{function_path}/{iteration}_input.pkl"
    io_path = f"{function_path}/{iteration}_{io}.pkl"
    with open(io_path, "rb") as f:
        io = pickle.load(f)
    for k, v in io.items():
        vtype = type(v)
        if vtype in [str, float, int, bool]:
            st.write(f"{k} = {v}")

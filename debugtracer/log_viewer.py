# streamlit app
# select functions using selectbox
# automatically show IO
import streamlit as st
from pathlib import Path

path = st.text_input("path", "/data/trace_data")
functions = list(Path(path).glob("*"))
function = st.selectbox("function", [x.stem for x in functions])
function_path = [x for x in functions if function == x.stem][0]
iteration = st.number_input("iteration", min=0, value=0)

input = list(function_path.glob(f"{iteration}-"))

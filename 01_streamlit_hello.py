import numpy as np
import streamlit as st

st.set_page_config(page_title="Streamlit Hello")

if "run_count" not in st.session_state:
    st.session_state.run_count = 0
st.session_state.run_count += 1

st.title("Streamlit Hello Demo")
st.caption("Every widget interaction reruns this script from top to bottom.")

value = st.slider("Number", min_value=0, max_value=100, value=25, step=1)
random_value = int(np.random.default_rng().integers(0, 1000))

left, middle, right = st.columns(3)
left.metric("Selected", value)
middle.metric("Square", value**2)
right.metric("Run", st.session_state.run_count)

st.info(f"Random sample for this run: {random_value}")

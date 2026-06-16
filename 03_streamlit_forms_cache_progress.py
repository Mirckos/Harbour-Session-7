import time

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cache + Progress")
st.title("Cache + Smart Progress Bar")


@st.cache_data(show_spinner=False)
def heavy_computation(n: int) -> np.ndarray:
    time.sleep(1.5)
    return np.square(np.arange(n))


with st.form("params"):
    n = st.number_input("Number of squares", 100, 10_000, 1_000, 100)
    run = st.form_submit_button("Run")

if run:
    status = st.status("Request accepted", expanded=True)
    status.write("Checking cache or computing the result.")
    tic = time.perf_counter()
    data = heavy_computation(int(n))
    elapsed = time.perf_counter() - tic

    if elapsed < 0.2:
        status.update(label=f"Cache hit in {elapsed:.2f}s", state="complete")
    else:
        status.write("Cold run finished; rendering a small preview.")
        bar = st.progress(0, text="Preparing preview")
        for value in range(0, 101, 5):
            time.sleep(0.02)
            bar.progress(value, text="Preparing preview")
        bar.empty()
        status.update(label=f"Cold run finished in {elapsed:.2f}s", state="complete")

    st.metric("Latency", f"{elapsed:.2f}s")
    st.dataframe(
        pd.DataFrame({"i": np.arange(10), "i_squared": data[:10]}),
        hide_index=True,
        use_container_width=True,
    )

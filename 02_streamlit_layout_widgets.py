import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Editable Table", layout="wide")
st.title("Editable Table + Multiplier")


def make_initial_frame() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    return pd.DataFrame({"A": np.arange(1, 11), "B": rng.normal(size=10).round(3)})


if "df" not in st.session_state:
    st.session_state.df = make_initial_frame()

with st.sidebar:
    multiplier = st.number_input("Multiplier", min_value=1, max_value=10, value=2)

editable_df = st.session_state.df.copy()
editable_df["B * k"] = editable_df["B"] * multiplier

edited_df = st.data_editor(
    editable_df,
    column_config={
        "A": st.column_config.NumberColumn("A", min_value=1, step=1),
        "B": st.column_config.NumberColumn("B", format="%.3f"),
        "B * k": st.column_config.NumberColumn("B * k", format="%.3f"),
    },
    disabled=["B * k"],
    hide_index=True,
    num_rows="dynamic",
    key="editable_table",
    use_container_width=True,
)

base_df = edited_df[["A", "B"]].copy()
base_df["A"] = pd.to_numeric(base_df["A"], errors="coerce")
base_df["B"] = pd.to_numeric(base_df["B"], errors="coerce")
base_df = base_df.dropna().sort_values("A").reset_index(drop=True)

st.session_state.df = base_df

with st.sidebar:
    st.metric("Rows", len(base_df))
    mean_b = base_df["B"].mean()
    st.metric("Mean B", f"{mean_b:.2f}" if pd.notna(mean_b) else "n/a")

chart_tab, data_tab = st.tabs(["Chart", "Clean Data"])

with chart_tab:
    st.subheader("B * k Line")
    if base_df.empty:
        st.warning("Add at least one numeric row to draw the chart.")
    else:
        st.line_chart(base_df.set_index("A")["B"] * multiplier)

with data_tab:
    st.dataframe(base_df, hide_index=True, use_container_width=True)

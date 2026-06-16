import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mini Dashboard", layout="wide")
st.title("Mini Dashboard: Map + Filters")


@st.cache_data
def load_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "city": [f"City {i}" for i in range(200)],
            "lat": rng.uniform(40, 60, 200),
            "lon": rng.uniform(-5, 15, 200),
            "value": rng.integers(0, 101, 200),
            "segment": rng.choice(["baseline", "candidate", "holdout"], 200),
        }
    )


df = load_data()

with st.sidebar:
    st.header("Filters")
    v_min, v_max = st.slider("Value range", 0, 100, (20, 80))
    filtered_pool = df[df["value"].between(v_min, v_max)].copy()

    if filtered_pool.empty:
        sample = 0
        st.warning("No rows match the current range.")
    else:
        sample = st.number_input(
            "Sample size",
            min_value=1,
            max_value=len(filtered_pool),
            value=min(50, len(filtered_pool)),
        )

    show_table = st.checkbox("Show table", True)

if sample:
    filtered = filtered_pool.sample(n=int(sample), random_state=7)
else:
    filtered = filtered_pool

left, middle, right = st.columns(3)
left.metric("Rows", len(filtered))
middle.metric("Mean value", f"{filtered['value'].mean():.1f}" if not filtered.empty else "n/a")
right.metric("Max value", int(filtered["value"].max()) if not filtered.empty else "n/a")

map_tab, data_tab = st.tabs(["Map", "Data"])

with map_tab:
    st.subheader("Distribution Map")
    if filtered.empty:
        st.info("Relax the filter to display points.")
    else:
        st.map(filtered[["lat", "lon"]])

with data_tab:
    if show_table:
        st.dataframe(
            filtered.sort_values("value", ascending=False),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Enable the table in the sidebar to inspect rows.")

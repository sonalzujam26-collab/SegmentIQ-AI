import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui import load_css, sidebar_branding

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="PCA Visualization | SegmentIQ AI",
    page_icon="🧠",
    layout="wide"
)

load_css()
sidebar_branding()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

file_path = "data/processed/customer_segments_pca.csv"

df = pd.read_csv(file_path)

df["Cluster"] = df["Cluster"].astype(str)


# ---------------------------------------------------------
# SEGMENT NAMES
# ---------------------------------------------------------

segment_names = {
    "0": "Occasional / Low-Value",
    "1": "Loyal / High-Value"
}

df["Segment"] = df["Cluster"].map(segment_names)


# ---------------------------------------------------------
# PCA INFORMATION
# ---------------------------------------------------------

pc1_variance = 67.81
pc2_variance = 15.99
total_variance = 83.80


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("🧠 PCA Visualization")

st.write(
    "Principal Component Analysis (PCA) reduces the customer "
    "features into two dimensions so that the customer segments "
    "can be visualized on a 2D chart."
)

st.divider()


# ---------------------------------------------------------
# PCA METRICS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "PC1 Variance",
        f"{pc1_variance:.2f}%"
    )

with col2:

    st.metric(
        "PC2 Variance",
        f"{pc2_variance:.2f}%"
    )

with col3:

    st.metric(
        "Total Variance",
        f"{total_variance:.2f}%"
    )


st.divider()


# ---------------------------------------------------------
# SEGMENT FILTER
# ---------------------------------------------------------

st.header("🎯 Explore Customer Segments")

selected_segments = st.multiselect(
    "Select segments to display",
    options=list(segment_names.values()),
    default=list(segment_names.values())
)

filtered_df = df[
    df["Segment"].isin(selected_segments)
]


# ---------------------------------------------------------
# PCA SCATTER PLOT
# ---------------------------------------------------------

st.header("📍 Customer Segments in PCA Space")

fig = px.scatter(
    filtered_df,
    x="PC1",
    y="PC2",
    color="Segment",
    hover_data={
        "Customer ID": True,
        "Segment": True,
        "Recency": ":.2f",
        "Frequency": ":.2f",
        "Monetary": ":.2f",
        "TotalQuantity": ":.2f",
        "UniqueProducts": ":.2f",
        "AverageOrderValue": ":.2f",
        "PC1": ":.3f",
        "PC2": ":.3f"
    },
    title="Customer Segmentation Using PCA"
)

fig.update_traces(
    marker=dict(
        size=7,
        opacity=0.65
    )
)

fig.update_layout(
    height=700,
    xaxis_title="Principal Component 1",
    yaxis_title="Principal Component 2",
    legend_title="Customer Segment",
    hovermode="closest"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------

st.divider()

st.header("🔎 How to Read This Visualization")

st.write(
    """
Each point represents one customer.

Customers that appear closer together have more similar patterns
across the features used for segmentation.

The colors represent the customer segments identified by the
K-Means clustering algorithm.

PCA does not create the customer segments. It is used here only
to reduce the six customer features into two principal components
for easier visualization.
"""
)


# ---------------------------------------------------------
# PCA SUMMARY
# ---------------------------------------------------------

st.info(
    f"""
**PCA Summary**

PC1 explains **{pc1_variance:.2f}%** of the variance in the data.

PC2 explains **{pc2_variance:.2f}%** of the variance.

Together, PC1 and PC2 explain **{total_variance:.2f}%** of the
total variance, allowing a large portion of the customer behavior
to be visualized in two dimensions.
"""
)


# ---------------------------------------------------------
# CUSTOMER COUNT
# ---------------------------------------------------------

st.divider()

st.caption(
    f"Customers currently visualized: {len(filtered_df):,}"
)

st.caption(
    "SegmentIQ AI | PCA Customer Visualization"
)
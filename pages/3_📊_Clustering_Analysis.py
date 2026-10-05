import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui import load_css, sidebar_branding

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Clustering Analysis | SegmentIQ AI",
    page_icon="📊",
    layout="wide"
)

load_css()
sidebar_branding()

# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("📊 Clustering Analysis")

st.write(
    "Analyze how K-Means clustering was evaluated and understand "
    "why K = 2 was selected for customer segmentation."
)

st.divider()


# ---------------------------------------------------------
# CLUSTERING RESULTS
# ---------------------------------------------------------

results = pd.DataFrame({
    "K": [2, 3, 4, 5, 6, 7, 8, 9, 10],

    "Inertia": [
        19866.14,
        15537.60,
        13578.41,
        12116.06,
        11017.81,
        10230.40,
        9585.01,
        9015.80,
        8568.70
    ],

    "Silhouette Score": [
        0.3643,
        0.2762,
        0.2326,
        0.2351,
        0.2222,
        0.2185,
        0.2141,
        0.2127,
        0.2022
    ]
})


# ---------------------------------------------------------
# KEY METRICS
# ---------------------------------------------------------

best_k = 2
best_silhouette = 0.3643

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🏆 Selected K",
        best_k
    )

with col2:

    st.metric(
        "📐 Best Silhouette Score",
        f"{best_silhouette:.4f}"
    )

with col3:

    st.metric(
        "🔎 Tested K Values",
        "2 – 10"
    )


st.divider()


# ---------------------------------------------------------
# ELBOW METHOD
# ---------------------------------------------------------

st.header("📈 Elbow Method")

st.write(
    "The Elbow Method compares the clustering inertia for different "
    "values of K. A lower inertia means that customers are closer to "
    "their assigned cluster centers."
)

fig_elbow = px.line(
    results,
    x="K",
    y="Inertia",
    markers=True,
    title="Elbow Method — K vs Inertia"
)

fig_elbow.update_layout(
    height=500,
    xaxis_title="Number of Clusters (K)",
    yaxis_title="Inertia"
)

st.plotly_chart(
    fig_elbow,
    use_container_width=True
)


# ---------------------------------------------------------
# SILHOUETTE SCORE
# ---------------------------------------------------------

st.header("📊 Silhouette Score")

st.write(
    "The Silhouette Score measures how well customers fit within "
    "their assigned cluster compared with other clusters. A higher "
    "score indicates better separation among the clusters."
)

fig_silhouette = px.line(
    results,
    x="K",
    y="Silhouette Score",
    markers=True,
    title="Silhouette Score for Different K Values"
)

fig_silhouette.update_layout(
    height=500,
    xaxis_title="Number of Clusters (K)",
    yaxis_title="Silhouette Score"
)

st.plotly_chart(
    fig_silhouette,
    use_container_width=True
)


# ---------------------------------------------------------
# RESULTS TABLE
# ---------------------------------------------------------

st.header("📋 Clustering Evaluation Results")

display_results = results.copy()

display_results["Inertia"] = display_results[
    "Inertia"
].round(2)

display_results["Silhouette Score"] = display_results[
    "Silhouette Score"
].round(4)

st.dataframe(
    display_results,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# K = 2 EXPLANATION
# ---------------------------------------------------------

st.divider()

st.header("🏆 Why Was K = 2 Selected?")

st.success(
    """
K = 2 was selected because it achieved the highest Silhouette Score
among the tested values from K = 2 to K = 10.

The Silhouette Score for K = 2 was **0.3643**, which was higher than
the scores obtained for the other tested K values.

The resulting two customer groups also provide a simple and
business-friendly segmentation:

**Segment 0 — Occasional / Low-Value Customers**

These customers generally have fewer orders, lower spending, and
longer time since their last purchase.

**Segment 1 — Loyal / High-Value Customers**

These customers generally have more orders, higher spending,
more product variety, and more recent purchasing activity.
"""
)


# ---------------------------------------------------------
# IMPORTANT NOTE
# ---------------------------------------------------------

st.info(
    "K = 2 is the strongest quantitative choice among the tested "
    "values for this particular dataset, feature set, and preprocessing."
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "SegmentIQ AI | K-Means Clustering Analysis"
)
import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui import load_css, sidebar_branding

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SegmentIQ AI",
    page_icon="🧩",
    layout="wide"
)

load_css()
sidebar_branding()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

customer_file = "data/processed/customer_features.csv"
segment_file = "data/processed/customer_segments.csv"

customers = pd.read_csv(customer_file)
segments = pd.read_csv(segment_file)

segments = segments[["Customer ID", "Cluster"]]

df = customers.merge(
    segments,
    on="Customer ID",
    how="inner"
)


# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------

st.title("🧩 SegmentIQ AI")

st.subheader("Customer Segmentation & Business Intelligence Dashboard")

st.write(
    "SegmentIQ AI uses customer purchasing behavior to identify "
    "different customer segments and generate useful business insights."
)


# ---------------------------------------------------------
# KEY METRICS
# ---------------------------------------------------------

total_customers = len(df)
total_segments = df["Cluster"].nunique()
average_spending = df["Monetary"].mean()
average_orders = df["Frequency"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "🧩 Customer Segments",
        total_segments
    )

with col3:
    st.metric(
        "💰 Avg. Customer Spending",
        f"£{average_spending:,.2f}"
    )

with col4:
    st.metric(
        "🛒 Avg. Orders",
        f"{average_orders:.2f}"
    )


# ---------------------------------------------------------
# SEGMENT SUMMARY
# ---------------------------------------------------------

st.divider()

st.header("📊 Customer Segment Overview")

segment_summary = (
    df.groupby("Cluster")
    .agg(
        Customers=("Customer ID", "count"),
        Average_Spending=("Monetary", "mean"),
        Average_Orders=("Frequency", "mean"),
        Average_Recency=("Recency", "mean")
    )
    .reset_index()
)

segment_summary["Segment"] = segment_summary["Cluster"].map({
    0: "Occasional / Low-Value",
    1: "Loyal / High-Value"
})


# ---------------------------------------------------------
# SEGMENT DISTRIBUTION CHART
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        segment_summary,
        values="Customers",
        names="Segment",
        title="Customer Distribution by Segment",
        hole=0.45
    )

    fig.update_layout(
        height=450,
        legend_title="Customer Segment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# SEGMENT SPENDING CHART
# ---------------------------------------------------------

with col2:

    fig = px.bar(
        segment_summary,
        x="Segment",
        y="Average_Spending",
        title="Average Customer Spending",
        text_auto=".2f"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Customer Segment",
        yaxis_title="Average Spending"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# SEGMENT TABLE
# ---------------------------------------------------------

st.header("📋 Segment Performance")

display_table = segment_summary[
    [
        "Segment",
        "Customers",
        "Average_Spending",
        "Average_Orders",
        "Average_Recency"
    ]
].copy()

display_table.columns = [
    "Customer Segment",
    "Customers",
    "Average Spending",
    "Average Orders",
    "Average Recency (Days)"
]

display_table["Average Spending"] = display_table[
    "Average Spending"
].round(2)

display_table["Average Orders"] = display_table[
    "Average Orders"
].round(2)

display_table["Average Recency (Days)"] = display_table[
    "Average Recency (Days)"
].round(2)

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# BUSINESS SUMMARY
# ---------------------------------------------------------

st.divider()

st.header("💡 Business Summary")

st.info(
    """
SegmentIQ AI identifies two major customer groups.

**Occasional / Low-Value Customers:** These customers purchase less frequently,
have lower overall spending, and have not purchased recently. Businesses can
target them with re-engagement campaigns, discounts, and personalized offers.

**Loyal / High-Value Customers:** These customers purchase more frequently,
spend significantly more, and have purchased more recently. Businesses can
focus on retention, loyalty programs, cross-selling, and upselling.
"""
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "SegmentIQ AI | Customer Segmentation & Business Intelligence"
)
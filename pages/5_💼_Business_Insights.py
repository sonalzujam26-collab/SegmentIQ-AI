import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui import load_css, sidebar_branding

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Business Insights | SegmentIQ AI",
    page_icon="💼",
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
# SEGMENT NAMES
# ---------------------------------------------------------

segment_names = {
    0: "Occasional / Low-Value",
    1: "Loyal / High-Value"
}

df["Segment"] = df["Cluster"].map(segment_names)


# ---------------------------------------------------------
# BUSINESS PROFILE
# ---------------------------------------------------------

profile = (
    df.groupby(["Cluster", "Segment"])
    .agg(
        Customers=("Customer ID", "count"),
        Recency=("Recency", "mean"),
        Frequency=("Frequency", "mean"),
        Monetary=("Monetary", "mean"),
        TotalQuantity=("TotalQuantity", "mean"),
        UniqueProducts=("UniqueProducts", "mean"),
        AverageOrderValue=("AverageOrderValue", "mean")
    )
    .reset_index()
)

profile["CustomerPercentage"] = (
    profile["Customers"] / len(df) * 100
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("💼 Business Insights")

st.write(
    "Convert customer segmentation results into practical "
    "business strategies and customer-focused actions."
)

st.divider()


# ---------------------------------------------------------
# KEY BUSINESS FINDINGS
# ---------------------------------------------------------

st.header("📊 Key Findings")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👥 Total Customers",
        f"{len(df):,}"
    )

with col2:

    st.metric(
        "🧩 Segments",
        df["Cluster"].nunique()
    )

with col3:

    high_value = profile.loc[
        profile["Cluster"] == 1,
        "Customers"
    ].iloc[0]

    st.metric(
        "🟢 High-Value Customers",
        f"{high_value:,}"
    )

with col4:

    high_value_percentage = profile.loc[
        profile["Cluster"] == 1,
        "CustomerPercentage"
    ].iloc[0]

    st.metric(
        "High-Value Customer Share",
        f"{high_value_percentage:.2f}%"
    )


st.divider()


# ---------------------------------------------------------
# SEGMENT BUSINESS INSIGHTS
# ---------------------------------------------------------

st.header("🎯 Segment-Level Insights")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# OCCASIONAL / LOW-VALUE
# ---------------------------------------------------------

with col1:

    st.warning(
        """
## 🟠 Occasional / Low-Value

**Customer profile**

These customers have lower purchase frequency and lower
overall spending. Their average recency is also much higher,
which means they have generally purchased less recently.

**Business objective**

### Re-engage these customers

**Recommended actions**

1. Personalized discount offers
2. Email re-engagement campaigns
3. Product recommendations
4. Limited-time offers
5. Encourage repeat purchases
"""
    )


# ---------------------------------------------------------
# LOYAL / HIGH-VALUE
# ---------------------------------------------------------

with col2:

    st.success(
        """
## 🟢 Loyal / High-Value

**Customer profile**

These customers purchase more frequently, spend significantly
more, buy a wider variety of products, and have purchased more
recently.

**Business objective**

### Retain and grow customer value

**Recommended actions**

1. Loyalty programs
2. Premium customer offers
3. Cross-selling
4. Upselling
5. Early access to new products
"""
    )


# ---------------------------------------------------------
# SPENDING COMPARISON
# ---------------------------------------------------------

st.divider()

st.header("💰 Customer Value Comparison")

fig = px.bar(
    profile,
    x="Segment",
    y="Monetary",
    text_auto=".2f",
    title="Average Spending by Customer Segment"
)

fig.update_layout(
    height=500,
    xaxis_title="Customer Segment",
    yaxis_title="Average Customer Spending"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# ORDER FREQUENCY COMPARISON
# ---------------------------------------------------------

st.header("🛒 Purchase Frequency Comparison")

fig = px.bar(
    profile,
    x="Segment",
    y="Frequency",
    text_auto=".2f",
    title="Average Orders per Customer"
)

fig.update_layout(
    height=500,
    xaxis_title="Customer Segment",
    yaxis_title="Average Orders"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# BUSINESS PRIORITIES
# ---------------------------------------------------------

st.divider()

st.header("🚀 Business Priorities")

st.info(
    """
### Priority 1 — Re-engage Occasional Customers

The Occasional / Low-Value segment represents **54.58%** of
customers. Increasing their purchase frequency can be an
important opportunity for customer re-engagement.

### Priority 2 — Retain High-Value Customers

The Loyal / High-Value segment represents **45.42%** of
customers and has substantially higher purchasing activity
and spending. Retaining these customers should be a major
business priority.

### Priority 3 — Personalize Marketing

Different customer groups show different purchasing behaviors.
Marketing strategies can therefore be tailored according to
the characteristics of each segment instead of treating every
customer in the same way.
"""
)


# ---------------------------------------------------------
# FINAL TAKEAWAY
# ---------------------------------------------------------

st.divider()

st.header("💡 Final Business Takeaway")

st.success(
    """
SegmentIQ AI converts raw transaction data into meaningful
customer groups.

The analysis identifies two major groups:

**Occasional / Low-Value Customers** → focus on re-engagement
and increasing purchase frequency.

**Loyal / High-Value Customers** → focus on retention,
loyalty, cross-selling, and upselling.

This allows businesses to use different strategies for
different customer groups.
"""
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "SegmentIQ AI | Customer Segmentation & Business Intelligence"
)
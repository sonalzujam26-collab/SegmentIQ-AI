import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui import load_css, sidebar_branding

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Segment Intelligence | SegmentIQ AI",
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
# SEGMENT NAMES
# ---------------------------------------------------------

segment_names = {
    0: "Occasional / Low-Value",
    1: "Loyal / High-Value"
}

df["Segment"] = df["Cluster"].map(segment_names)


# ---------------------------------------------------------
# SEGMENT PROFILE
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

st.title("🧩 Segment Intelligence")

st.write(
    "Understand the characteristics, purchasing behavior, and "
    "business opportunities of each customer segment."
)

st.divider()


# ---------------------------------------------------------
# SEGMENT CARDS
# ---------------------------------------------------------

st.header("👥 Customer Segment Profiles")

for _, row in profile.iterrows():

    if row["Cluster"] == 0:

        st.subheader("🟠 Occasional / Low-Value Customers")

        st.write(
            "Customers with fewer purchases, lower spending, "
            "and longer time since their last purchase."
        )

    else:

        st.subheader("🟢 Loyal / High-Value Customers")

        st.write(
            "Customers with frequent purchases, higher spending, "
            "more product variety, and more recent activity."
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Customers",
            f"{row['Customers']:,}"
        )

    with col2:
        st.metric(
            "Customer Share",
            f"{row['CustomerPercentage']:.2f}%"
        )

    with col3:
        st.metric(
            "Avg. Spending",
            f"£{row['Monetary']:,.2f}"
        )

    with col4:
        st.metric(
            "Avg. Orders",
            f"{row['Frequency']:.2f}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Avg. Recency",
            f"{row['Recency']:.2f} days"
        )

    with col2:
        st.metric(
            "Avg. Products",
            f"{row['UniqueProducts']:.2f}"
        )

    with col3:
        st.metric(
            "Avg. Order Value",
            f"£{row['AverageOrderValue']:,.2f}"
        )

    st.divider()


# ---------------------------------------------------------
# COMPARISON CHARTS
# ---------------------------------------------------------

st.header("📊 Segment Comparison")

col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        profile,
        x="Segment",
        y="Frequency",
        title="Average Orders per Customer",
        text_auto=".2f"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Customer Segment",
        yaxis_title="Average Orders"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        profile,
        x="Segment",
        y="Monetary",
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
# RECENCY COMPARISON
# ---------------------------------------------------------

fig = px.bar(
    profile,
    x="Segment",
    y="Recency",
    title="Average Days Since Last Purchase",
    text_auto=".2f"
)

fig.update_layout(
    height=450,
    xaxis_title="Customer Segment",
    yaxis_title="Average Recency (Days)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# BUSINESS ACTIONS
# ---------------------------------------------------------

st.header("💡 Recommended Business Actions")

col1, col2 = st.columns(2)


with col1:

    st.warning(
        """
### 🟠 Occasional / Low-Value

**Goal: Re-engage and increase activity**

Recommended actions:

- Send personalized offers
- Provide limited-time discounts
- Use email re-engagement campaigns
- Recommend products based on previous purchases
- Encourage repeat purchases
"""
    )


with col2:

    st.success(
        """
### 🟢 Loyal / High-Value

**Goal: Retain and increase customer value**

Recommended actions:

- Introduce loyalty programs
- Provide premium offers
- Use cross-selling
- Use upselling
- Give early access to new products
- Focus on customer retention
"""
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "SegmentIQ AI | Customer Segmentation & Business Intelligence"
)
import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui import load_css, sidebar_branding

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Customer Explorer | SegmentIQ AI",
    page_icon="🔍",
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
# PAGE HEADER
# ---------------------------------------------------------

st.title("🔍 Customer Explorer")

st.write(
    "Explore individual customers and understand their purchasing "
    "behavior and customer segment."
)

st.divider()


# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    selected_segment = st.selectbox(
        "Select Customer Segment",
        ["All Customers"] + list(segment_names.values())
    )

with col2:

    search_id = st.text_input(
        "Search Customer ID",
        placeholder="Enter Customer ID"
    )


# ---------------------------------------------------------
# APPLY SEGMENT FILTER
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_segment != "All Customers":

    filtered_df = filtered_df[
        filtered_df["Segment"] == selected_segment
    ]


# ---------------------------------------------------------
# CUSTOMER SEARCH
# ---------------------------------------------------------

if search_id.strip():

    try:
        customer_id = float(search_id)

        customer_result = filtered_df[
            filtered_df["Customer ID"] == customer_id
        ]

    except ValueError:

        customer_result = pd.DataFrame()

else:

    customer_result = pd.DataFrame()


# ---------------------------------------------------------
# CUSTOMER DETAILS
# ---------------------------------------------------------

if not customer_result.empty:

    customer = customer_result.iloc[0]

    st.header("👤 Customer Profile")

    st.success(
        f"Customer {int(customer['Customer ID'])} "
        f"belongs to the **{customer['Segment']}** segment."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📅 Recency",
            f"{customer['Recency']:.0f} days"
        )

    with col2:
        st.metric(
            "🛒 Orders",
            f"{customer['Frequency']:.0f}"
        )

    with col3:
        st.metric(
            "💰 Total Spending",
            f"£{customer['Monetary']:,.2f}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📦 Total Quantity",
            f"{customer['TotalQuantity']:,.0f}"
        )

    with col2:
        st.metric(
            "🛍️ Unique Products",
            f"{customer['UniqueProducts']:,.0f}"
        )

    with col3:
        st.metric(
            "💳 Average Order Value",
            f"£{customer['AverageOrderValue']:,.2f}"
        )

else:

    st.info(
        "Enter a Customer ID above to view the customer's detailed profile."
    )


# ---------------------------------------------------------
# CUSTOMER DISTRIBUTION
# ---------------------------------------------------------

st.divider()

st.header("📊 Customer Distribution")

fig = px.scatter(
    filtered_df,
    x="Frequency",
    y="Monetary",
    color="Segment",
    hover_data=[
        "Customer ID",
        "Recency",
        "TotalQuantity",
        "UniqueProducts",
        "AverageOrderValue"
    ],
    title="Customer Spending vs Order Frequency"
)

fig.update_layout(
    height=600,
    xaxis_title="Number of Orders",
    yaxis_title="Total Spending"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# CUSTOMER TABLE
# ---------------------------------------------------------

st.header("📋 Customer Data")

display_df = filtered_df[
    [
        "Customer ID",
        "Segment",
        "Recency",
        "Frequency",
        "Monetary",
        "TotalQuantity",
        "UniqueProducts",
        "AverageOrderValue"
    ]
].copy()

display_df.columns = [
    "Customer ID",
    "Segment",
    "Recency (Days)",
    "Orders",
    "Total Spending",
    "Total Quantity",
    "Unique Products",
    "Average Order Value"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
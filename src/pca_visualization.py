import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 1. Load PCA dataset
# --------------------------------------------------

file_path = "data/processed/customer_segments_pca.csv"

df = pd.read_csv(file_path)


# --------------------------------------------------
# 2. Create cluster labels
# --------------------------------------------------

df["Cluster"] = df["Cluster"].astype(str)


# --------------------------------------------------
# 3. Create interactive PCA chart
# --------------------------------------------------

fig = px.scatter(
    df,
    x="PC1",
    y="PC2",
    color="Cluster",
    hover_data=[
        "Customer ID",
        "Recency",
        "Frequency",
        "Monetary",
        "TotalQuantity",
        "UniqueProducts",
        "AverageOrderValue"
    ],
    title="Customer Segmentation — PCA Visualization",
    labels={
        "PC1": "Principal Component 1",
        "PC2": "Principal Component 2",
        "Cluster": "Customer Segment"
    }
)


# --------------------------------------------------
# 4. Improve chart appearance
# --------------------------------------------------

fig.update_traces(
    marker=dict(
        size=7,
        opacity=0.65
    )
)

fig.update_layout(
    height=650,
    legend_title="Customer Segment",
    hovermode="closest"
)


# --------------------------------------------------
# 5. Save interactive HTML
# --------------------------------------------------

output_path = "assets/customer_pca_visualization.html"

fig.write_html(output_path)


print("Interactive PCA visualization created successfully!")

print("\nSaved to:")
print(output_path)

print("\nNumber of customers visualized:")
print(len(df))
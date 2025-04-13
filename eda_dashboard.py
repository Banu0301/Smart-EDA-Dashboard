import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 EDA Dashboard", layout="wide")

# --------------------------
# Header
# --------------------------
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .block-container { padding-top: 2rem; }
    .css-1aumxhk { font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3 { color: #003262; }
    .stButton>button { border-radius: 10px; background-color: #0066cc; color: white; padding: 0.5em 1em; }
    .stFileUploader label { font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Smart EDA Dashboard")
st.markdown("Upload your dataset to get a quick, interactive exploratory analysis.")

# --------------------------
# Upload Section
# --------------------------
uploaded_file = st.file_uploader("📁 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Load dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File loaded successfully!")
    st.write("### 👁️ Data Preview", df.head())

    # --------------------------
    # Data Overview
    # --------------------------
    st.markdown("### 🧾 Dataset Info")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")
        st.write("**Column Names:**", list(df.columns))
    with col2:
        st.write("**Data Types**")
        st.write(df.dtypes)

    # --------------------------
    # Summary Statistics
    # --------------------------
    st.markdown("### 📊 Summary Statistics")
    st.dataframe(df.describe(include='all').transpose())

    # --------------------------
    # Missing Value Heatmap
    # --------------------------
    st.markdown("### 🚨 Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        st.write(missing)
        fig, ax = plt.subplots()
        sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="Reds")
        st.pyplot(fig)
    else:
        st.success("No missing values detected.")

    # --------------------------
    # Correlation Matrix
    # --------------------------
    st.markdown("### 🔗 Correlation Heatmap (Numeric Only)")
    num_df = df.select_dtypes(include=np.number)
    if not num_df.empty:
        corr = num_df.corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
        st.plotly_chart(fig, use_container_width=True)

    # --------------------------
    # Categorical Summary
    # --------------------------
    cat_cols = df.select_dtypes(include='object').columns
    if len(cat_cols) > 0:
        st.markdown("### 🧮 Categorical Column Summary")
        selected_col = st.selectbox("Select a categorical column to view counts", cat_cols)
        st.write(df[selected_col].value_counts().head(10))

    # --------------------------
    # Interactive Chart Generator
    # --------------------------
    st.markdown("### 📊 Professional Data Visualizations")

    chart_type = st.selectbox("Choose Chart Type", ["Bar Chart", "Line Chart", "Pie Chart", "Histogram", "Box Plot", "Scatter Plot"])

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    all_cols = df.columns.tolist()

    if chart_type in ["Bar Chart", "Pie Chart"]:
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        if cat_cols:
            cat_col = st.selectbox("Select Categorical Column", cat_cols)
            agg_col = st.selectbox("Select Value Column (Optional)", ["None"] + numeric_cols)
            agg_func = st.selectbox("Aggregation", ["count", "sum", "mean", "median"]) if agg_col != "None" else "count"

            if chart_type == "Bar Chart":
                temp_df = df.groupby(cat_col)[agg_col].agg(agg_func).reset_index() if agg_col != "None" else df[cat_col].value_counts().reset_index()
                fig = px.bar(temp_df, x=cat_col, y=temp_df.columns[1], title=f"{agg_func.title()} by {cat_col}")
            else:
                temp_df = df.groupby(cat_col)[agg_col].agg(agg_func).reset_index() if agg_col != "None" else df[cat_col].value_counts().reset_index()
                fig = px.pie(temp_df, names=cat_col, values=temp_df.columns[1], title=f"{agg_func.title()} by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Histogram":
        selected_col = st.selectbox("Select Numeric Column for Histogram", numeric_cols)
        fig = px.histogram(df, x=selected_col, nbins=30, marginal="box", opacity=0.75,
                           title=f"Histogram + Box for {selected_col}",
                           color_discrete_sequence=["#003262"])
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        x = st.selectbox("Group By (X-Axis)", all_cols)
        y = st.selectbox("Numeric Column (Y-Axis)", numeric_cols)
        fig = px.box(df, x=x, y=y, points="all", notched=True,
                     title=f"Box Plot of {y} grouped by {x}",
                     color_discrete_sequence=["#1f77b4"],  # Custom color
                     labels={x: f"{x} Category", y: f"{y} Distribution"})
        
        fig.update_layout(
            title_x=0.5,  # Center title
            title_font_size=18,
            xaxis_title=f"{x} Category",
            yaxis_title=f"{y} Value Distribution",
            xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility
            showlegend=False  # Hide legend as it's not necessary for Box Plot
        )

        fig.update_traces(
            boxmean="sd",  # Display mean as standard deviation
            jitter=0.05,  # Add slight jitter for point distribution
            marker=dict(color="#FF5733", size=6)  # Customize outlier points
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart":
        x = st.selectbox("X-Axis (Must be Date or Ordinal)", all_cols)
        y = st.selectbox("Y-Axis", numeric_cols)
        fig = px.line(df, x=x, y=y, markers=True,
                      title=f"Line Chart of {y} over {x}",
                      color_discrete_sequence=["#2e86de"])
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        x = st.selectbox("X-Axis", numeric_cols)
        y = st.selectbox("Y-Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        hue = st.selectbox("Color By (Optional)", ["None"] + all_cols)
        fig = px.scatter(df, x=x, y=y, color=None if hue == "None" else hue,
                         trendline="ols", title=f"Scatter Plot of {y} vs {x} with Trendline",
                         opacity=0.8)
        st.plotly_chart(fig, use_container_width=True)


    # --------------------------
    # Download JSON (Optional)
    # --------------------------
    st.markdown("### 📥 Download JSON version of your data")
    json_data = df.to_json(orient='records', indent=2)
    st.download_button("Download JSON", json_data, file_name="data.json", mime="application/json")

else:
    st.info("Upload a CSV or Excel file to begin.")

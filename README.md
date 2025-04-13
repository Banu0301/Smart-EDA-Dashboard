# Smart EDA Dashboard

## Overview

The **Smart EDA Dashboard** is an interactive web application built with **Streamlit** that allows users to upload datasets (CSV or Excel files) and explore them through various **visualizations** and **summary statistics**. The app performs **Exploratory Data Analysis (EDA)**, providing insights such as missing values, correlation matrices, and categorical column summaries, as well as interactive charts like bar charts, line charts, histograms, and more.

### Features:
- Upload your dataset (CSV or Excel).
- Visualize missing values with a heatmap.
- Generate summary statistics for numerical and categorical columns.
- Display correlation heatmap for numeric columns.
- Interactive charts: Bar chart, Line chart, Pie chart, Histogram, Box plot, and Scatter plot.
- Download dataset in JSON format.

## Technologies Used:
- **Python**
- **Streamlit**: For the web application.
- **Pandas**: For data manipulation.
- **Numpy**: For numerical operations.
- **Plotly**: For interactive visualizations.
- **Matplotlib** and **Seaborn**: For static visualizations.

## Installation

To run the Smart EDA Dashboard locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Banu0301/Smart-EDA-Dashboard.git


**2.Navigate to the project directory:**
  cd eda-dashboard
  
**3. Create a virtual environment (optional but recommended):**
  python3 -m venv venv
  
  
**4.  Activate the virtual environment:**

    On Windows:
    .\venv\Scripts\activate
    
   On macOS/Linux:
    source venv/bin/activate

**5.Install the required dependencies:**

  pip install -r requirements.txt
  
**6.Run the Streamlit app:**

 streamlit run eda_dashboard.py
 
After running this command, the app will open in your web browser.




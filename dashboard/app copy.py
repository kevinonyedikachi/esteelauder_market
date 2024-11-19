import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime

# Streamlit App Title
st.title("Data Analysis and Visualization Dashboard")

# Upload the dataset
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load the data depending on the file type
    if uploaded_file.name.endswith('.csv'):
        gaia_data = pd.read_csv(uploaded_file)
    else:
        gaia_data = pd.read_excel(uploaded_file)

    # Show the dataframe (top rows)
    st.subheader("Data Overview")
    st.write(gaia_data.head())

    # General Information of the Data
    st.subheader("Data Info")
    st.text(gaia_data.info())

    # Data Cleaning Summary
    st.subheader("Missing Data Analysis")
    missing_data = gaia_data.isnull().sum()
    missing_data_percentage = (missing_data / gaia_data.shape[0]) * 100
    missing_data_summary = pd.DataFrame({
        "Missing Values": missing_data,
        "Percentage": missing_data_percentage
    })
    st.write(missing_data_summary)

    # Handle missing values if necessary
    st.sidebar.header("Data Preprocessing")
    handle_missing_data = st.sidebar.selectbox(
        "Select Action for Missing Data", ["Do Nothing", "Drop Rows with Missing Values", "Fill Missing Values with Mean"]
    )

    if handle_missing_data == "Drop Rows with Missing Values":
        gaia_data = gaia_data.dropna()
        st.write("Rows with missing values have been dropped.")
    elif handle_missing_data == "Fill Missing Values with Mean":
        gaia_data.fillna(gaia_data.mean(), inplace=True)
        st.write("Missing values filled with mean.")

    # Convert 'Publication date' to datetime
    gaia_data['Publication date'] = pd.to_datetime(gaia_data['Publication date'], errors='coerce')

    # Storytelling Section: Show Summary Statistics
    st.subheader("Summary Statistics")
    st.write(gaia_data.describe())

    # Visualize Distribution of Numeric Columns
    st.subheader("Numeric Feature Distribution")
    numeric_columns = gaia_data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:
        selected_column = st.selectbox("Select a numeric feature to visualize its distribution", numeric_columns)
        fig, ax = plt.subplots()
        sns.histplot(gaia_data[selected_column].dropna(), kde=True, ax=ax)
        ax.set_title(f'Distribution of {selected_column}')
        st.pyplot(fig)
    else:
        st.write("No numeric columns found for visualization.")

    # Analyze 'Equadis Status' and 'Retailer' columns
    st.subheader("Equadis Status vs Retailer")
    equadis_retailer_df = gaia_data.groupby(['Equadis Status', 'Retailer']).size().reset_index(name='Count')
    fig = px.bar(equadis_retailer_df, x='Retailer', y='Count', color='Equadis Status', 
                 title="Count of 'Equadis Status' for each 'Retailer'")
    st.plotly_chart(fig)

    # Analyze 'Publication date' trends
    st.subheader("Publication Date Trend Analysis")
    if 'Publication date' in gaia_data.columns:
        gaia_data['Year'] = gaia_data['Publication date'].dt.year
        year_counts = gaia_data['Year'].value_counts().sort_index()
        fig = px.line(x=year_counts.index, y=year_counts.values, labels={'x': 'Year', 'y': 'Count'},
                      title="Number of Publications per Year")
        st.plotly_chart(fig)
    else:
        st.write("No 'Publication date' column found for analysis.")

    # Error analysis in the 'Equadis error' and 'Connector error' columns
    st.subheader("Error Analysis")
    if 'Equadis error' in gaia_data.columns:
        equadis_errors = gaia_data['Equadis error'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=equadis_errors.index, y=equadis_errors.values, ax=ax)
        ax.set_title("Top 10 'Equadis Error' Types")
        ax.set_ylabel('Count')
        ax.set_xlabel('Error Type')
        st.pyplot(fig)
    
    if 'Connector error' in gaia_data.columns:
        connector_errors = gaia_data['Connector error'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=connector_errors.index, y=connector_errors.values, ax=ax)
        ax.set_title("Top 10 'Connector Error' Types")
        ax.set_ylabel('Count')
        ax.set_xlabel('Error Type')
        st.pyplot(fig)

    # Interactive data filtering options
    st.sidebar.header("Interactive Filtering")
    retailer_options = gaia_data['Retailer'].unique()
    selected_retailer = st.sidebar.selectbox("Select Retailer", retailer_options)
    filtered_data = gaia_data[gaia_data['Retailer'] == selected_retailer]

    st.subheader(f"Filtered Data for {selected_retailer}")
    st.write(filtered_data)

    # Additional analysis based on the filtered data
    if len(filtered_data) > 0:
        st.subheader(f"Analysis for {selected_retailer}")
        st.write(filtered_data.describe())

    # Display the complete filtered data
    st.subheader("Filtered Data Table")
    st.write(filtered_data)

else:
    st.warning("Please upload a dataset to proceed.")

# --- Additional analysis sections ---

# Load data with caching (useful if data is large and won't change often)
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    if 'Publication date' in data.columns:
        data['Publication date'] = pd.to_datetime(data['Publication date'], errors='coerce')
    return data

# Load the dataset
gaia_data = load_data('data/gaia_data.csv')  # Ensure correct file path

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a Report Section:", 
                            ["Overview", "Missing Data", "Descriptive Analysis", "Time Trends", 
                             "Error Analysis", "Retailer Performance", "Text Analysis"])

# Overview Section
if options == "Overview":
    st.title("Dataset Overview")
    st.write("### General Information:")
    st.write(gaia_data.info())
    st.write("### Sample Data:")
    st.dataframe(gaia_data.head())
    
    st.write("### Summary Statistics:")
    st.write(gaia_data.describe(include='all'))

    st.write("### Missing Values:")
    st.bar_chart(gaia_data.isnull().sum())

# Missing Data Section
elif options == "Missing Data":
    st.title("Missing Data Analysis")
    st.write("### Missing Data Heatmap:")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(gaia_data.isnull(), cbar=False, cmap="viridis", ax=ax)
    st.pyplot(fig)

    st.write("### Missing Data by Column:")
    missing_data = gaia_data.isnull().sum()
    st.bar_chart(missing_data)

# Descriptive Analysis Section
elif options == "Descriptive Analysis":
    st.title("Descriptive Analysis")
    
    st.write("### Categorical Columns Distribution:")
    selected_col = st.selectbox("Select a Column:", ['Retailer', 'Equadis Status', 'Global Connector Status'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=gaia_data, y=selected_col, order=gaia_data[selected_col].value_counts().index, ax=ax)
    ax.set_title(f"Distribution of {selected_col}")
    st.pyplot(fig)

# Time Trends Section
elif options == "Time Trends":
    st.title("Time-Based Trends")
    
    st.write("### Publications Over Time:")
    if 'Publication date' in gaia_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        gaia_data.set_index('Publication date')['GTIN'].resample('M').count().plot(ax=ax)
        ax.set_title("Product Publications Over Time")
        st.pyplot(fig)
    else:
        st.write("No 'Publication date' column found.")

    st.write("### Errors Over Time:")
    if 'Publication date' in gaia_data.columns and 'Equadis error' in gaia_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        gaia_data.set_index('Publication date')['Equadis error'].resample('M').count().plot(color='red', ax=ax)
        ax.set_title("Equadis Errors Over Time")
        st.pyplot(fig)
    else:
        st.write("No 'Equadis error' column found.")

# Error Analysis Section
elif options == "Error Analysis":
    st.title("Error Analysis")
    
    st.write("### Error Frequency:")
    if 'Equadis error' in gaia_data.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        gaia_data['Equadis error'].value_counts().plot(kind='bar', color='darkblue', ax=ax)
        ax.set_title("Frequency of Equadis Errors")
        st.pyplot(fig)
    else:
        st.write("No 'Equadis error' column found.")

    st.write("### Error Heatmap by Retailer and User:")
    if 'Retailer' in gaia_data.columns and 'User' in gaia_data.columns:
        error_heatmap = pd.crosstab(gaia_data['Retailer'], gaia_data['User'])
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(error_heatmap, cmap='coolwarm', ax=ax)
        ax.set_title("Error Heatmap by Retailer and User")
        st.pyplot(fig)
    else:
        st.write("No 'Retailer' or 'User' column found.")

# Retailer Performance Section
elif options == "Retailer Performance":
    st.title("Retailer Performance")
    
    if 'Retailer' in gaia_data.columns:
        retailer_perf = gaia_data.groupby('Retailer').agg(
            Total=('GTIN', 'count'),
            Errors=('Equadis error', 'count'),
            SuccessRate=lambda x: 1 - (x.isnull().sum() / len(x))
        )
        retailer_perf['ErrorRate'] = retailer_perf['Errors'] / retailer_perf['Total']

        st.write("### Performance Metrics:")
        st.dataframe(retailer_perf)

        st.write("### Success vs Error Rates:")
        fig, ax = plt.subplots(figsize=(12, 6))
        retailer_perf[['SuccessRate', 'ErrorRate']].plot(kind='bar', ax=ax)
        ax.set_title("Retailer Success vs Error Rates")
        st.pyplot(fig)
    else:
        st.write("No 'Retailer' column found.")

# Text Analysis Section
elif options == "Text Analysis":
    st.title("Text Analysis")
    
    st.write("### Word Cloud for Product Names:")
    if 'Product Name' in gaia_data.columns:
        text_data = ' '.join(gaia_data['Product Name'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    if 'Equadis error' in gaia_data.columns:
        text_data = ' '.join(gaia_data['Equadis error'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.write("No 'Equadis error' column found.")

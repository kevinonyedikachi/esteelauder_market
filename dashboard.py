import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud

# Load data with caching
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    if 'Publication date' in data.columns:
        data['Publication date'] = pd.to_datetime(data['Publication date'], errors='coerce')
    return data

# Load the dataset
gaia_data = load_data('gaia_data.csv')  # Ensure correct file path

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
    else:
        st.write("No 'Product Name' column found.")

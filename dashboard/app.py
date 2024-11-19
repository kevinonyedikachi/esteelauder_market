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

# Load the dataset
gaia_data = pd.read_excel('data/gaia_data.xlsx')  # Ensure correct file path

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a Report Section:", 
                            ["Overview", "Missing Data", "Descriptive Analysis", "Time Trends", 
                             "Error Analysis", "Retailer Performance", "Text Analysis"])

# Overview Section
if options == "Overview":
    st.title("Dataset Overview")
    st.write("### General Information:")
    st.write(gaia_data.info())  # Display dataset info
    st.write("### Sample Data:")
    st.dataframe(gaia_data.head())  # Display the first 5 rows of the dataset
    
    st.write("### Summary Statistics:")
    st.write(gaia_data.describe(include='all'))  # Show summary statistics for all columns

    st.write("### Missing Values:")
    st.bar_chart(gaia_data.isnull().sum())  # Plot missing values count

# Missing Data Section
elif options == "Missing Data":
    st.title("Missing Data Analysis")
    
    # Missing Data Heatmap
    # st.write("### Missing Data Heatmap:")
    # fig, ax = plt.subplots(figsize=(12, 6))
    # sns.heatmap(gaia_data.isnull(), cbar=False, cmap="viridis", ax=ax)
    # st.pyplot(fig)

    # Missing Data by Column
    st.write("### Missing Data by Column:")
    missing_data = gaia_data.isnull().sum()
    st.bar_chart(missing_data)  # Plot missing data by column

# Descriptive Analysis Section
elif options == "Descriptive Analysis":
    st.title("Descriptive Analysis")
    
    st.write("### Categorical Columns Distribution:")
    
    # Select a categorical column for visualization
    selected_col = st.selectbox("Select a Column:", ['Retailer', 'Equadis Status', 'Global Connector Status'])
    
    # Plot the count distribution for the selected column
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=gaia_data, y=selected_col, order=gaia_data[selected_col].value_counts().index, ax=ax)
    ax.set_title(f"Distribution of {selected_col}")
    st.pyplot(fig)

    # Display unique values for each categorical column
    categorical_col = ['Retailer', 'Equadis Status', 'Global Connector Status', 'Detailed Connector Status', 'User']
    for col in categorical_col:
        st.write(f"### Unique values in '{col}':")
        st.write(gaia_data[col].value_counts())  # Display the unique value counts for each categorical column

    # Frequency Distribution of Categorical Columns
    for col in categorical_col:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=gaia_data, y=col, order=gaia_data[col].value_counts().index)
       # Set the title and labels
        ax.set_title(f'Frequency Distribution of {col}')
        ax.set_xlabel('Count')
        ax.set_ylabel(col)
    
        # Pass the figure object to st.pyplot()
        st.pyplot(fig)

# Time Trends Section
elif options == "Time Trends":
    st.title("Time-Based Trends")
    
    # Product Publications Over Time
    st.write("### Publications Over Time:")
    if 'Publication date' in gaia_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        gaia_data.set_index('Publication date')['GTIN'].resample('M').count().plot(ax=ax)
        ax.set_title("Product Publications Over Time")
        st.pyplot(fig)
    else:
        st.write("No 'Publication date' column found.")

    # Equadis Errors Over Time
    st.write("### Equadis Errors Over Time:")
    if 'Publication date' in gaia_data.columns and 'Equadis error' in gaia_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        gaia_data.set_index('Publication date')['Equadis error'].resample('M').count().plot(color='red', ax=ax)
        ax.set_title("Equadis Errors Over Time")
        st.pyplot(fig)
    
    # Global Connector Status Over Time
    st.write("### Global Connector Status Error Over Time:")
    if 'Publication date' in gaia_data.columns and 'Global Connector Status' in gaia_data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        gaia_data.set_index('Publication date')['Global Connector Status'].resample('M').count().plot(color='black', ax=ax)
        ax.set_title("Global Connector Status Over Time")
        st.pyplot(fig)
    else:
        st.write("No 'Equadis error' column found.")

# Error Analysis Section
elif options == "Error Analysis":
    st.title("Error Analysis")
    
    # Error Heatmap by Retailer and User
    st.write("### Error Heatmap by Retailer and User:")
    if 'Retailer' in gaia_data.columns and 'User' in gaia_data.columns:
        error_heatmap = pd.crosstab(gaia_data['Retailer'], gaia_data['User'])
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(error_heatmap, cmap='coolwarm', ax=ax)
        ax.set_title("Error Heatmap by Retailer and User")
        st.pyplot(fig)
    else:
        st.write("No 'Retailer' or 'User' column found.")

    # Check if necessary columns are available in the dataset
    if 'Retailer' in gaia_data.columns and 'Connector error' in gaia_data.columns:
        # Count the number of Connector errors by Retailer
        retailer_connector_error = gaia_data.groupby('Retailer')['Connector error'].count().sort_values(ascending=False)
        
        # Plot the error count for each Retailer
        fig, ax = plt.subplots(figsize=(12, 6))
        retailer_connector_error.plot(kind='bar', color='darkblue', ax=ax)
        ax.set_title("Connector Errors by Retailer")
        ax.set_xlabel('Retailer')
        ax.set_ylabel('Number of Connector Errors')
        st.pyplot(fig)
    else:
        st.write("No 'Retailer' or 'Connector error' column found.")
    
    # Error Analysis by User and Connector error
    st.write("### Error Analysis by User and Connector Error")
    
    # Check if necessary columns are available in the dataset
    if 'User' in gaia_data.columns and 'Connector error' in gaia_data.columns:
        # Count the number of Connector errors by User
        user_connector_error = gaia_data.groupby('User')['Connector error'].count().sort_values(ascending=False)
        
        # Plot the error count for each User
        fig, ax = plt.subplots(figsize=(12, 6))
        user_connector_error.plot(kind='bar', color='coral', ax=ax)
        ax.set_title("Connector Errors by User")
        ax.set_xlabel('User')
        ax.set_ylabel('Number of Connector Errors')
        st.pyplot(fig)
    else:
        st.write("No 'User' or 'Connector error' column found.")

    # Check if necessary columns are available in the dataset
    if 'Publication date' in gaia_data.columns and 'Connector error' in gaia_data.columns:
        # Convert 'Publication date' to datetime if it's not already
        gaia_data['Publication date'] = pd.to_datetime(gaia_data['Publication date'], errors='coerce')
        
        # Group by the 'Publication date' and count the number of Connector errors
        date_connector_error = gaia_data.groupby(gaia_data['Publication date'].dt.to_period('M'))['Connector error'].count()
        
        # Plot the error count over time
        fig, ax = plt.subplots(figsize=(12, 6))
        date_connector_error.plot(kind='line', color='green', marker='o', ax=ax)
        ax.set_title("Connector Errors by Date")
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Connector Errors')
        st.pyplot(fig)
    else:
        st.write("No 'Publication date' or 'Connector error' column found.")

# Retailer Performance Section
elif options == "Retailer Performance":
    st.title("Retailer Performance")
    
    # Retailer Performance Metrics
    if 'Retailer' in gaia_data.columns:
        retailer_performance = gaia_data.groupby('Retailer').agg(
            Total=('GTIN', 'count'),
            Errors=('Connector error', 'count')  # Assuming non-null Equadis errors are counted
        )

        # Calculate SuccessRate and ErrorRate
        retailer_performance['SuccessRate'] = 1 - (retailer_performance['Errors'] / retailer_performance['Total'])
        retailer_performance['ErrorRate'] = retailer_performance['Errors'] / retailer_performance['Total']
        
        # Display Performance Metrics
        st.write("### Performance Metrics:")
        st.dataframe(retailer_performance)

        # Plot Success vs Error Rates
        st.write("### Success vs Error Rates:")
        fig, ax = plt.subplots(figsize=(12, 6))
        retailer_performance[['SuccessRate', 'ErrorRate']].plot(kind='bar', ax=ax)
        ax.set_title("Retailer Success vs Error Rates")
        st.pyplot(fig)
    else:
        st.write("No 'Retailer' column found.")

# Text Analysis Section
elif options == "Text Analysis":
    st.title("Text Analysis")
    
    # Word Cloud for most common words
    st.write("### Word Cloud for most common words")
    
    # Word cloud for 'Product Name' if available
    if 'Product Name' in gaia_data.columns:
        text_data = ' '.join(gaia_data['Product Name'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    
    # Word cloud for 'Equadis error' if available
    if 'Equadis error' in gaia_data.columns:
        text_data = ' '.join(gaia_data['Equadis error'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    
    # Word cloud for 'Connector error' if available
    if 'Connector error' in gaia_data.columns:
        text_data = ' '.join(gaia_data['Connector error'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.write("No 'Connector error' column found.")

import streamlit as st
import requests
import os

# Configure the API endpoint
API_URL = os.getenv('API_ENDPOINT', 'https://your-api-gateway-url/prod/query')

# Set page config
st.set_page_config(
    page_title="Query Dashboard",
    layout="wide"
)

# Add custom CSS for styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Query Dashboard")
st.markdown("Enter your query below to search the database.")

# Query input
query = st.text_input("Enter your query:", key="query_input")

# Submit button
if st.button("Submit Query"):
    if query:
        try:
            # Make API request
            response = requests.post(
                API_URL,
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # Display results
                st.subheader("Results")
                results = response.json()
                st.json(results)
            else:
                st.error(f"Error: API returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")
    else:
        st.warning("Please enter a query first.")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
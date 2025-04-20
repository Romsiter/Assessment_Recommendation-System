import streamlit as st
import requests
API_URL = "http://localhost:8000/recommend"


st.title('SHL Assessment Recommendation System')
st.markdown("Enter a job description or requirements")

query = st.text_area("Type here")
num_results = st.slider("Number of results:", 1, 10, 1)

if st.button("Get Assessments"):
    if not query:
        st.warning("Please enter some job description first")
    else:
        with st.spinner("Fetching recommendations…"):
            response = requests.post(
                API_URL,
                json={"text": query, "max_results": num_results},
                timeout=60
            )
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                st.table(results)
            else:
                st.info("No relevant assessments found for this query.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
        

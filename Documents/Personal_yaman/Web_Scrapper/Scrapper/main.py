import streamlit as st
from add_driver import Add_driver
import pickle
import json
from get_data_class import get_data_class_url_file_config
# Initialize session state for key-value pairs


# Title of the app
st.title("AI Web Scraper and Key-Value Input Form")

# Web Scraper Section
st.header("AI Web Scraper")
url = st.text_input("Paste your website URL here")


if st.button("Scrape site"):
    if url:
        result = Add_driver(url)
        print("the result is",result)

        st.subheader("HTML Source Code")
        st.text_area("HTML Source Code", result, height=300)

        st.subheader("Website Preview")
        st.markdown(
            f'<div style="display: flex; justify-content: center;">'
            f'<iframe src="{url}" width="1500" height="700" frameborder="0"></iframe>'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # Independent message to guide the user
        st.markdown(
            f'<p style="font-size: 20px;">If the preview is not available, open <a href="{url}" target="_blank">{url}</a> in a new tab to view the source code.</p>',
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter a valid URL.")


st.header("Enter the Scraping Parameters Here")


# Initialize session state to store label and tag fields
if 'labeling' not in st.session_state:
    st.session_state.labeling = [{'label': '', 'tag': ''}]

# Function to add new inputs when the "Add More" button is pressed
def add_new_input():
    st.session_state.labeling.append({'label': '', 'tag': ''})

# Display input fields for label and tag with placeholders
for index, field in enumerate(st.session_state.labeling):
    cols = st.columns(2)
    with cols[0]:
        field['label'] = st.text_input(f"Label {index + 1}", value=field['label'], key=f"label_{index}", placeholder="Label")
    with cols[1]:
         field['tag'] = st.text_input(f"Tag {index + 1}", value=field['tag'], key=f"tag_{index}", placeholder="Tag")

# Button to add more label and tag fields
st.button("Add More", on_click=add_new_input)
if st.button("Submit"):
    # Create a dictionary to hold the label and tag pairs
    submitted_data = {
        f"Label {i + 1}": {
            'label': field['label'],
            'tag': field['tag']
        } for i, field in enumerate(st.session_state.labeling)
    }
    
    if submitted_data:
        st.success("Submitted Inputs:")
        st.write(submitted_data)
        with open("submitted_data.pkl", "wb") as f:
            pickle.dump(submitted_data, f)
            
        instantiate_url = get_data_class_url_file_config(url)
        
    else:
        st.warning("Please fill in both Label and Tag for at least one entry.")

   
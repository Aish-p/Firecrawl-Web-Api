import streamlit as st
import os
import gc
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import time
import pandas as pd
from pydantic import BaseModel
import json


load_dotenv()
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

@st.cache_resource
def load_app():
    app = FirecrawlApp(api_key=firecrawl_api_key)
    return app

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "schema_fields" not in st.session_state:
    st.session_state.schema_fields = [{"name": "", "type": "str"}]

def reset_chat():
    st.session_state.messages = []
    gc.collect()

def create_dynamic_model(fields):
    """Create a dynamic Pydantic model from schema fields."""
    field_annotations = {}
    for field in fields:
        if field["name"]:
            # Convert string type names to actual types
            type_mapping = {
                "str": str,
                "bool": bool,
                "int": int,
                "float": float
            }
            field_annotations[field["name"]] = type_mapping[field["type"]]
    
    # Dynamically create the model class
    return type(
        "ExtractSchema",
        (BaseModel,),
        {
            "__annotations__": field_annotations
        }
    )

def create_schema_from_fields(fields):
    """Create schema using Pydantic model."""
    # Filter out empty field names
    valid_fields = [field for field in fields if field["name"].strip()]
    if not valid_fields:
        return None
    
    model_class = create_dynamic_model(valid_fields)
    return model_class.model_json_schema()

def convert_to_table(data):
    """Convert a list of dictionaries to a markdown table."""
    if not data:
        return ""
    
    # Clean and format the data
    df = pd.DataFrame(data)
    
    # Escape pipe characters in string columns
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.replace('|', '\\|')
    
    # Return formatted markdown table with alignment
    return df.to_markdown(index=False, tablefmt="pipe")

def stream_text(text: str, delay: float = 0.001) -> None:
    """Stream text with a typing effect."""
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)
    
    return placeholder

# Main app layout
st.markdown("""
    # WebScraperAPI - Convert Websites to Structured Data
    Transform any website into structured data using Firecrawl
""")



# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    # Website URL input
    website_url = st.text_input("Enter Website URL", placeholder="https://example.com")
    
    st.divider()
    
    # Schema Builder
    st.subheader("Schema Builder (Optional)")
    
    # Initialize action tracking in session state if not exists
    if "last_action" not in st.session_state:
        st.session_state.last_action = None
    
    # Create a list to store indexes of fields to remove
    fields_to_remove = []
    
    for i, field in enumerate(st.session_state.schema_fields):
        col1, col2, col3 = st.columns([2, 1, 0.5])
        
        with col1:
            field["name"] = st.text_input(
                "Field Name",
                value=field["name"],
                key=f"name_{i}",
                placeholder="e.g., company_mission"
            )
        
        with col2:
            field["type"] = st.selectbox(
                "Type",
                options=["str", "bool", "int", "float"],
                key=f"type_{i}",
                index=0 if field["type"] == "str" else ["str", "bool", "int", "float"].index(field["type"])
            )
        
        with col3:
            # Only show remove button if there's more than one field
            if len(st.session_state.schema_fields) > 1:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.last_action = "remove"
                    fields_to_remove.append(i)

    # Remove marked fields
    for index in sorted(fields_to_remove, reverse=True):
        st.session_state.schema_fields.pop(index)

    if len(st.session_state.schema_fields) < 5:  # Limit to 5 fields
        if st.button("Add Field ➕"):
            if st.session_state.last_action != "remove":
                st.session_state.schema_fields.append({"name": "", "type": "str"})
            st.session_state.last_action = "add"

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the website..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        if not website_url:
            st.error("Please enter a website URL first!")
        else:
            try:
                with st.spinner("Extracting data from website..."):
                    app = load_app()
                    schema = create_schema_from_fields(st.session_state.schema_fields)
                    print(f"Generated Schema: {schema}")
                    extract_params = {
                        'prompt': prompt
                    }
                    if schema:
                        extract_params['schema'] = schema
                        
                    data = app.extract(
                        [website_url],
                        extract_params
                    )
                    print(f"Extracted Data: {data}")
                    if 'data' not in data:
                        st.error("No data received from the API")
                        st.stop()
                    
                    # Handle different data formats
                    if isinstance(data['data'], (list, dict)):
                        # Convert dict to list if necessary
                        data_list = data['data'] if isinstance(data['data'], list) else [data['data']]
                        table = convert_to_table(data_list)
                        df = pd.DataFrame(data_list)
                        
                        placeholder = stream_text(table)
                        st.session_state.messages.append({"role": "assistant", "content": table})

                        # Add download buttons only if we have valid data
                        st.download_button(
                            label="Download as JSON",
                            data=json.dumps(data, indent=2),
                            file_name="extracted_data.json",
                            mime="application/json"
                        )

                        csv_data = df.to_csv(index=False)
                        st.download_button("Download as CSV", csv_data, "extracted_data.csv", "text/csv")
                    else:
                        st.error("Unexpected data format received")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please check your API key and try again")

# Footer
st.markdown("---")

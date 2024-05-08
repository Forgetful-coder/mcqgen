import os
import json
import pandas as pd
import traceback
import streamlit as st
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.MCQGenerator import generate_review_chain
from src.mcq_generator.logger import logging
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Load response JSON
response_json_path = '/Users/aayushaggarwal/Desktop/mcqgen/Response.json'
with open(response_json_path, 'r') as file:
    response_json = json.load(file)

# Create the title
st.title('MCQ Generator Application ✅ ⛓️')

# User inputs form
with st.form('user_inputs'):
    # File upload
    uploaded_file = st.file_uploader('Upload a PDF or text file')

    # MCQ input
    mcq_count = st.number_input("Number of MCQ's", max_value=50, min_value=3)

    # Subject
    subject = st.text_input('Enter your Subject', max_chars=20, placeholder='Subject')

    # Tone
    tone = st.text_input('Enter difficulty level', max_chars=20, placeholder='Simple')

    # Add button
    button = st.form_submit_button('Create MCQs')

    # Check if button is clicked and all information is provided
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner('Generating...'):
            try:
                # Read the file
                text = read_file(uploaded_file)

                # Generate MCQs
                with get_openai_callback() as cb:
                    response = generate_review_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(response_json)
                    })

                # Log token and cost information
                logging.info(f"Total Tokens: {cb.total_tokens}")
                logging.info(f"Prompt Tokens: {cb.prompt_tokens}")
                logging.info(f"Completion Tokens: {cb.completion_tokens}")
                logging.info(f"Total Cost: {cb.total_cost}")

                # Display MCQs and review
                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    if quiz:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            st.write("MCQ Data:")
                            st.write(table_data)
                            df = pd.DataFrame(table_data)
                            df.index += 1  # Adjust index to start from 1
                            st.write("MCQ DataFrame:")
                            st.write(df)
                            # Display DataFrame in Streamlit app
                            st.table(df)

                            # Add download button for CSV
                            csv = df.to_csv(index=False)
                            b64 = base64.b64encode(csv.encode()).decode()
                            href = f'<a href="data:file/csv;base64,{b64}" download="mcq_data.csv">Download CSV</a>'
                            st.markdown(href, unsafe_allow_html=True)
                        else:
                            st.error('Error in table data')
                    else:
                        st.error('No quiz found in response')
                else:
                    st.write(response)

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                traceback.print_exc()
                st.error('An error occurred during generation')
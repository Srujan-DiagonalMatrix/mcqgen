import os, json, traceback, pandas as pd, streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import quiz_review_sequential_chain
from src.mcqgenerator.logger import logging

# command to run the application - streamlit run StreamlitAPP.py

# loading json file
with open('/Users/alikanti/Documents/GenAI/mcqgen/Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

# Create title for the APP.
st.title("MCQs Creator Application with LangChain 🦜⛓️")

# creating form with streamlit form
with st.form("user_inputs"):

    # upload file
    uploaded_files = st.file_uploader("Choose a PDF/txt file")

    # Number of fields to generate
    mcq_count = st.number_input("Enter the number of MCQs to generate", min_value=3, max_value=10, value=8)

    # enter subject line
    subject=st.text_input("Enter the subject of the MCQs",max_chars=20)

    # enter tone
    tone=st.text_input("Enter the level of complexity",max_chars=20)

    # submit button
    button=st.form_submit_button("Generate MCQs")

    # Check if buttons is clicked and all fields are filled
    if button and uploaded_files and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_files)
                with get_openai_callback() as cb:
                    response=quiz_review_sequential_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        try:
                            print(f"Raw quiz data before cleaning: {quiz}")
                            if isinstance(quiz, str) and quiz.startswith("### RESPONSE_JSON"):
                                quiz = quiz.replace("### RESPONSE_JSON", "").strip()
                            print(f"Cleaned quiz data: {quiz}")

                            table_data = get_table_data(quiz)

                            if table_data:
                                df = pd.DataFrame(table_data).T  # Transpose so each question is a row
                                df.reset_index(drop=True, inplace=True)  # Ensure index is numeric
                                df.index = df.index + 1  # Increment index by 1
                                st.table(df)
                                st.text_area(label="Review", value=response.get("review", ""))
                            else:
                                st.error("Table data is empty.")
                        except ValueError as e:
                            st.error(f"Error processing quiz data: {e}")
                    else:
                        st.error("Quiz data is not available.")
                else:
                    st.error("Invalid response format.")
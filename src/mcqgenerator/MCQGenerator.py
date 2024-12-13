import os, pandas as pd
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# load environment variables from .env file
load_dotenv()

# get OPENAI key from environment variables
key=os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model
llm = ChatOpenAI(
    openai_api_key=key,
    model="gpt-3.5-turbo",
    temperature=0.3
)

# Define the first prompt for quiz generation
template1 = """
Text: {text}
You are an expert MCQ maker. Given the above text, create {number} multiple choice questions for {subject} students in {tone} tone.
Make sure questions are not repeated and are aligned with the text.
Format the response as:
### RESPONSE_JSON
{response_json}
"""
quiz_generation_prompt = PromptTemplate.from_template(template1)

# Create the LLMChain for quiz generation
quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz"  # The output will be stored under this key
)

# Define the second prompt for quiz review
template2 = """
You are an expert English grammarian and writer. Analyze the following quiz for {subject} students, \
evaluating if it's appropriate for their level. Use up to 50 words for the analysis. If changes are needed, update the questions.
Quiz:
{quiz}
"""
quiz_review_prompt = PromptTemplate.from_template(template2)

# Create the LLMChain for quiz review
review_chain = LLMChain(
    llm=llm,
    prompt=quiz_review_prompt,
    output_key="review"  # The output will be stored under this key
)

ivariables=["text", "number", "subject", "tone", "response_json"]
opvariables=["quiz", "review"]

# Combine both chains into a SequentialChain
quiz_review_sequential_chain = SequentialChain(
    chains=[quiz_chain, review_chain],  # Run quiz generation followed by review
    input_variables=ivariables,
    output_variables=opvariables,
    verbose=True
)

# Example input for the sequential chain
inputs = {
    "text": "Artificial intelligence is revolutionizing the world.",
    "number": 5,
    "subject": "Technology",
    "tone": "formal",
    "response_json": "{}",
}

# Execute the sequential chain
results = quiz_review_sequential_chain(inputs)

# Extract the results
quiz = results["quiz"]
review = results["review"]

# Convert the quiz and review outputs into DataFrames for better visualization
quiz_df = pd.DataFrame([quiz])  # Wrapping in a list to create a DataFrame
review_df = pd.DataFrame([review])

# Print the DataFrames
print("Quiz:")
print(quiz_df)
print("\nReview:")
print(review_df)

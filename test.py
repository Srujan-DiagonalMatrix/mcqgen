from src.mcqgenerator.logger import logging

logging.info("This is a test message")

import os, json, traceback, pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.utils import logging
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PrompTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

print("This is a test message")
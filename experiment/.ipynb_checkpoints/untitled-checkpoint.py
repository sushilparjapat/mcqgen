import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2
import os
import json
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file , get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain


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
import sys
print(sys.path)

from src.mcqgenerator.utils import read_file , get_table_data
from src.mcqgenerator.logger import logging




KEY = os.getenv("GOOGLE_API_KEY")

os.environ["GOOGLE_API_KEY"] = getpass.getpass(KEY)

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3, convert_system_message_to_human=True) # set the convert_system_message_to_human to true 

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables = ["text","number","subject","tone","response_json"],
    template=template
)

quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)

template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}


"""


quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=template2)


review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True)

# NUMBER=5 
# SUBJECT="machine learning"
# TONE="simple"


# file_path = "/home/sushil_2211mc24/mcqgen/data.txt"

# with open(file_path, 'r') as file:
#     TEXT = file.read()


# #https://python.langchain.com/docs/modules/model_io/llms/token_usage_tracking

# #How to setup Token Usage Tracking in LangChain
# with get_openai_callback() as cb:
#     response=generate_evaluate_chain(
#         {
#             "text": TEXT,
#             "number": NUMBER,
#             "subject":SUBJECT,
#             "tone": TONE,
#             "response_json": json.dumps(RESPONSE_JSON)
#         }
#         )
# response
# print(response.get("quiz").split("RESPONSE_JSON")[1])
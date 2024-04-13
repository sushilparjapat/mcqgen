import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2
import os
import json
import pandas as pd
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI

from src.mcqgenerator.utils import read_file , get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
import getpass
from dotenv import load_dotenv

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key,value in quiz_dict.items():
            mcq = value["mcq"]
            options=" || ".json(
                [
                    f"{ option}-> {option_value}" for option,option_value in value["options"].items()
                ]
            )
            correct=value["correct"]
            quiz_table_data.append({"MCQ":mcq,"Choices":options,"Correct":correct})


      
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False

with open('/home/sushil_2211mc24/mcqgen/Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

st.title("MCQs Creater Application with Langchain ")

with st.form("user_inputs"):
    #File upload
    uploaded_file = st.file_uploader("Upload a pdf or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3,max_value=50)

    #Subject
    subject=st.text_input("Input Subject",max_chars=20)
    
    #quiz Tone
    tone=st.text_input("Complexityv Level of Questions",max_chars=20,placeholder="Simple")

    #add Button
    button=st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                #######################################################################################################################



                #########################################################################################################################
                text=read_file(uploaded_file)
                #coutn tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    # Extract the quiz data from the response
                    #quiz = response.get("quiz",None)
                    quiz = response.get("quiz").split("RESPONSE_JSON")[1]

                    if quiz is not None:
                        #table_data=get_table_data(quiz)
     
#################################################################################################################################################
                        try:
                                # convert the quiz from a str to dict
                            quiz_dict = json.loads(quiz)
                            quiz_table_data = []
                            for key, value in quiz_dict.items():
                                mcq = value["mcq"]
                                options = " | ".join(
                                    [
                                         f"{option}: {option_value}"
                                        for option, option_value in value["options"].items()
                                        ]
                                    )
                                correct = value["correct"]
                                quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

                        except Exception as e:
                             traceback.print_exception(type(e),e,e.__traceback__)
                             print("False")


################################################################################################################################################
                        if quiz_table_data is not None:
                            df=pd.DataFrame(quiz_table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in atext box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)


## it is helping file 
import PyPDF2
import os
import json
import traceback
import pandas as pd

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            print(file)
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            print("sushil")
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            print(f"Error message from PyPDF2: {str(e)}")
            raise Exception("error reading the PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
        )

def get_table_data(quiz_str):
    try:
        # convert the quiz from a str to dict
        quiz_dict = json.loads(quiz_str)
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


      
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False
data = ''' {"1": {"mcq": "Who coined the term 'machine learning'?", "options": {"a": "Donald Hebb", "b": "Arthur Samuel", "c": "Walter Pitts", "d": "Warren McCulloch"}, "correct": "b"}, "2": {"mcq": "What was the purpose of the 'Cybertron' machine?", "options": {"a": "To play checkers", "b": "To analyze sonar signals", "c": "To recognize characters", "d": "To trade stocks"}, "correct": "b"}, "3": {"mcq": "According to Tom M. Mitchell's definition, what is the goal of machine learning?", "options": {"a": "To understand human cognitive processes", "b": "To improve performance on specific tasks", "c": "To create artificial intelligence", "d": "To classify data"}, "correct": "b"}, "4": {"mcq": "What are the two main objectives of modern-day machine learning?", "options": {"a": "Classification and prediction", "b": "Pattern recognition and reinforcement learning", "c": "Data mining and natural language processing", "d": "Image processing and speech recognition"}, "correct": "a"}, "5": {"mcq": "Which of the following is NOT a researcher who contributed to the development of machine learning?", "options": {"a": "Arthur Samuel", "b": "Donald Hebb", "c": "Alan Turing", "d": "Warren McCulloch"}, "correct": "c"}}''' 

print(type(data))

ans = get_table_data(data)
print(ans)
df=pd.DataFrame(ans)
df.index=df.index+1

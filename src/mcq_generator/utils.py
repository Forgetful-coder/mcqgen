import os
import PyPDF2
import json
import traceback
from src.mcq_generator.logger import logging

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text=""
            for pages in pdf_reader:
                text+= pages.extract_text()
            logging.info('Text extracted')
            return text
        except Exception as e:
            logging.info('An error occured: %s',e)
            raise Exception('error reading the PDF File')

    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise Exception("unsupported file format only pdf or txt file allowed")
    
def get_table_data(quiz_str):
    try:
        # Remove prefix if present
        if quiz_str.startswith("### RESPONSE_JSON"):
            quiz_str = quiz_str[len("### RESPONSE_JSON"):].strip()

        # Parse JSON data
        quiz_dict = json.loads(quiz_str)

        # Construct DataFrame
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        logging.error('An error occurred: %s', e)
        return False
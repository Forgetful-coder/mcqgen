import os
import json
import pandas as pd
import traceback
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
import streamlit as st
from src.mcq_generator.logger import logging


#loading the json file


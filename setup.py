from setuptools import setup,find_packages

setup(
    name = 'mcqgen',
    version='0.0.1',
    author= 'Aayush Aggarwal',
    author_email='aayushaggarwal243@gmail.com',
    install_requires=['openai','langchain','python-dotenv','PyPDF2','streamlit'],
    find_packages=find_packages()
)
# import os
# import streamlit as st
# from PIL import Image
# from dotenv import load_dotenv
# from lyzr import ChatBot
# from lyzr_automata.ai_models.openai import OpenAIModel
# from lyzr_automata import Agent, Task
# from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
# from utils import save_uploaded_file, remove_existing_files
# import PyPDF2

# load_dotenv()
# api = os.getenv("OPENAI_API_KEY")

# data = "data"
# os.makedirs(data, exist_ok=True)

# st.title("Assignment Grader and Chatbot")
# st.markdown("### Welcome to the Assignment Grader and Chatbot!")
# st.markdown("Upload your assignment file and provide the rubric to get a grade, and ask questions about the graded assignment.")

# # Initialize session state variables
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "chatbot" not in st.session_state:
#     st.session_state.chatbot = None

# if "uploaded_files" not in st.session_state:
#     st.session_state.uploaded_files = []

# if "file_upload_key" not in st.session_state:
#     st.session_state.file_upload_key = 0

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "rubric_content" not in st.session_state:
#     st.session_state.rubric_content = ""

# vector_store_params = {
#     "vector_store_type": "WeaviateVectorStore",
#     "index_name": "RonitPatil"
# }

# def file_checker():
#     file = []
#     for filename in os.listdir(data):
#         file_path = os.path.join(data, filename)
#         file.append(file_path)
#     return file

# def reset_file_uploader():
#     st.session_state.file_upload_key += 1
#     st.session_state.uploaded_files = []

# def get_file_extension(file_name):
#     _, file_extension = os.path.splitext(file_name)
#     return file_extension.lower().lstrip('.')

# def read_assignment_content(file):
#     extension = get_file_extension(file.name)
#     content = ""
#     if extension == "pdf":
#         reader = PyPDF2.PdfReader(file)
#         for page in range(len(reader.pages)):
#             content += reader.pages[page].extract_text()

# def grade_assignment(assignment_content, rubric_content):
#     open_ai_text_completion_model = OpenAIModel(
#         api_key=api,
#         parameters={
#             "model": "gpt-4-turbo-preview",
#             "temperature": 0.2,
#             "max_tokens": 1500,
#         },
#     )

#     grader_agent = Agent(
#         role='Assignment Grader',
#         prompt_persona=f'You are an expert ASSIGNMENT GRADER. Your task is to GRADE the assignment based on the provided rubric.'
#     )

#     task = Task(
#         name="Grade Assignment",
#         model=open_ai_text_completion_model,
#         agent=grader_agent,
#         instructions=f"""
# 1. Analyze the provided assignment content and rubric.
# 2. Grade the assignment based on the criteria mentioned in the rubric.
# 3. Provide detailed feedback on each criterion and justify the grade given.
# 4. Give an overall grade for the assignment.

# Assignment Content:
# {assignment_content}

# Rubric Content:
# {rubric_content}
# """
#     )

#     output = LinearSyncPipeline(
#         name="Assignment Grader Pipeline",
#         completion_message="Grading completed",
#         tasks=[task],
#     ).run()

#     return output[0]['task_output']

# # File upload section
# with st.sidebar:
#     with st.container():
#         st.markdown("### Upload Assignment File")
#         assignment_file = st.file_uploader("Upload Assignment", type=['pdf'], key=f"file_uploader_assignment_{st.session_state.file_upload_key}")

#         st.markdown("### Provide Rubric")
#         rubric_content = st.text_area("Paste your rubric here")

#         if assignment_file and rubric_content:
#             save_uploaded_file([assignment_file])
#             st.session_state.uploaded_files.append(os.path.join(data, assignment_file.name))

#             assignment_content = read_assignment_content(assignment_file)

            
#             st.success("Assignment graded. You may ask questions about the grade now.")
#             st.session_state.uploaded_files = []
#             st.session_state.rubric_content = rubric_content

#         if st.button("Remove All Files"):
#             remove_existing_files(data)
#             st.success("All files have been removed.")
#             reset_file_uploader()

# def handle_user_input(user_input):
#     st.chat_message("user").markdown(user_input)
#     response = st.session_state["chatbot"].chat(user_input)
#     st.chat_message("assistant").markdown(response)
#     st.session_state.chat_history.append({"role": "user", "content": user_input})
#     st.session_state.chat_history.append({"role": "assistant", "content": response})

# if "grade_result" in st.session_state:
#     st.markdown("### Grading Result:")
#     st.markdown(st.session_state.grade_result)

# for message in st.session_state.chat_history:
#     with st.chat_message(message["role"]):
#         grade = grade_assignment(assignment_content, rubric_content)
#         st.markdown(grade)

# if st.session_state.chatbot:
#     if user_input := st.chat_input("Ask me anything about the graded assignment"):
#         handle_user_input(user_input)
import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from utils import save_uploaded_file, remove_existing_files
import PyPDF2

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

data = "data"
os.makedirs(data, exist_ok=True)

st.set_page_config(
    page_title="Assignment Grader and Chatbot",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.title("Assignment Grader and Chatbot")
st.markdown("### Welcome to the Assignment Grader and Chatbot!")
st.markdown("Upload your assignment file and provide the rubric to get a grade, and ask questions about the graded assignment.")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = None

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "file_upload_key" not in st.session_state:
    st.session_state.file_upload_key = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "rubric_content" not in st.session_state:
    st.session_state.rubric_content = ""

if "grade_result" not in st.session_state:
    st.session_state.grade_result = ""

vector_store_params = {
    "vector_store_type": "WeaviateVectorStore",
    "index_name": "RonitPatil"
}

def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)
    return file

def reset_file_uploader():
    st.session_state.file_upload_key += 1
    st.session_state.uploaded_files = []

def get_file_extension(file_name):
    _, file_extension = os.path.splitext(file_name)
    return file_extension.lower().lstrip('.')

def read_assignment_content(file):
    extension = get_file_extension(file.name)
    content = ""
    if extension == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in range(len(reader.pages)):
            content += reader.pages[page].extract_text()
    return content

def grade_assignment(assignment_content, rubric_content):
    open_ai_text_completion_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )

    grader_agent = Agent(
        role='Assignment Grader',
        prompt_persona=f'You are an expert ASSIGNMENT GRADER. Your task is to GRADE the assignment based on the provided rubric.'
    )

    task = Task(
        name="Grade Assignment",
        model=open_ai_text_completion_model,
        agent=grader_agent,
        instructions=f"""
1. Analyze the provided assignment content and rubric.
2. Grade the assignment based on the criteria mentioned in the rubric.
3. Provide detailed feedback on each criterion and justify the grade given.
4. Give an overall grade for the assignment.

Assignment Content:
{assignment_content}

Rubric Content:
{rubric_content}
"""
    )

    output = LinearSyncPipeline(
        name="Assignment Grader Pipeline",
        completion_message="Grading completed",
        tasks=[task],
    ).run()

    return output[0]['task_output']

# File upload section
with st.sidebar:
    with st.container():
        st.markdown("### Upload Assignment File")
        assignment_file = st.file_uploader("Upload Assignment", type=['pdf'], key=f"file_uploader_assignment_{st.session_state.file_upload_key}")

        st.markdown("### Provide Rubric")
        rubric_content = st.text_area("Paste your rubric here")

        if assignment_file and rubric_content:
            save_uploaded_file([assignment_file])
            st.session_state.uploaded_files.append(os.path.join(data, assignment_file.name))

            assignment_content = read_assignment_content(assignment_file)

            grade = grade_assignment(assignment_content, rubric_content)
            st.session_state.grade_result = grade
            st.success("Assignment graded. You may ask questions about the grade now.")
            st.session_state.uploaded_files = []
            st.session_state.rubric_content = rubric_content

        if st.button("Remove All Files"):
            remove_existing_files(data)
            st.success("All files have been removed.")
            reset_file_uploader()

def handle_user_input(user_input):
    st.chat_message("user").markdown(user_input)
    response = st.session_state["chatbot"].chat(user_input)
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

if "grade_result" in st.session_state:
    st.markdown("### Grading Result:")
    st.markdown(st.session_state.grade_result)

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.chatbot:
    if user_input := st.chat_input("Ask me anything about the graded assignment"):
        handle_user_input(user_input)

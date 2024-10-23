import base64
import json
from docx import Document
from io import BytesIO
from fastapi import APIRouter
from ..schemas.build_json import BuildJsonIn, BuildJsonOut

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

router = APIRouter()


schema = """{
header: {
           fullName: string,
           jobTitle: string,
           email: string,
           phoneNumber: string,
           summary: string,
         },
         coreExpertise: {
           Software: string[],
           Coding: string[],
           Languages: string[],
         },
         keyProjects: {
           [key: string]: string,
         },
         professionalExperience: [{
           date: string,
           title: string,
           company: string,
           description: string[],
         }],
         education:  {
           title: string,
           institute: string,
           description: string[],
         },
} 
"""
def get_user_info_object(user_info: set, development: bool):
    template = """Question: {user_info} 
    can u please convert this text to the following schema?
    {schema}

    Answer: give me only the json, make sure its a valid json string"""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.2")
    chain = prompt | model
    if(development): 
        return "{\"header\": {\"fullName\": \"Dor Ron\", \"jobTitle\": \"Full Stack Developer\", \"email\": \"Dorron139@gmail.com\", \"phoneNumber\": \"+972 (54) 300-2278\", \"summary\": \"Positive and social person, independent, and highly motivated to continue learning and developing.\"}, \"coreExpertise\": {\"Software\": [\"Node.js\", \"React.js\", \"Docker\"], \"Coding\": [\"JavaScript\", \"Typescript\", \"HTML\", \"CSS\"], \"Languages\": [\"Hebrew\", \"English\"]}, \"keyProjects\": {\"Qwad\": \"Implemented a full native front-end application using React Native.\", \"Tech4Israel\": \"Implemented a small responsive front-end application using React.js.\"}, \"professionalExperience\": [{\"date\": \"2022 - Present\", \"title\": \"Full Stack Developer | Sapiens (Engage.com, Acquired by Sapiens)\", \"company\": \"Sapiens (Engage.com, Acquired by Sapiens)\", \"description\": [\"Managed one of the company's largest and most profitable clients...\", \"Developed and delivered features using Node.js and React.js...\", \"Wrote and maintained comprehensive test suites with Jest and Supertest...\", \"Specialized in backend development with hands-on experience in Docker...\"]}], \"education\": {\"title\": \"B.Sc. - Industrial Engineering\", \"institute\": \"Afeka Academic College of Engineering, Tel Aviv, Israel.\", \"description\": [\"Excellent scholarship for outstanding students program Smart-Up.\"]}}"
    return chain.invoke({"schema": schema, "user_info": user_info})

# @router.post('/build-user-info', response_model=BuildJsonOut)
@router.post('/build-user-info')
def build_user_info(data: BuildJsonIn):
    try:
        base64_user_resume = data.base64_user_resume
        
        docx_buffer = base64.b64decode(base64_user_resume)
        docx_bytes = BytesIO(docx_buffer)

        document = Document(docx_bytes)

        # TODO: handle the different types of docx structure
        document_text = set()
        for table in document.tables:
            for col in table.columns:
                for cell in col.cells:
                    text = cell.text
                    if text:
                        document_text.add(text)

        # TODO: drop this development shit
        str_user_info = get_user_info_object(document_text, True)

        return str_user_info
    except Exception as error:
        print('there is an error', error)
        return {
            "msg": str(error)
        }
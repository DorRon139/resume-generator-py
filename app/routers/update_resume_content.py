import base64
import json
from fastapi import APIRouter
from ..schemas.api_schemas import UpdateResumeContentIn, UpdateResumeContentOut 

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

router = APIRouter()

def get_updated_user_info(user_info: dict, job_description: str):
    template = """Question: based on this job description:
    {job_description}

    and this data about my cv:
    {user_info}

    Answer: {instructions}"""

    instructions = """you are a proffesional resume builder for high tech companies.
    please don't fabricate skills that I don't have.
    can you please adjust a new content and update the above json
    give me only the json, make sure its a valid json string
    dont change anything that isnt relevant to the job description"""

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.2")
    chain = prompt | model

    return chain.invoke({"job_description": job_description, "user_info": user_info, "instructions": instructions })

@router.post('/update-resume-content')
def update_resume_content(data : UpdateResumeContentIn):
    try:
        job_description = data.job_description
        base_user_info = data.base_user_info

        result = get_updated_user_info(base_user_info, job_description)
        return result
    except Exception as error:
        print('there is an error', error)
        return {
            "msg": str(error)
        }
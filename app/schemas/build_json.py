from typing import List
from pydantic import BaseModel

class Header(BaseModel):
    fullName: str
    jobTitle: str
    email: str
    phoneNumber: str
    summary: str

class CoreExpertise(BaseModel):
    Software: str
    Coding: str
    Languages: str

class ProfessionalExperience(BaseModel):
    date: str
    title: str
    company: str
    description: List[str]

class Education(BaseModel):
    title: str
    institute: str
    description: List[str]


class BaseUserInfo(BaseModel):
    header: Header
    coreExpertise: CoreExpertise
    keyProjects: object
    professionalExperience: List[ProfessionalExperience]
    education:  Education


class BuildJsonIn(BaseModel):
    base64_user_resume: str

class BuildJsonOut(BaseModel):
    success: bool
    base_user_info: BaseUserInfo






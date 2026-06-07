# prompt.py
# define all basic data structure
from pydantic import BaseModel

# prompt
class PromptCreate(BaseModel):
    name:str

class PromptResponse(BaseModel):
    name:str
    id:int

#prompt_version
class VersionCreate(BaseModel):
    content:str
    tags:list[str]

class VersionResponse(BaseModel):
    prompt_id:int
    version_id:int

#render
class RenderRequest(BaseModel):
    variables:dict[str,str]

class RenderResponse(BaseModel):
    prompt_id:int
    version_id:int
    rendered:str

# generage
class GenerateRequest(BaseModel):
    variables:dict[str,str]

class GenerateResponse(BaseModel):
    prompt_id:int
    version_id:int
    rendered:str
    output:str
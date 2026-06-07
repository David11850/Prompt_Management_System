# api.py
# all route api
from fastapi import HTTPException
from fastapi import FastAPI,HTTPException
from dotenv import load_dotenv

app=FastAPI()
load_dotenv()

from schemas.prompt import PromptCreate
from schemas.prompt import PromptResponse
from schemas.prompt import PromptRenderRequest
from schemas.prompt import PromptRenderResponse
from schemas.prompt import PromptGenerateRequest
from schemas.prompt import PromptGenerateResponse

from models.llm_service import llm_generate

# create prompt and push to db
@app.post("/prompts",response_model=PromptResponse)
async def post_prompt(prompt:PromptCreate):
    global next_id
    response=PromptResponse(
        id=next_id,
        name=prompt.name,
        content=prompt.content,
        tags=prompt.tags
    )
    virtual_db[next_id]=response
    next_id+=1
    return response

# get targeted prompt using id from db
@app.get("/prompts/{prompt_id}",response_model=PromptResponse)
async def get_prompt(prompt_id:int):
    if prompt_id in virtual_db:
        response=virtual_db[prompt_id]
        return response
    else:
        raise HTTPException(status_code=404,detail="prompt not found")

# get all prompt from db
@app.get("/prompts",response_model=list[PromptResponse])
async def get_all_prompt(tag:str|None=None):
    if tag==None:
        return list(virtual_db.values())
    result=[]
    for prompt in virtual_db.values():
        if tag in prompt.tags:
            result.append(prompt)
    return result

# render prompt
@app.post("/prompts/{prompt_id}/render",response_model=PromptRenderResponse)
async def render_prompt(prompt_id:int,request:PromptRenderRequest):
    if prompt_id not in virtual_db:
        raise HTTPException(status_code=404,detail="prompt not found")
    prompt=virtual_db[prompt_id]
    try:
        rendered=prompt.content.format(**request.variables)
    except KeyError:
        raise HTTPException(status_code=400,detail="missing variable")
    return PromptRenderResponse(prompt_id=prompt_id,rendered=rendered)

@app.post("/prompts/{prompt_id}/generate",response_model=PromptGenerateResponse)
async def call_llm(prompt:id,request:PromptRenderRequest):
    generate_request:PromptGenerateRequest()
    llm_generate(id,request)
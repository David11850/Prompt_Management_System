# prompt_api.py
from fastapi import APIRouter,HTTPException

from schemas.prompt import PromptCreate
from schemas.prompt import PromptResponse
from schemas.prompt import VersionCreate
from schemas.prompt import VersionResponse

from database.database import create_prompt
from database.database import get_prompt
from database.database import get_all_prompts
from database.database import create_version

router=APIRouter()

@router.post("/prompts",response_model=PromptResponse)
def post_prompt_api(request:PromptCreate):
    prompt_id=create_prompt(request.name)
    return PromptResponse(
        id=prompt_id,
        name=request.name
    )

@router.get("/prompts/{prompt_id}",response_model=PromptResponse)
def get_target_prompt_api(prompt_id:int):
    # in case of no such prompt_id
    # so take the value error from db and raise http error
    try:
        prompt:dict=get_prompt(prompt_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)    
        )
    # valid prompt_id
    return PromptResponse(
        id=prompt["id"],
        name=prompt["name"]
    )

@router.get("/prompts",response_model=list[PromptResponse])
def get_all_prompts_api():
    prompt=get_all_prompts()
    return prompt

@router.post("/prompts/{prompt_id}/versions",response_model=VersionResponse)
def post_prompt_version_api(
    prompt_id:int,
    request:VersionCreate
):
    prompt_version_id=create_version(prompt_id,request.content,request.tags)
    return VersionResponse(
        prompt_id=prompt_id,
        version_id=prompt_version_id[1]
    )
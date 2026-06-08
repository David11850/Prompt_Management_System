# prompt_api.py
from fastapi import APIRouter,HTTPException

from schemas.prompt import PromptCreate
from schemas.prompt import PromptResponse
from schemas.prompt import VersionCreate
from schemas.prompt import VersionResponse
from schemas.prompt import RenderRequest
from schemas.prompt import RenderResponse

from service.prompt_service import get_target_prompt
from service.prompt_service import get_all_prompts_from_db
from service.prompt_service import post_prompt
from service.prompt_service import render_version
from service.prompt_service import render_latest_prompt
from service.version_service import get_all_version_prompt
from service.version_service import post_prompt_version_to_db
from service.version_service import get_latest_version_from_db

router=APIRouter()

# prompt
# create prompt
@router.post("/prompts",response_model=PromptResponse)
def post_prompt_api(request:PromptCreate):
    return post_prompt(request)

# get prompt through id
@router.get("/prompts/{prompt_id}",response_model=PromptResponse)
def get_target_prompt_api(prompt_id:int):
    try:
        prompt=get_target_prompt(prompt_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=e
        )
    return prompt

# get all prompts
@router.get("/prompts",response_model=list[PromptResponse])
def get_all_prompt_api():
    return get_all_prompts_from_db()


# version
# add new version to a prompt
@router.post("/prompts/{prompt_id}/versions",response_model=VersionResponse)
def post_prompt_vetsion_api(prompt_id:int,request:VersionCreate):
    return post_prompt_version_to_db(prompt_id,request)

# get all version of a prompt
@router.get("/prompts/{prompt_id}/versions",response_model=list[VersionResponse])
def get_all_version_prompt_api(prompt_id:int):
    return get_all_version_prompt(prompt_id)

# render
@router.post("/prompt/{prompt_id}/render",response_model=RenderResponse)
def render_latest_version_api(prompt_id:int,request:RenderRequest):
    version=get_latest_version_from_db(prompt_id)
    rendered_text=render_latest_prompt(prompt_id,request.variables)
    return RenderResponse(
        prompt_id=prompt_id,
        version_id=version,
        rendered=rendered_text
    )

@router.post("/prompt/{prompt_id}/{version}/render",response_model=RenderResponse)
def render_target_version_api(prompt_id:int,version:int,request:RenderRequest):
    rendered_text=render_version(prompt_id,version,request.variables);
    return RenderResponse(
        prompt_id=prompt_id,
        version_id=version,
        rendered=rendered_text
    )
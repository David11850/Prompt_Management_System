# prompt_service.py
from schemas.prompt import PromptCreate
from schemas.prompt import PromptResponse
from schemas.prompt import VersionCreate
from schemas.prompt import VersionResponse

from database.database import get_prompt
from database.database import get_all_prompts
from database.database import create_prompt
from database.database import create_version
from database.database import get_target_version
from database.database import get_latest_version
from database.database import get_all_versions

# get prompt
def get_target_prompt(prompt_id:int)->PromptResponse:
    # in case of no such prompt_id
    # so take the value error from db and raise http error
    try:
        prompt:dict=get_prompt(prompt_id)
    except ValueError as e:
        raise ValueError("no such prompt")
    # valid prompt_id
    return PromptResponse(
        id=prompt["id"],
        name=prompt["name"]
    )

def get_all_prompts_from_db():
    prompt=get_all_prompts()
    return prompt

def post_prompt(request:PromptCreate)->PromptResponse:
    prompt_id=create_prompt(request.name)
    return PromptResponse(
        id=prompt_id,
        name=request.name
    )


# render prompt
# tool function to render target version_info and variables
def render_content(
    version_info:dict,
    variables:dict[str,str]
)->str:
    content=version_info["content"]
    try:
        rendered=content.format(**variables)
    except KeyError as e:
        raise ValueError(f"missing variable:{e}")
    return rendered

# render target version of prompt
def render_version(
    prompt_id:int,
    version:int,
    variables:dict[str,str]
)->str:
    version_info=get_target_version(prompt_id,version)
    return render_content(version_info,variables)

# render the latest version of prompt
def render_latest_prompt(
    prompt_id:int,
    variables:dict[str,str]
)->str:
    version_info=get_latest_version(prompt_id)
    return render_content(version_info,variables)
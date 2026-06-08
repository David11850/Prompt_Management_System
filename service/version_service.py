import json

from schemas.prompt import PromptCreate
from schemas.prompt import PromptResponse
from schemas.prompt import VersionCreate
from schemas.prompt import VersionResponse

from database.database import create_version
from database.database import get_all_versions
from database.database import get_latest_version

# get all version of a prompt
def get_all_version_prompt(prompt_id:int)->list[VersionResponse]:
    all_version:list=get_all_versions(prompt_id)
    result:list[VersionResponse]=[]
    for cur_version in all_version:
        result.append(
            VersionResponse(
                prompt_id=cur_version["prompt_id"],
                version_id=cur_version["version"],
                content=cur_version["content"],
                tags=cur_version["tags"]
            )
        )
    return result

def post_prompt_version_to_db(
    prompt_id:int,
    request:VersionCreate
):
    prompt_version_id=create_version(prompt_id,request.content,request.tags)
    return VersionResponse(
        prompt_id=prompt_id,
        version_id=prompt_version_id[1],
        content=request.content,
        tags=request.tags
    )

def get_latest_version_from_db(prompt_id:int):
    version=get_latest_version(prompt_id)
    return version["version"]
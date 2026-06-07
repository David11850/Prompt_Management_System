# prompt_service.py
from database.database import get_target_version
from database.database import get_latest_version
from database.database import get_all_versions

# get prompt
# list all version of a prompt
def list_prompt_versions(prompt_id:int):
    version_info:list=get_all_versions(prompt_id)
    return version_info


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
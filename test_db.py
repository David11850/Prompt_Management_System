from database.database import create_prompt
from database.database import get_prompt
from database.database import create_version

# create prompt
prompt_id=create_prompt("answer2")
print(prompt_id)

# get prompt
if(prompt_id==-1):
    print("create prompt error")
    exit(-1)
row=get_prompt(prompt_id)
print(row)

# get version
content:str="answer {question} in {language}"
tags:list[str]=["question","language"]
version_id=create_version(prompt_id,content,tags)
print(version_id)
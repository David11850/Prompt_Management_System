# llm_service.py
# call different llm model
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from openai import OpenAI

from schemas.prompt import PromptGenerateRequest
from schemas.prompt import PromptGenerateResponse

# LLm caller
async def llm_generate(prompt_id:int,request:PromptGenerateRequest):
    if prompt_id not in virtual_db:
        raise HTTPException(status_code=404,detail="prompt not found")
    prompt:str=virtual_db[prompt_id].content
    try:
        rendered_prompt:str=prompt.format(**request.variables)
        output:str=await call_deepseek(rendered_prompt)
    except KeyError:
        raise HTTPException(status_code=400,detail="missing variable")
    return PromptGenerateResponse(
        prompt_id=prompt_id,
        rendered_prompt=rendered_prompt,
        output=output
    )

async def call_deepseek(rendered_prompt:str)->str:
    api_key=os.getenv("DEEPSEEK_API_KEY")
    api_url=os.getenv("DEEPSEEK_URL")
    model=os.getenv("DEEPSEEK_MODEL")
    if not api_key:
        raise HTTPException(status_code=500,detail="DEEPSEEK_API_KEY is not configured")
    if not api_url:
        raise HTTPException(status_code=500,detail="DEEPSEEK_API_URL is not configured")
    if not model:
        raise HTTPException(status_code=500,detail="DEEPSEEK_MODEL is not configured")
    try:
        client=OpenAI(
            api_key=api_key,
            base_url=api_url
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role":"system","content":"you are a code assistant"},
                {"role":"user","content":rendered_prompt}
            ],
            stream=False,
        )
        output=response.choices[0].message.content
        if output is None:
            raise HTTPException(status_code=502,detail="LLM returned empty content")
        return output
    except Exception as e:
        raise HTTPException(status_code=501,detail=f"LLM request dailed {str(e)}")

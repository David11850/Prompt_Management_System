# database.py
import sqlite3
import json

# connect to/open the target sqlite db in the disk
def get_connection():
    conn=sqlite3.connect('./database/prompt_manager.db')
    conn.row_factory=sqlite3.Row
    return conn

# prompt
# create prompt in db with string name
def create_prompt(name:str)->int:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO prompts(name)
        VALUES(?)
    ''',
    (name,))
    conn.commit()
    prompt_id=cursor.lastrowid
    if prompt_id is None:
        return -1
    conn.close()
    return prompt_id

# get prompt with prompt_id
def get_prompt(prompt_id:int)->dict:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        SELECT * 
        FROM prompts
        WHERE id = ?               
    ''',
    (prompt_id,))
    row=cursor.fetchone()
    conn.close()
    if row is None:
        raise ValueError("prompt not found")
    return dict(row)

# get all prompts in db
def get_all_prompts()->list:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        SELECT * 
        FROM prompts
    ''')
    rows=cursor.fetchall()
    conn.close()
    result=[]
    for cur_row in rows:
        result.append(dict(cur_row))
    return result

# version
# tool function to get last version and calculate new version
def get_prompt_latest_version(prompt_id:int)->int:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        SELECT MAX(version)
        FROM prompt_versions
        WHERE prompt_id=?
    ''',
    (prompt_id,))
    raw=cursor.fetchone()
    conn.close()
    if raw[0] is None:
        return 1
    return raw[0]+1

# create a prompt version in prompt_version db
def create_version(
    prompt_id:int,
    content:str,
    tags:list[str]
)->list:
    conn=get_connection()
    cursor=conn.cursor()
    # get last version and calculate new version
    new_version:int=get_prompt_latest_version(prompt_id)
    tags_str=json.dumps(tags)
    # create new row in database
    cursor.execute('''
        INSERT INTO prompt_versions(
            prompt_id,
            version,
            content,
            tags
        )
        VALUES(
            ?,
            ?,
            ?,
            ?
        )               
    ''',
    (prompt_id,new_version,content,tags_str)
    )
    conn.commit()
    versionid=cursor.lastrowid
    conn.close()
    if versionid is None:
        return [-1,-1]
    return [versionid,new_version]

# tool function to convert version_raw to dict
def version_row_to_dict(row)->dict:
    result=dict(row)
    if result.get("tags"):
        result["tags"]=json.loads(result["tags"])
    return result

# get target prompt version in prompt_versoion db
def get_target_version(prompt_id:int,version:int)->dict:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        SELECT * 
        FROM prompt_versions
        WHERE prompt_id=?
        AND version=?
    ''',
    (prompt_id,version))
    raw=cursor.fetchone()
    conn.close()
    if raw is None:
        raise ValueError("no such version or prompt")
    return version_row_to_dict(raw)

# get latest version of the target prompt in prompt_version db
def get_latest_version(prompt_id:int)->dict:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        SELECT *
        FROM prompt_versions
        WHERE prompt_id=? 
        ORDER BY version DESC
        LIMIT 1
    ''',
    (prompt_id,))
    raw=cursor.fetchone()
    conn.close()
    if raw is None:
        raise ValueError("no latest version yet")
    return version_row_to_dict(raw)

# get all version in prompt_version db
def get_all_versions(prompt_id:int)->list:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('''
        SELECT * FROM prompt_versions
        WHERE prompt_id=?
        ORDER BY version ASC
    ''',
    (prompt_id,))
    rows=cursor.fetchall()
    conn.close()
    result:list=[]
    for cur_row in rows:
        row_dict=version_row_to_dict(cur_row)
        result.append(row_dict)
    return result
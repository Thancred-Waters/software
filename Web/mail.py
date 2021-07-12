# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 11:07:44 2021

@author: zc
"""

import uvicorn
from typing import Optional, List
from fastapi import FastAPI, Body, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
#import db

import nest_asyncio

nest_asyncio.apply()

app = FastAPI()

# 配置跨域
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = Field(None, min_length=1)


class UserOut(BaseModel):
    username: str
    state: str = "Accepted"
    email: EmailStr

"""
@app.get("/login")
async def login(user_ID: str, name: str):
    return {"result": db.find(user_ID, name)}
"""

@app.post("/user/", response_model=UserOut, response_model_exclude={"email"})
async def create_user(user: UserIn = Body(...)):
    return user


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    if len(files) == 0:
        raise (HTTPException(status_code=404, detail="Empty File"))
    return {"file_size": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_uploadfiles(file: List[UploadFile] = File(...)):
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    return {"file_names": file.filename}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


uvicorn.run(host="192.168.1.104", port=8000, app=app)

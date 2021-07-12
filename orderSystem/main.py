import uvicorn
import nest_asyncio
from fastapi import FastAPI
from orderSystem.api import server,cook,admin,login
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles

nest_asyncio.apply()
app = FastAPI()

app.mount("/static", StaticFiles(directory="./pic"), name="static")

#配置跨域
origins = ["*",
           "http://192.168.1.121",
           "http://rm-bp1565i7xkloy1o23wo.mysql.rds.aliyuncs.com"
           ]  

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"])  

# 注册api路由
app.include_router(server.router,prefix="/server")
app.include_router(cook.router,prefix="/cook")
app.include_router(admin.router,prefix="/admin")
app.include_router(login.router,prefix="/login")

if __name__ == '__main__':
    uvicorn.run(app=app,host='192.168.1.104', port=8000)
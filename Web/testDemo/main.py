import uvicorn
import nest_asyncio
from fastapi import FastAPI
from testDemo.api import stu
from testDemo.api import item
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

nest_asyncio.apply()
app = FastAPI()

#配置跨域
origins = ["*"]  

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"])  

# 注册api路由
app.include_router(stu.router,prefix="/stu")
app.include_router(item.router,prefix="/item")

if __name__ == '__main__':
    uvicorn.run(app=app,host='192.168.0.154', port=8000)
    
    
   
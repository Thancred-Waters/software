# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:03:33 2021

@author: zc
"""

import uvicorn  # 服务器客户端程序
from typing import Optional, Set  # Optional: 表示参数可选
from fastapi import FastAPI, Query, Path, Body
# Query用于请求数据校验，Path用于路径数据校验，Body表示将数据放在请求体中
# 格式为：ORDER(默认值,min_length,max_length,le,ge,lt,gt)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field  # Json结构体,Field提供内部检验

import nest_asyncio

nest_asyncio.apply()  # 开启异步通信


class Image(BaseModel)
    url: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=100)


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(  # BaseModel内参数检验,本例中限制字符串长度
        None, min_length=0, max_length=10)
    price: float
    tax: Optional[float] = None
    image: Optional[Image] = None
    tag: Optional[Set] = set()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items")
async def add_items(a: int, b: Optional[int] = Query(0, le=1e18)):
    return {"sum": a + b}


@app.get("/items/{item_id}")
async def read_item(item_id: str = Query(None, min_length=5),
                    q: Optional[str] = None, short: Optional[bool] = False):
    item = {"item_id": item_id, "aa": 123}
    if q == "AC":
        item.update({"Accepted": 100})
    else:
        item.update({"Wrong Answer": 0})
    if short:
        item.update({"State": 1})
    return item


@app.post("/old_item")
async def create_old_item(item: Item):
    item = dict(item)
    item["tax"] = item["price"] * 0.05
    return item


@app.post("/new_item")
async def create_new_item(item: Item = Body(..., embed=True),
                          val: Optional[int] = Body(0)):  # ...代表必须参数
    item = dict(item)  # JSON转化为dict
    item["tax"] = item["price"] * 0.05 + val
    return item


@app.put("/test_put/{item_id}")
async def test_put(item_id: int = Path(..., ge=0, le=100)):
    # ge、le表示大于等于、小于等于
    ans = 1
    for i in range(1, item_id + 1):
        ans *= i
    return {"{:d}!".format(item_id): ans}


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tag": []},
}


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str = Path(...), item: Item = Body(...)):
    if not item_id in items.keys():
        raise HTTPException(status_code=404, detail="Key not found.")
    stored_item_data = items[item_id]  # 获取存储的字典
    stored_item_model = Item(**stored_item_data)  # 建立BaseModel
    update_data = item.dict(exclude_unset=True)  # 去除默认值
    updated_item = stored_item_model.copy(update=update_data)  # 更新模型
    items[item_id] = jsonable_encoder(updated_item)  # 重新写回字典
    return updated_item  # 返回更新后的值


uvicorn.run(host="192.168.43.67", port=8000, app=app)

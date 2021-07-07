from fastapi import APIRouter

# 构建api路由
router = APIRouter()

@router.get("/item",tags=["item"])
async def get_item() :
    return {"item":"ok"}


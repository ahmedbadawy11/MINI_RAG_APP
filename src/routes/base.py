from fastapi import FastAPI,APIRouter,Depends
import os
from helpers.config import get_setting, settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/welcome")
async def welcome(app_setting:settings = Depends(get_setting)):

    # setting=get_setting()
    app_name=app_setting.APP_NAME
    app_version=app_setting.APP_VERSION

    
    return {"app name": app_name, "app version": app_version}

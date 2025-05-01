from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_setting, settings
from controllers import DataController,ProjectController
import aiofiles
import os
from models import ResponseSignal
import logging

logger=logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,
                      app_setting:settings=Depends(get_setting)):

    #
    # Validate the file type and size
    # Check if the file type is allowed and the size is within the limit

    data_obj=DataController()
    is_valid ,result_signal= data_obj.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
        )
    project_dir_path=ProjectController().Get_project_path(project_id=project_id)

    file_path,file_id=data_obj.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
    # to handle the file upload, like saving the file to the server no disk space or disk access
    # we will use aiofiles to handle the file upload asynchronously
    try:
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(app_setting.FILE_DEFAULT_CHUNK_SIZE):
                await f.write (chunk)

    except Exception as e:
         logger.error(f"Error while uploading file :{e}")
         return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        
        content={
            "message": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_id":file_id,
            }
    )

    
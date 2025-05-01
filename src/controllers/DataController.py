from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import os
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 #MB to Byte

    def validate_uploaded_file(self,file:UploadFile, ):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        # Check if the file size exceeds the maximum allowed size
        if file.size > self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        # Check if the file is empty
        return True ,ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filepath(self,orig_file_name:str,project_id :str):
        random_Key=self.generate_random_string()

        project_path=ProjectController().Get_project_path(project_id=project_id)

        #clean the orig_file_name to remove any special characters and replace spaces with underscores
        cleaned_file_name=self.get_clean_file_name(
            orig_file_name=orig_file_name
        )
        # create the new file path with the random key and cleaned file name
        new_file_path=os.path.join(
            project_path,
            random_Key + "_"+cleaned_file_name
        )
        # check if the file already exists, if it does, generate a new random key and create a new file path
        # This is to avoid overwriting existing files with the same name
        while os.path.exists(new_file_path):
            random_Key=self.generate_random_string()
            new_file_path=os.path.join(
            project_path,
            random_Key + "_"+cleaned_file_name
            )


        return new_file_path,random_Key + "_"+cleaned_file_name

    ## This function is used to clean the file name by removing any special characters and replacing spaces with underscores.
    ## It is used to avoid any issues with file names when saving the file to the server.
    def get_clean_file_name(self,orig_file_name:str):
        # remove any special characters, except underscore and .
        cleaned_file_name=re.sub(r'[^\w.]','',orig_file_name.strip())

        # replace space with underscore

        cleaned_file_name=cleaned_file_name.replace (" ","_")

        return cleaned_file_name

 
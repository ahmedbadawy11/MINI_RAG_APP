from .BaseController import BaseController
from fastapi import UploadFile
import os

class ProjectController(BaseController):

    def __init__(self):
        super().__init__()

    def Get_project_path(self,project_id:str):
        # Get the project path based on the project ID
        project_dir = os.path.join(self.files_dir,  project_id)
        # Create the project directory if it doesn't exist
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir
from helpers.config import get_setting, settings
import os
import random 
import string


class BaseController:
    def __init__(self):
        self.app_settings = get_setting()
        #os.path.dirname(__file__)  will give the path of the current file (BaseController.py)
        # os.path.dirname(os.path.dirname(__file__)) will give the path of the parent directory of the current file (src)
        self.base_dir= os.path.dirname(os.path.dirname(__file__))   
        self.files_dir = os.path.join(self.base_dir, "assets/files")


    def generate_random_string(self,length :int =12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits ,k=length))
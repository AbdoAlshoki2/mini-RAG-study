from .BaseController import BaseController 
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import os
import re

class DataController(BaseController):

    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self , file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * 1024 * 1024:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_UPLOADED_SUCCESS.value

    def generate_unique_file_name(self, org_file_name: str, project_id: str):

        random_key= self.generate_random_string()  # generate random prefix
        project_path = ProjectController().get_project_dir(project_id=project_id)
        
        cleaned_file_name = self.get_clean_file_name(org_file_name=org_file_name)  # clean the original file name

        new_path = os.path.join(project_path , random_key + "_" + cleaned_file_name)

        while os.path.exists(new_path): # if the file already exists, generate a new random prefix
            random_key= self.generate_random_string()
            new_path = os.path.join(project_path , random_key + "_" + cleaned_file_name)

        return random_key + "_" + cleaned_file_name


    def get_clean_file_name(self, org_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', org_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
        

        
from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    
    def __init__(self , db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]


    async def async_create_project(self , project: Project):
        result = await self.collection.insert_one(project.dict())
        project._id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):

        result = await self.collection.find_one({
            "project_id": project_id
        })


        if result is None:
            project = Project(project_id=project_id)
            project = await self.async_create_project(project=project)
            return project
            
        return Project(**result)

    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        total_docs = await self.collection.count_documents({})
        
        total_pages = (total_docs + page_size - 1) // page_size

        cursor = self.collection.find({}).skip((page - 1) * page_size).limit(page_size)

        projects = [Project(**document) async for document in cursor]

        return projects, total_pages
        
            
        


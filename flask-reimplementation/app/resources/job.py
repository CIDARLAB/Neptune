import uuid
from app.controllers.authentication import AuthenticationController
from app.controllers.filesystem import FileSystem
from app.models.job import Job
from flask import request, send_file
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from pathlib import Path

from app.parameters import FLASK_DOWNLOADS_DIRECTORY
from app.utils import zip_dir


class JobAPI:
    
    class JobBase(Resource):
        """Base API for jobs

        GET - gets all the information for a job
        DELETE - deletes a job (Not implemented)
        PUT - updates a job status (Not implemented)

        """

        def get(self, job_id):
            
            # Verify Access
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            has_access = AuthenticationController.check_user_job_access(user_id, job_id)

            if has_access == False:
                return {'error': 'User does not have access to this job'}, 401

            job = Job.objects.get(job_id=job_id)
            return job.to_json(), 200
        
        # def delete(self):
        #     job_id = request.get_json()['job_id']

        #     # Verify Access
        #     verify_jwt_in_request()
        #     user_id = get_jwt_identity()
        #     has_access = AuthenticationController.check_user_job_access(user_id, job_id)

        #     if has_access == False:
        #         return {'error': 'User does not have access to this job'}, 401
            
        #     # Delete a task

        #     job = Job.objects.get(job_id=job_id)
        #     job.delete()
        #     return {'message': 'Job deleted successfully'}, 200
        
        # def put(self):
        #     job_id= request.get_json()['job_id']
            
        #     # Verify Access
        #     verify_jwt_in_request()
        #     user_id = get_jwt_identity()
        #     has_access = AuthenticationController.check_user_job_access(user_id, job_id)

        #     if has_access == False:
        #         return {'error': 'User does not have access to this job'}, 401
            
        #     job = Job.objects.get(job_id=job_id)
        #     job.update(request.get_json())
        #     return {'message': 'Job updated successfully'}, 200        
        
    class JobZip(Resource):
        def get(self, job_id):
            # Verify Access
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            has_access = AuthenticationController.check_user_job_access(user_id, job_id)

            if has_access == False:
                return {'error': 'User does not have access to this job'}, 401

            job = Job.objects.get(job_id=job_id)
            # Create a new temporary folder downloading the zip
            zip_name = str(uuid.uuid4())
            temp_folder = Path(FLASK_DOWNLOADS_DIRECTORY).joinpath(zip_name).mkdir(parents=True, exist_ok=True)
            
            if temp_folder is None:
                return {'error': 'Could not create downloads folder'}, 500

            # Run through all the files in the job and download them using the FileSystem APU
            for file in job.files:
                FileSystem.download_file(file.file_id, temp_folder)

            # Zip the folder
            zip_file_name = Path(FLASK_DOWNLOADS_DIRECTORY).joinpath(zip_name).with_suffix('.zip')
            zip_dir(temp_folder, zip_file_name)
                
            return send_file(str(zip_file_name.absolute()), as_attachment=True)
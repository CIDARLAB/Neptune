import uuid
from app.controllers.authentication import AuthenticationController
from app.controllers.s3filesystem import S3FileSystem
from app.controllers.ziphelper import download_s3files_and_zip
from app.models.job import Job
from flask import request, send_file, after_this_request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from pathlib import Path
from marshmallow import fields
from flask_apispec import use_kwargs

from app.parameters import FLASK_DOWNLOADS_DIRECTORY
from app.utils import zip_dir


class JobAPI:
    
    class JobBase(Resource):
        """Base API for jobs

        GET - gets all the information for a job
        DELETE - deletes a job (Not implemented)
        PUT - updates a job status (Not implemented)

        """

        @use_kwargs({'job_id': fields.Str()})
        def get(self, **kwargs):
            
            # Verify Access
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            job_id = kwargs.get('job_id')

            has_access = AuthenticationController.check_user_job_access(user_id, job_id)

            if has_access == False:
                return {'error': 'User does not have access to this job'}, 401

            job = Job.objects.get(job_id=job_id)
            return job.to_json(), 200
        
        # def delete(self):
        #     job_id = kwargs.get('job_id')

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
        #     job_id= kwargs.get('job_id')
            
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

        @use_kwargs({'job_id': fields.Str()})
        def get(self, **kwargs):
            job_id = kwargs.get('job_id')
            # Verify Access
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            has_access = AuthenticationController.check_user_job_access(user_id, job_id)

            if has_access == False:
                return {'error': 'User does not have access to this job'}, 401

            job = Job.objects.get(job_id=job_id)

            # Run through all the files in the job and download them using the FileSystem APU
            files_list = [file for file in job.files]
            
            zip_file_name = download_s3files_and_zip(files_list)
            
            download_file_handle = open(zip_file_name, 'rb')
            @after_this_request
            def remove_file(response):
                try:
                    zip_file_name.unlink()
                    download_file_handle.close()
                except Exception as error:
                    print("Error removing or closing downloaded file handle", error)
                return response

            return send_file(str(zip_file_name.absolute()), as_attachment=True, download_name=f'job-{job.job_id}.zip')
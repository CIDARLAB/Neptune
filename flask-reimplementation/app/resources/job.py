from app.models.job import Job
from flask import request
from flask_restful import Resource

class JobAPI:
    
    class JobBase(Resource):
        def get(self, job_id):
            job = Job.objects.get(job_id=job_id)
            return job.to_json(), 200
        
        def delete(self):
            job_id = request.get_json()['job_id']
            job = Job.objects.get(job_id=job_id)
            job.delete()
            return {'message': 'Job deleted successfully'}, 200
        
        def put(self):
            job_id= request.get_json()['job_id']
            job = Job.objects.get(job_id=job_id)
            job.update(request.get_json())
            return {'message': 'Job updated successfully'}, 200
        
        def post(self):
            job_id = request.get_json()['job_id']
            job = Job.objects.get(job_id=job_id)
            job.update(request.get_json())
            return {'message': 'Job updated successfully'}, 200
        
        
    class JobZip(Resource):
        def get(self, job_id):
            job = Job.objects.get(job_id=job_id)
            new_job = job.copy()
            return {'message': 'Job copied successfully', 'job_id': str(new_job.id)}, 200
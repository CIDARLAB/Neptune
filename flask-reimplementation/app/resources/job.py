from app.models.job import Job
from flask import request


class JobAPI:
    
    class Base(Resource):
        def get(self, job_id):
            job = Job.objects.get(id=job_id)
            return job.to_json(), 200
        
        def delete(self):
            job_id = request.get_json()['job_id']
            job = Job.objects.get(id=job_id)
            job.delete()
            return {'message': 'Job deleted successfully'}, 200
        
        def put(self):
            job_id= request.get_json()['job_id']
            job = Job.objects.get(id=job_id)
            job.update(request.get_json())
            return {'message': 'Job updated successfully'}, 200
        
        def post(self):
            job_id = request.get_json()['job_id']
            job = Job.objects.get(id=job_id)
            job.update(request.get_json())
            return {'message': 'Job updated successfully'}, 200
        
        
    class Zip(Resource):
        def get(self, job_id):
            job = Job.objects.get(id=job_id)
            new_job = job.copy()
            return {'message': 'Job copied successfully', 'job_id': str(new_job.id)}, 200
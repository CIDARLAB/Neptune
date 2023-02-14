from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from fluigi_cloud.db.user import User

class UserAPI(Resource):
    
    def get(self, **kwargs):
        """Gets all the user object info (id, workspaces, job, etc.)

        Returns:
            Tuple: (json, status_code)
        """
        verify_jwt_in_request()
        print("JWT Identity:", get_jwt_identity())
        user_id = get_jwt_identity()
        workspace_ids = [str(workspace.id) for workspace in User.objects.get(id=user_id).workspaces]
        job_ids = [str(job.id) for job in User.objects.get(id=user_id).jobs]
        return {
            'user_id': user_id,
            'first_name': User.objects.get(id=user_id).first_name,
            'last_name': User.objects.get(id=user_id).last_name,
            'email': User.objects.get(id=user_id).email,
            'workspaces': workspace_ids,
            'jobs': job_ids
        }, 200

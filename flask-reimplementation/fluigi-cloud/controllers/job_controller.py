import connexion
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import six
from app.controllers.authentication import AuthenticationController
from app.models.job import Job

from swagger_server.models.job_input import JobInput  # noqa: E501
from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server import util


def delete_job(body):  # noqa: E501
    """delete_job

    Delete the job # noqa: E501

    :param body: Delete a job
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = JobInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_job_zip_fs(body):  # noqa: E501
    """get_job_zip_fs

    Starts downloading the specified job as a zip file # noqa: E501

    :param body: Starts downloading the specified job
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = JobInput.from_dict(connexion.request.get_json())  # noqa: E501
        job_id = body.job_id
        # Verify Access
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        has_access = AuthenticationController.check_user_job_access(user_id, job_id)

        if has_access == False:
            return {'error': 'User does not have access to this job'}, 401

        job = Job.objects.get(job_id=job_id)

        # Run through all the files in the job and download them using the FileSystem APU
        files_list = [file for file in job.files]
        result_files = [file.s3_path for file in job.result_files]
            

        zip_file_name = download_s3files_and_zip(files_list)

        if zip_file_name == None:
            return {'error': 'Could create zip file'}, 500
        
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

def get_jobs(body):  # noqa: E501
    """get_jobs

    Get all jobs # noqa: E501

    :param body: Get all jobs
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = JobInput.from_dict(connexion.request.get_json())  # noqa: E501
        # Verify Access
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        job_id = body.job_id

        has_access = AuthenticationController.check_user_job_access(user_id, job_id)

        if has_access == False:
            return {'error': 'User does not have access to this job'}, 401

        job = Job.objects.get(job_id=job_id)
        return {
            'job_id': str(job.id),
            'created_at': job.created_at,
            'updated_at': job.updated_at,
            'files': [str(file.id) for file in job.files],
            'status': job.status,

        }, 200

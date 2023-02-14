import connexion
import six

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
    return 'do some magic!'


def get_jobs(body):  # noqa: E501
    """get_jobs

    Get all jobs # noqa: E501

    :param body: Get all jobs
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = JobInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

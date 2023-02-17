import connexion
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import six
from core.tasks import dispatch_compile_lfr, dispatch_compile_mint, test_task
from core.db.file import File

from api.models.compiler_inputs import CompilerInputs  # noqa: E501
from api.models.job_response import JobResponse  # noqa: E501
from api import util


def compile_lfr(body):  # noqa: E501
    """compile_lfr

    Compile the LFR File # noqa: E501

    :param body: Compile the LFR File
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = CompilerInputs.from_dict(connexion.request.get_json())  # noqa: E501
        
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        source_file_ids = body.source_files
        config_file_id = body.config_file
        args = body.args
        
        source_files = [File.objects.get(id=file_id) for file_id in source_file_ids]
        config_file = File.objects.get(id=config_file_id)
        if args is None:
            args = []
        result = dispatch_compile_lfr(user_id, source_files, config_file, args)
        return 


def compile_mint(body):  # noqa: E501
    """compile_mint

    Compile the MINT File # noqa: E501

    :param body: Compile the MINT File
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = CompilerInputs.from_dict(connexion.request.get_json())  # noqa: E501
        
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        source_file_ids = body.source_files
        config_file_id = body.config_file
        args = body.args
        
        source_files = [File.objects.get(id=file_id) for file_id in source_file_ids]
        config_file = File.objects.get(id=config_file_id)
        if args is None:
            args = []
        result = dispatch_compile_mint(user_id, source_files, config_file, args)
        return 

def run_test_job(body):  # noqa: E501
    """run_test_job

    Run The Test Job # noqa: E501

    :param body: Compile the MINT File
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = CompilerInputs.from_dict(connexion.request.get_json())  # noqa: E501
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        x = body.x
        y = body.y
        result = test_task(user_id, x, y)
        return {"job_id": str(result.id)}, 200
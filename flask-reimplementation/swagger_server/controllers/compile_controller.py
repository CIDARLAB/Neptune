import connexion
import six

from swagger_server.models.compiler_inputs import CompilerInputs  # noqa: E501
from swagger_server.models.job_response import JobResponse  # noqa: E501
from swagger_server import util


def compile_lfr(body):  # noqa: E501
    """compile_lfr

    Compile the LFR File # noqa: E501

    :param body: Compile the LFR File
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = CompilerInputs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def compile_mint(body):  # noqa: E501
    """compile_mint

    Compile the MINT File # noqa: E501

    :param body: Compile the MINT File
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = CompilerInputs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def run_test_job(body):  # noqa: E501
    """run_test_job

    Run The Test Job # noqa: E501

    :param body: Compile the MINT File
    :type body: dict | bytes

    :rtype: JobResponse
    """
    if connexion.request.is_json:
        body = CompilerInputs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

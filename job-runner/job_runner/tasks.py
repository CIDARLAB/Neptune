# import os
from pathlib import Path
import subprocess
from sys import stdout
from typing import Dict, List, Optional, Tuple
from job_runner.filesystem import download_file_using_client, upload_file_using_client

from job_runner.server import celery_app
import time
from socket_io_emitter import Emitter
import shutil

from .setting import SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_PORT


@celery_app.task(name="add_task")
def add(x, y):
    for i in range(5):
        time.sleep(1)
        print(i)
    print(x + y)
    
    return x + y

@celery_app.task(name="execute_task")
def execute(
    job_id:str,
    command: List[str],
    input_file_s3_objects:List[Tuple[str,str]] = [], 
    config_file_s3_object:Optional[Tuple[str, str]] = None,
) -> Dict[str, str]:
    """ Executes a command in a subprocess and returns a dictionary with the output file names and their corresponding s3 object names

    Args:
        job_id (str): Unique identifier for the job
        command (List[str]): Command to execute in a subprocess
        input_file_s3_objects (List[Tuple[str,str]]): List of tuples containing the input file name and its corresponding s3 object name
        config_file_s3_object (Tuple[str, str]): Tuple containing the config file name and its corresponding s3 object name

    Returns:
        Dict[str, str]: Dictionary with the output file names and their corresponding s3 object names
    """
    print("Executing task")
    print(f"job_id: {job_id}")
    print(f"command: {command}")
    print(f"input_file_s3_objects: {input_file_s3_objects}")
    print(f"config_file_s3_object: {config_file_s3_object}")
    
    # Create a new directory for the job and download all the input files to the directory
    path = Path(f"./jobs-tmp/{job_id}")
    output_path = path.joinpath("output")
    path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Download all the input files to the directory
    for (s3_object_name, local_file_name) in input_file_s3_objects:
        download_file_using_client(s3_object_name, local_file_name, path)
        
    # Download the config file to the directory
    if config_file_s3_object is not None and len(config_file_s3_object) == 2:
        download_file_using_client(config_file_s3_object[0], config_file_s3_object[1], path)
    
    # Start a subprocess to execute the test.sh script and pipe the output to a variable.
    io = Emitter({'host': SOCKETIO_REDIS_HOST, 'port': SOCKETIO_REDIS_PORT})
    with subprocess.Popen(
        command,
        # ["/bin/bash", "test.sh", str(output_path.absolute())], 
        # bufsize=1, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    ) as process, open(str(output_path.joinpath('output.log')), 'a+') as logfile:
        while process.poll() is None:
            stdout_line = ""
            stderr_line = ""
            if process.stdout is not None:
                stdout_line = process.stdout.readline().decode("utf-8")
            if process.stderr is not None:
                stderr_line = process.stderr.readline().decode("utf-8")
            stdout_data = stdout_line + stderr_line
            logfile.write(stdout_data)
            io.To(job_id).Emit('stdout', stdout_data)
    
    logfile.close()
    
    # Upload the output files from the job directory to the s3 bucket
    # Loop through all the files in the output directory and upload them to the s3 bucket
    s3_object_names: Dict[str, str] = {}
    for file in output_path.glob("*"):
        s3_object_name = upload_file_using_client(file.absolute())
        
        s3_object_names[file.name]=s3_object_name
    
    # Delete the job directory and all its contents
    shutil.rmtree(str(path.absolute()))
    
    # Send the final Signal to the monitor that the job is complete
    io.Emit('EOP', "This is finished !")
    
    return s3_object_names
    

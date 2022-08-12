# import os
from pathlib import Path
import subprocess
from job_runner.filesystem import upload_file_using_client

from job_runner.server import celery_app
import time
from socket_io_emitter import Emitter
import shutil


@celery_app.task(name="add_task")
def add(x, y):
    for i in range(5):
        time.sleep(1)
        print(i)
    print(x + y)
    
    return x + y

@celery_app.task(name="execute_task")
def test_execute(job_id:str):
    print("Executing task")
    
    # Create a new directory for the job and download all the input files to the directory
    path = Path(f"./jobs-tmp/{job_id}")
    output_path = path.joinpath("output")
    path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Start a subprocess to execute the test.sh script and pipe the output to a variable.
    io = Emitter({'host': 'localhost', 'port': 6379})
    with subprocess.Popen(
        ["/bin/bash", "test.sh", str(output_path.absolute())], 
        # bufsize=1, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    ) as process, open(str(output_path.joinpath('output.log')), 'a+') as logfile:
    
        stdout_data = process.stdout.read() + process.stderr.read()
        logfile.write(stdout_data.decode("utf-8"))
        io.Emit('stdout', stdout_data.decode("utf-8"))
    
    logfile.close()
    
    # TODO: Upload the output files from the job directory to the s3 bucket
    
    # Loop through all the files in the output directory and upload them to the s3 bucket
    for file in output_path.glob("*"):
        upload_file_using_client(file.absolute())
    
    # Delete the job directory and all its contents
    shutil.rmtree(str(path.absolute()))
    
    # Send the final Signal to the monitor that the job is complete
    io.Emit('EOP', "This is finished !")
    
    return "Executed task"    
    

# Neptune

# Getting Started Guide

This is the getting orientation guide to the massive set of repositories that are a part of the Neptune Project developed at CIDAR Lab. Please follow the dev guide section to seamlessly setup the repositories.

### Repository List

1. [Fluigi Cloud](https://github.com/CIDARLAB/Fluigi-Cloud) - node.js based serverside Framework that resides on AWS
1. [Neptune-UI](https://github.com/CIDARLAB/Neptune-UI) - vue.js based frontend framework
1. [pyFluigi](https://github.com/CIDARLAB/pyFluigi) - Place & Route manager system 
1. [pyLFR](https://github.com/CIDARLAB/pyLFR) - LFR Compiler for implemented in python (not yet public)
1. [pyparchmint](https://github.com/CIDARLAB/pyparchmint) - ParchMINT data model library in python
1. [pyMINT](https://github.com/CIDARLAB/pyMINT) - MINT Compiler and Datamodel
1. [LFR TestCases](https://github.com/CIDARLAB/LFR-TestCases) - Repository of LFR Test Cases used for Testing the LFR compiler
1. [MINT TestCases](https://github.com/CIDARLAB/MINT-TestCases) - Repository of the MINT Test Cases used for testing the MINT Compiler

## Development Guide

### Cloning and tracking for development

First, run the following commands for recursively cloning all the required dependencies for the project and set up the sub repo branch tracking for development:

```
git clone --recurse-submodules -j8 https://github.com/cidarlab/Neptune
cd Neptune
git submodule update --init
git submodule foreach -q --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'
```
[Submodule Recipe Reference](https://gist.github.com/slavafomin/08670ec0c0e75b500edbaa5d43a5c93c)

### Neptune Webapplication Development

The top-level development environment for the repo is for developing the cloud based application. The development container reuses the docker-compose components from the repo, i.e. `mongodb`, `minio` and `redis`. That means that you can only make edits to the neptune cloud application and **not the other components**. Its been intended to be done this way so that you utilize fluigi repo/3DuF repos for development for their corresponding components. This way you don't pollute the codebases and adhere the Pull Request discipline necessary for making changes to these code bases.

On launching the development containaer one can start the development using the following commands:

#### Steps
1. Goto the job-runner directory and run `python job_runner/server.py` (TODO-Update with debugging config in the future).
1. Goto the flask application directory and run `poetry lock --no-update` to install the dependencies.
2. Open the `server.py` file and run the debugger on it (Use the saved vscode debugger profile `Python: Flask`).
3. Goto the Neptune-UI directory and run `npm ci` to install the dependencies.
4. Run `npm run dev` frontend development server.


#### Notes
- Ensure that ports `8080` and `8081` are forwarded to ensure that you can see development Backend and frontend respectively.
- Ensure that port `27017` is forwarded to ensure that you can see the mongodb database. You can use [mongodb compass](https://www.mongodb.com/products/compass) to connect to the database and keep track of the changes going on in it.
  - user: `root`
  - password: `rootpassword`
  - database: `none`
- In order to have the cloud application's virtual filesystem working, you need to create the bucket on minio / S3 beforehand. Here are the details to access the minio server (simulates s3 locally)
  - admin panel url: `http://localhost:9001`
  - user: `minio`
  - password: `minio123`
  - bucket: `fluigi`. If this is not there create it, if you use another name, make sure the environment variable `AWS_S3_BUCKET_NAME` is set to the name of the bucket you created.

### Running individual services

```bash
docker run -i containername:dev --env-file=myenvfile
```

```bash
docker exec -ti <container name> /bin/bash
```

### How-To Mini Guides

#### Converting MINT Benchmaks to Parchmint 

In order to convert the benchmarks to ParchMint, you need to be able to use `pyfluigi` and `primitives-server`. In order to spawn a new instance of the Pritives-Server service to pull component parameters from the latest tracked 3DuF Implementation, you need to run the following command:

```bash
docker-compose up primitives-server
```

This server can now be accessed at `http://localhost:6060` (You can verify this on the browser).

Now setup the required environment for `pyfluigi` to run (Dedicated Docker Dev Environment Coming Soon). This can be done by running the following command:

```bash
cd pyfluigi
poetry install
poetry shell
fluigi convert-to-parchmint <mint-file> --assign-terminals --generate-graph-view --outpath <output-location>
```

### Contact

Reach out to [@rkrishnasanka](https://github.com/rkrishnasanka) for more details.

# Neptune

# Getting Started Guide

This is the getting orientation guide to the massive set of repositories that are a part of the Neptune Project developed at CIDAR Lab. 

### Repository List

1. [Fluigi Cloud](https://github.com/CIDARLAB/Fluigi-Cloud) - node.js based serverside Framework that resides on AWS
1. [Neptune-UI](https://github.com/CIDARLAB/Neptune-UI) - vue.js based frontend framework
1. [pyFluigi](https://github.com/CIDARLAB/pyFluigi) - Place & Route manager system 
1. [pyLFR](https://github.com/CIDARLAB/pyLFR) - LFR Compiler for implemented in python (not yet public)
1. [pyparchmint](https://github.com/CIDARLAB/pyparchmint) - ParchMINT data model library in python
1. [pyMINT](https://github.com/CIDARLAB/pyMINT) - MINT Compiler and Datamodel
1. [LFR TestCases](https://github.com/CIDARLAB/LFR-TestCases) - Repository of LFR Test Cases used for Testing the LFR compiler
1. [MINT TestCases](https://github.com/CIDARLAB/MINT-TestCases) - Repository of the MINT Test Cases used for testing the MINT Compiler

### How to Build

Since there are there many packages in the project, building this project is going to be a pain. Use the docker to complete builds, but please be aware that this can take a substantial amount of time to build.

TBA Rest of the guide...

### Contact

Reach out to [@rkrishnasanka](https://github.com/rkrishnasanka) for more details.


### Running individual services

```bash
docker run -i containername:dev --env-file=myenvfile
```

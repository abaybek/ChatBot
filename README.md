# ChatBot

Tested on thit env:
- OS             :: Ubuntu 16.04 LTS
- Python version :: Python 3.6.3 Anaconda, Inc.
- Package manager:: Conda  4.3.31

## Install

### Download and install
Official distributions are available at https://conda.io/miniconda.html 

### Create virtual environment on exist env file

#### Short explonation

Create new env on conda
```term
conda create --name chatbot python=3.6
```

#### Nice explonation
Open a terminal (`Ctrl+Alt+T`) and run:

```term
conda env update -f environment.yml
```

### Basics of Anaconda environment management ###
#### Creating an environment

```term
conda create --name myNewEnv python=x.x.x
  
```
#### Activating an environment
```term
activate myNewEnv   
```
#### Deactivating an environment
```term
deactivate myNewEnv 
```
#### Listing environments
```term
conda info --envs 
```
#### Removing an environment
```term
conda remove --name myNewEnv --all
```
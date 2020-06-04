# semantic-web
Software Engineering Course Project

## Pre-requisites
Kindly install docker, redis and graphviz on the system. Also ensure that you have spotify installed on your system (this doesn't need a premium account).


## Getting Started
In order to get started you'll need to install the dependencies by creating a virtual environment.
Follow the commands given below

```bash
git clone https://github.com/amet-vikram13/semantic-web
cd semantic-web
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

After installing the requirements, you'll have to setup redisgraph server using docker -> 

```bash
docker run -p 6379:6379 -it --rm redislabs/redisgraph
```

Once the server is up, you can run the project in a new terminal instance using the steps below ->
PS: Before running the project, ensure that spotify is up and running.

```bash
cd tobie
python querying.py
```

To get information about commands and operations, type help on the prompt.

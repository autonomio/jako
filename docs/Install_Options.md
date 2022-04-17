# Install Options

Before installing jako, it is recommended to first setup and start the following:
* A python or conda environment.
* A postgresql database setup in one of the machines. This will be used as the central datastore.


## Installing Jako 

#### Creating a python virtual environment
```python
virtualenv -p python3 jako_env
source jako_env/bin/activate
```

#### Creating a conda virtual environment
```python
conda create --name jako_env
conda activate jako_env
```

#### Install latest from PyPi
```python
pip install jako
```

#### Install a specific version from PyPi
```python
pip install jako==0.1
```

#### Upgrade installation from PyPi
```python
pip install -U --no-deps jako
```

#### Install from monthly
```python
pip install --upgrade --no-deps --force-reinstall git+https://github.com/autonomio/jako
```

#### Install from weekly
```python
pip install --upgrade --no-deps --force-reinstall git+https://github.com/autonomio/jako@dev
```

#### Install from daily
```python
pip install --upgrade --no-deps --force-reinstall git+https://github.com/autonomio/jako@daily-dev
```

## Installing a postgres database

To enable postgres in your central datastore, follow the steps in this 
* Postgres for ubuntu machine: [link](https://blog.logrocket.com/setting-up-a-remote-postgres-database-server-on-ubuntu-18-04/)   
* Postgres for Mac Machines: [link](https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/)


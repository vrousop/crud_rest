# REST API for VCF file data manipulation

The project contains a Flask server with CRUD operation to manipulate
the content of VCF file.

## Getting started
**1. (Optional) Set the following environmental variables if you want to change the
default configuration:**

- `SECRET_KEY` (secret key for authorization - default: 's3cr3t!')
- `CURRENT_SERVER` (host url - default: '0.0.0.0')

**2. Copy VCF file to folder src/data**

## **Run instructions**:
Run the bash script (run.sh) located in the "crud_rest" directory:

VCF_file example: "file.vcf"

    
    chmod +x run.sh
    ./run.sh -f VCF_file
    
OR run following commands:

- Create virtual environment with python3
    ```
    python -m venv env
    ```
- Activate the virtual environment
    ```
    source env/bin/activate
    ```
- Update pip package
    ```
    python -m pip install -U pip
    ```
- Install setup.py
    ```
    pip install -e .
    ```
- Run the application
    ```
    run -f VCF_file
    ```
### **Run tests**:
1. Activate the virtual environment if it is not activated
```
source env/bin/activate
```
Run available tests
   ```
   python -m unittest tests/test_get.py
   python -m unittest tests/test_post.py
   python -m unittest tests/test_put_del.py
   ````


### **For running on Windows**:
For running in Windows you can run the following commands in the
setup.py file location:
```
python3 -m venv env
env\bin\activate
python -m pip install -U pip
pip install -e .
run -f VCF_file
```
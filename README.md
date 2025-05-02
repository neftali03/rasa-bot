## Rasa project

## This project uses an environment with Python 3.8.20, and the dependencies managed with pip-tools.

## Requirements

1. **Python 3.8.20** 
    ## You need to make sure that you have Python 3.8.20 installed. 
    ##  If you don't have it, you can download it from [python.org], or use the following command to create a virtual environment with Python 3.8.20:
     ```bash
   python3.8 -m venv venv

2. **pip-tools** 
    ## We use this tool to manage the project's dependencies.
    ## You can install it by running:
    ```bash
   pip install pip-tools
    
3. **commands**   
   ## After completing the steps above, you can run the following commands in your terminal:
    ```bash
    pip-compile requirements.in
    pip install -r requirements.txt


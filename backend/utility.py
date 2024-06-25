import json
from tqdm import tqdm
import os

from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
from dotenv import load_dotenv
import logging.handlers


default_model="BAAI/bge-small-en-v1.5"
default_collection="collection"
default_metadata={'user':'admin'}
default_path_documents='documents/alcune_fiabe.pdf'
default_k=5


# ------------------------------------------------------------------------------
# Questa funzione tipizza il loglevel ricevuto in input come stringa
# ------------------------------------------------------------------------------
def log_level(level):
    if level == "CRITICAL":
        return CRITICAL
    if level == "ERROR":
        return ERROR
    if level == "WARNING":
        return WARNING
    if level == "DEBUG":
        return DEBUG
    return INFO


def create_logger(log_name):
    print("create_logger() IN")
    log_name=log_name+".log"
    
    if not os.path.exists('./log'):
        os.mkdir('./log')

    load_dotenv(verbose=True, override=True)

    myLog = logging.getLogger()

    if os.getenv("LOGLEVEL") is None:
        myLog.setLevel(INFO)
    else:
        myLog.setLevel(log_level(os.getenv("LOGLEVEL")))

    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s (%(processName)-10s - %(threadName)-10s) : %(message)s')

    logHandler = logging.handlers.TimedRotatingFileHandler(os.path.join("log", log_name), when="midnight")
    logHandler.setFormatter(logFormatter)
    myLog.addHandler(logHandler)
    print("create_logger() OK")

    return myLog


# prende in ingresso il percorso ed i dati e si salva in json
def save_in_json(file_name, data, delete=True):
    with tqdm(total=1, desc="Save in json")as pbar:
        name_mkdir="json"
        
        os.makedirs(name_mkdir,exist_ok=True)

        if file_name[-5:] != ".json":
            file_name+=".json"

        file_name=name_mkdir+'/'+file_name

        if delete:
            modify_or_delete='w'
        else:
            modify_or_delete='a'

        with open(file_name, modify_or_delete) as json_file:
            json.dump(data,json_file,indent=4)
        pbar.update(1)
    
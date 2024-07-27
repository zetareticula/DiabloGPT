from enum import IntEnum
import logging
import os
import requests
import sys
import time

# Desc: Base module for cdbtune
#
# This module contains the following functions:
# 1. Logger: A function that returns a logger object
# 2. init_logger: A function that initializes the logger
# 3. CONST: A class that contains constants used in the project
# 4. Err: An enumeration class that contains error codes
# 5. Err_Detail: A class that contains error descriptions
# 6. os_quit: A function that logs an error and exits the program
# 7. os: A module that provides a way to interact with the operating system
# 8. requests: A module that allows you to send HTTP requests
# 9. sys: A module that provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
# 10. time: A module that provides various time-related functions

def Logger(name="default_log", logger_level="debug"):
    logname = name.split("/")[-1][:-3]
    logger_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  

    logger = logging.getLogger(logname)
    logger.setLevel(logger_levels.get(logger_level))

    return logger


def init_logger(task_id, write_console=False, write_file=True):
    global cdb_logger
    fmt = "[%(asctime)s][%(levelname)s][%(process)d-%(filename)s:%(lineno)d] : %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    if write_file:
        fh = logging.FileHandler(CONST.FILE_LOG % task_id, mode='a')
        fh.setFormatter(logging.Formatter(fmt, datefmt))
        cdb_logger.addHandler(fh)
    if write_console:
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(fmt, datefmt))
        cdb_logger.addHandler(sh)


class CONST:
    TASK_ID = -1
    PROJECT_DIR = "/usr/local/cdbtune/"
    LOG_PATH = PROJECT_DIR + "log/"
    SCRIPT_PATH = PROJECT_DIR + "scripts/"
    LOG_SYSBENCH_PATH = LOG_PATH + "sysbench/"
    FILE_LOG = LOG_PATH + "%d.log"
    FILE_LOG_SYSBENCH = LOG_SYSBENCH_PATH + "%d_%s.log"
    FILE_LOG_BEST = LOG_PATH + "%d_bestnow.log"
    BASH_SYSBENCH = SCRIPT_PATH + "run_sysbench.sh"
    BASH_TPCC = SCRIPT_PATH + "run_tpcc.sh"
    cdb_public_api = "http://%s/cdb2/fun_logic/cgi-bin/public_api"
    URL_SET_PARAM = cdb_public_api + "/set_mysql_param.cgi"
    URL_QUERY_SET_PARAM = cdb_public_api + "/query_set_mysql_param_task.cgi"
    cdbtune_server = "http://127.0.0.1:9119"
    URL_INSERT_RESULT = cdbtune_server + "/insert_task_result"
    URL_UPDATE_TASK = cdbtune_server + "/update_task"


class Err(IntEnum):
    INPUT_ERROR = 101
    HTTP_REQUEST_ERR = 103
    RUN_SYSBENCH_FAILED = 201
    SET_MYSQL_PARAM_FAILED = 202
    MYSQL_CONNECT_ERR = 301
    MYSQL_EXEC_ERR = 302


class Err_Detail:
    Desc = dict()

    @classmethod
    def add_desc(cls, err, desc):
        cls.Desc[err] = desc


Err_Detail.add_desc(Err.INPUT_ERROR, "Input error")
Err_Detail.add_desc(Err.HTTP_REQUEST_ERR, "HTTP request error")
Err_Detail.add_desc(Err.RUN_SYSBENCH_FAILED, "Sysbench benchmarking failed")
Err_Detail.add_desc(Err.SET_MYSQL_PARAM_FAILED, "Failed to set MySQL parameters")
Err_Detail.add_desc(Err.MYSQL_CONNECT_ERR, "MySQL connection error")
Err_Detail.add_desc(Err.MYSQL_EXEC_ERR, "MySQL execution error")


def os_quit(err, detail=""):
    err_str = "err: %d, %s, %s" % (err, Err_Detail.Desc[err], detail)
    data = {"task_id": CONST.TASK_ID, "error": err_str}
    cdb_logger.error(err_str)
    cdb_logger.info("update task status %s", requests.post(CONST.URL_UPDATE_TASK, data))
    os._exit(int(err))

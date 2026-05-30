# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 07:24:26 2019

@author: PROJECT
"""

import logging as lg
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import time


log_dir = 'logs/'
log_file_name = datetime.utcnow().strftime("%Y_%m_%d")+'_search_engine_app.log'
log_data_file = log_dir+'/'+log_file_name


def time_rotated_log():
    lg.getLogger()
    lg.Formatter.converter = time.gmtime
    time_handler=TimedRotatingFileHandler(log_data_file,utc=True,when='midnight',encoding='utf-8')
    
    lg.basicConfig(format='[%(asctime)s] %(levelname)s::%(funcName)s() %(message)s', 
                            level=lg.INFO,
                            handlers=[time_handler])
    
    return lg



    
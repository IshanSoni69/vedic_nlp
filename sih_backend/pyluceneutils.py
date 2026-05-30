#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 09:39:44 2022

@author: Soni, Ishan
"""

import lucene

def initilaizeVM(log):
    try:
        lucene.initVM()
        log.info("JVM for PyLUcene initialized and running.")
    except:
        log.warn("VM arleady Initialized continuing execution")
    finally:
        return lucene
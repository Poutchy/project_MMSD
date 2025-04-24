#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 14:15:25 2024

@author: druetto
"""

import json
import os
import warnings

import pandas as pd

_ERR = (FileNotFoundError, IsADirectoryError)

curr_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ""))
configs = None
fileLecturer = None
dataLecturer = None
fileProduct = None
dataProduct = None

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

def createTableLecturers(fileName, configFile=""):
    try:
        with open(configFile, "r") as cf:
            configs = json.load(cf)
    except _ERR:
        print("[ERROR] Provide a valid CONFIG file!!!")
        return None

    fieldsLecturer = configs["professor"]

    try:
        fileLecturer = os.path.join(curr_dir, fileName)
        dataLecturer = pd.read_excel(fileLecturer, usecols=fieldsLecturer)
    except _ERR:
        print("[ERROR] Provide a valid PROFESSORS file!!!")
        return None

    return dataLecturer


def createTableProducts(fileName, configFile=""):
    try:
        with open(configFile, "r") as cf:
            configs = json.load(cf)
    except _ERR:
        print("[ERROR] Provide a valid CONFIG file!!!")
        return None

    fieldsProduct = configs["product"]

    try:
        fileProduct = os.path.join(curr_dir, fileName)
        dataProduct = pd.read_excel(fileProduct, usecols=fieldsProduct)
    except _ERR:
        print("[ERROR] Provide a valid PRODUCTS file!!!")
        return None

    return dataProduct

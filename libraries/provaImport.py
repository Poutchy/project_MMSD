#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 14:14:32 2024

@author: druetto
"""

from libraries.importExcel import createTableLecturers, createTableProducts

Configs = "data/config.json"
AffFile = "data/2024-02-12-DipInfoAfferenze-PO-PA-RIC-orig.xlsx"
ProdFile = "data/2024-02-12-prodotti-PO-PA-RIC-02A-03A-03B-04A-04B-2020-instampa.xlsx"

AffTable = createTableLecturers(AffFile, Configs)
ProdTable = createTableProducts(ProdFile, Configs)

print(AffTable)
print(ProdFile)

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

def isvalid_phone_number(text:str) -> bool:
    text = text.strip()
    if not len(text) == 10 or not text[0]=="0":
        return False

    try:
        int(text)
    except:
        return False
    return True

def isvalid_address(text:str, type_of_object:str)-> bool:
    #in CRUD only
    text = text.strip()

    if not type_of_object:
        return False
    arr_by_n = text.split("\n")
    arr_by_c = text.split(":")

    if type_of_object == "БЦ":
        if not (len(arr_by_n) == 4 and len(arr_by_c) == 5):
            return False
        return True
    if not (len(arr_by_n) == 3 and len(arr_by_c) == 4):
        return False
    return True

def isvalid_order(text:str, type_of_object:str)-> bool:
    text = text.strip()

    if not type_of_object:
        return False
    arr_by_n = text.split("\n")
    arr_by_c = text.split(":")

    if type_of_object == "БЦ":
        if not (len(arr_by_n) == 6 and len(arr_by_c) == 7):
            return False
        return True

    if not (len(arr_by_n) == 5 and len(arr_by_c) == 6):
        return False

    return True

def isvalid_count(text:str)-> bool:
    try:
        count = int(text)
        if count >= 0:
            return True
    except:
        return False
    return False

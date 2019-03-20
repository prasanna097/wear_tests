'''
Created on Feb 09, 2018

@author: aunnikri
'''

import json

class JsonUtility(object):

    @staticmethod
    def readJsonFile(file):
        with open(file, "r") as jsonFile:
            config = json.load(jsonFile)
        jsonFile.close()
        return config

    @staticmethod
    def writeJsonFile(data, file):
        with open(file, "w") as jsonFile:
            json.dump(data, jsonFile)
        jsonFile.close()
from dotenv import load_dotenv
load_dotenv(dotenv_path='properties.env')
import os
import csv
import numpy as np
import pandas as pd 

filePath = os.getenv("STOCK-INPUT_FILE_PATH")
fields=['date','close','open','high','low','volume','change']

def getInputStockCode(fileName):
    if(fileName):
        filePath = fileName
    with open("./inputs/" + filePath, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    # data.remove(data[0])
    return data

def writeStockDataToCSVFile(stockCode, datas):
    headLine = [["date","close","open","high","low","volume","change"]]
    pd.DataFrame(headLine).to_csv("./results/" + stockCode + ".csv", index = False, header=False)
    # print("datas", datas)
    pd.DataFrame(datas).to_csv("./results/" + stockCode + ".csv", mode='a', index = False, header=False)

def writeErrReport(fileName, datas):
    pd.DataFrame(datas).to_csv("./errReports/" + fileName + ".csv", mode='a', index = False, header=False)
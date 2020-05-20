from dotenv import load_dotenv
load_dotenv(dotenv_path='properties.env')
import os
import csv
import datetime
import numpy as np
import pandas as pd 
OUT_PUT_DATE_FORMAT = os.getenv("OUT_PUT_DATE_FORMAT")

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


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
	s = ''
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s

def changeDateFormat(strDate):
    if(not strDate):
        return ""
    else:
        return datetime.datetime.strptime(strDate, '%d/%m/%Y').strftime(OUT_PUT_DATE_FORMAT)
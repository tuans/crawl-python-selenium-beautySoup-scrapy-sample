from HTMLTableParser import HTMLTableParser
import pandas as pd
from fileUtils import *



def crawl(fileName):
    stockCodes = getInputStockCode(fileName)
    hp = HTMLTableParser()
    for code in stockCodes:
        finalDF = pd.DataFrame()
        for i in range(1, 51):
            tableDF = hp.parse_url(code, i)
            if(tableDF.empty):
                break
            if(finalDF.empty and not tableDF.empty):
                finalDF = tableDF
            elif(not tableDF.empty):
                finalDF = finalDF.append(tableDF)

        if(not finalDF.empty):
            finalDF.sort_values(by=['date'], inplace=True, ascending=True)
            finalDF.to_csv("./results/" + ''.join(code) + ".csv", index = False)


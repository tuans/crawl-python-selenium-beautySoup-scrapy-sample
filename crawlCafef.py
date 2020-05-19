import sys
import traceback
import datetime
import numpy as np
from dotenv import load_dotenv
load_dotenv(dotenv_path='properties.env')
import os
from seleniumUtils import *
from fileUtils import *



CRAWL_FROM_DATE = os.getenv("CRAWL_FROM_DATE")
OUT_PUT_DATE_FORMAT = os.getenv("OUT_PUT_DATE_FORMAT")

url="https://s.cafef.vn/Lich-su-giao-dich-XXX-1.chn"
rowXPath_1 = "//tr[@id='ctl00_ContentPlaceHolder1_ctl03_rptData_ctl[XXX]_itemTR']"
rowXPath_2 = "//tr[@id='ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl[XXX]_itemTR']"
dateXPath = "/td[@class='Item_DateItem']"
closePriceXPath_1 = "/td[@class='Item_Price1'][2]"
openPriceXPath_1 = "/td[@class='Item_Price1'][8]"
highestPriceXPath_1 = "/td[@class='Item_Price1'][9]"
lowestPriceXPath_1 = "/td[@class='Item_Price1'][10]"
volumeXPath_1 = "/td[@class='Item_Price1'][4]"
changeXPath = "/td[@class='Item_ChangePrice']"

closePriceXPath_2 = "/td[@class='Item_Price10'][2]"
openPriceXPath_2 = "/td[@class='Item_Price10'][6]"
highestPriceXPath_2 = "/td[@class='Item_Price10'][7]"
lowestPriceXPath_2 = "/td[@class='Item_Price10'][8]"
volumeXPath_2 = "/td[@class='Item_Price10'][3]"

nextXPath = "//table[@class='CafeF_Paging']//a[contains(text(),'>')]"
dataTableXPath_1 = "//table[@id='GirdTable']//tbody/tr"
dataTableXPath_2 = "//table[@id='GirdTable2']//tbody/tr"

pageType = 1

def changeDateFormat(strDate):
    if(not strDate):
        return ""
    else:
        return datetime.datetime.strptime(strDate, '%d/%m/%Y').strftime(OUT_PUT_DATE_FORMAT)

def compareDate(strDate1, strDate2):
    date1 = datetime.datetime.strptime(strDate1, "%d/%m/%Y")
    date2 = datetime.datetime.strptime(strDate2, "%d/%m/%Y")
    if(date1 > date2):
        return 1
    elif(date1 == date2):
        return 0
    else:
        return -1


def getRowXPath(rowIndex):
    global pageType
    selectedRowXPath = rowXPath_1
    rowXPath = selectedRowXPath.replace("[XXX]", '%02d' % rowIndex)
    pageType = 1
    if not isExist(rowXPath):
        rowXPath = rowXPath_2.replace("[XXX]", '%02d' % rowIndex)
        selectedRowXPath = rowXPath_2
        pageType = 2
        if not isExist(rowXPath):
            selectedRowXPath = None
            pageType = -1
    return selectedRowXPath   
         
def getItemPerPage():
    countTR = len(getElements(dataTableXPath_1))
    if(countTR > 2):
        return countTR - 2
    else:
        countTR = len(getElements(dataTableXPath_2))
        if(countTR > 2):
            return countTR - 2
        else:
            return 0
def crawl(fileName):
    try:
        withChrome(True)
        stockCodes = getInputStockCode(fileName)
        stockEmptyData = []
        stockDifferentData = []
        errStocks = []

        for code in stockCodes:
            pageNumber = 1    
            gotoURL(url.replace("XXX", ''.join(code)))
            npStockDatas = []
            try:
                while(pageNumber <= 50):
                    itemPerpage = getItemPerPage()
                    if(pageNumber == 1 and itemPerpage == 0):
                        stockEmptyData.append(code)
                        break
                    elif(itemPerpage == 0):
                        break

                    rowIndex = 1
                    rowXPath = getRowXPath(rowIndex)
                    if(not rowXPath):
                        stockDifferentData.append(code)
                        break
                    isOldData = False
                    
                    while rowIndex <= itemPerpage:
                        rowXPathHead = rowXPath.replace("[XXX]", '%02d' % rowIndex)
                        if(rowIndex % 2 ==0):
                            rowXPathHead = rowXPathHead.replace("_itemTR", "_altitemTR")
                        else:
                            rowXPathHead = rowXPathHead.replace("_altitemTR", "_itemTR")
                        
                        
                        date = myGetText(rowXPathHead + dateXPath)
                        # if(compareDate(date, CRAWL_FROM_DATE) < 0):
                        #     isOldData = True
                        #     break
                        if(pageType == 1):
                            closePrice = myGetText(rowXPathHead + closePriceXPath_1)
                            openPrice =  myGetText(rowXPathHead + openPriceXPath_1)
                            highestPrice =  myGetText(rowXPathHead + highestPriceXPath_1)
                            lowestPrice =  myGetText(rowXPathHead + lowestPriceXPath_1)
                            volume =  myGetText(rowXPathHead + volumeXPath_1)
                        else:
                            closePrice = myGetText(rowXPathHead + closePriceXPath_2)
                            openPrice =  myGetText(rowXPathHead + openPriceXPath_2)
                            highestPrice =  myGetText(rowXPathHead + highestPriceXPath_2)
                            lowestPrice =  myGetText(rowXPathHead + lowestPriceXPath_2)
                            volume =  myGetText(rowXPathHead + volumeXPath_2)
                        change =  myGetText(rowXPathHead + changeXPath)
                        rowData = [changeDateFormat(date), closePrice, openPrice, highestPrice, lowestPrice, volume.replace(",", ""), change]
                        # print("rowData", rowData)
                        npStockDatas.append(rowData)
                        rowIndex+=1
                    # if(isOldData):
                    #     break
                    # Next Page
                    # print("pageNumber", pageNumber)
                    pageNumber+=1
                    myClick(nextXPath)
                    pause(1)
                if(npStockDatas != []):
                    npStockDatas = sorted(npStockDatas,key=lambda x:datetime.datetime.strptime(x[0],"%Y-%m-%d"))
                    writeStockDataToCSVFile(''.join(code), npStockDatas)
            except:
                traceback.print_exc()
                errStocks.append(code)
            


        # print("stockEmptyData", stockEmptyData)
        # print("stockDifferentData", stockDifferentData)
        # print("errStocks", errStocks)
        if(stockEmptyData != []):
            writeErrReport("stockEmptyData", stockEmptyData)
        if(stockDifferentData != []):
            writeErrReport("stockDifferentData", stockDifferentData)
        if(errStocks != []):
            writeErrReport("errStocks", errStocks)

    except:
        traceback.print_exc()

    finally:
        if (driver != None):
            driver.quit()


# crawl("stock_code.csv")
import requests
import pandas as pd
from bs4 import BeautifulSoup
import traceback
from itertools import product
from fileUtils import *
import datetime as dt

URL_TEMPLATE="https://s.cafef.vn/Lich-su-giao-dich-[XXX]-1.chn"
    
class HTMLTableParser:
    errorStockCodes =[{}]
    def parse_url(self, code, pageNumber):
        url = URL_TEMPLATE.replace("[XXX]", ''.join(code))
        try:
            data['__EVENTARGUMENT'] = pageNumber
            data['ctl00$ContentPlaceHolder1$ctl03$txtKeyword'] = ''.join(code)
            headers['Referer'] = url
            response = requests.post(url, headers=headers, cookies=cookies, data=data)
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find("table", attrs={"id": "GirdTable2"})
            
            if(table == None):
                table = soup.find("table", attrs={"id": "GirdTable"})

            if(table == None):
                print("Empty data")
                print("url", url)
                print("pageNumber", pageNumber)
                print("------------------------------------------------")
                return pd.DataFrame()    

            tableData = table_to_2d(table)
            
            # print("tableData", tableData)
            tableData.remove(tableData[0])
            tableDF = pd.DataFrame(tableData, index=None)
            tableDF.columns = tableDF.iloc[0]
            tableDF = tableDF[1:]
            tableDF = tableDF.loc[:,~tableDF.columns.duplicated()]
            tableDF = tableDF[["Ngay", "Gia  dong cua", "Thay doi (+/-%)", "KL", "Gia mo cua", "Gia cao nhat", "Gia thap nhat"]]
            tableDF.rename(columns={'Ngay': 'date', 'Gia  dong cua': 'close', 'Thay doi (+/-%)': 'change', 'KL': 'volume', "Gia mo cua": "open", "Gia cao nhat": "high", "Gia thap nhat": "low"}, inplace=True)
            return tableDF
            
        except:
            print("Error happened!")
            print("code", code)
            print("pageNumber", pageNumber)
            print("Re crawl again ...")
            print("---------------------------------------")
            return self.parse_url(code, pageNumber)

    

def table_to_2d(table_tag):
    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    # first scan, see how many columns we need
    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        # count columns (including spanned).
        # add active rowspans from preceding rows
        # we *ignore* the colspan value on the last cell, to prevent
        # creating 'phantom' columns with no actual cells, only extended
        # colspans. This is achieved by hardcoding the last cell width as 1. 
        # a colspan of 0 means “fill until the end” but can really only apply
        # to the last cell; ignore it elsewhere. 
        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))
        # update rowspan bookkeeping; 0 is a span to the bottom. 
        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans 
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    if(row + drow == 0 or row + drow == 1):
                        table[row + drow][col + dcol] = remove_accents(value.replace('\xa0', ""))
                    else:
                        table[row + drow][col + dcol] = value.replace('\xa0', "").replace(",", "")
                        if(col + dcol == 0):
                            table[row + drow][col + dcol] = changeDateFormat(table[row + drow][col + dcol])
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    return table
cookies = {
    'cafef.IsMobile': 'IsMobile=NO',
    'ASP.NET_SessionId': 'towrzy45o5auahangwbsngif',
    'favorite_stocks_state': '1',
    '_ga': 'GA1.2.1763630523.1589899962',
    '_gid': 'GA1.2.1908934736.1589899962',
    '_gat': '1',
    '_gat_pagecafef': '1',
    '_gat_UA-108467182-1': '1',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'X-MicrosoftAjax': 'Delta=true',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Origin': 'https://s.cafef.vn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://s.cafef.vn/Lich-su-giao-dich-[XXX]-1.chn',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5,th;q=0.4',
}

data = {
  'ctl00$ContentPlaceHolder1$scriptmanager': 'ctl00$ContentPlaceHolder1$ctl03$panelAjax|ctl00$ContentPlaceHolder1$ctl03$pager2',
  'ctl00$ContentPlaceHolder1$ctl03$txtKeyword': 'ABC',
  'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker': '',
  'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate2$txtDatePicker': '',
  'ctl00$UcFooter2$hdIP': '',
  '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ctl03$pager2',
  '__EVENTARGUMENT': '30',
  '__VIEWSTATE': '/wEPDwUKMTU2NzY0ODUyMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY3RsMDMkYnRTZWFyY2jJnyPYjjwDsOatyCQBZar0ZSQygQ==',
  '__VIEWSTATEGENERATOR': '2E2252AF',
  '__ASYNCPOST': 'true',
  '': ''
}
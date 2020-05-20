import multiprocessing
import traceback
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='properties.env')
from crawlCafef_v2 import *

NUMBER_OF_THREAD = os.getenv("NUMBER_OF_THREAD")

if __name__ == '__main__':
    try:
        jobs = []
        for i in range(1, int(NUMBER_OF_THREAD) + 1):
            p = multiprocessing.Process(target=crawl, args=("stock_code_" + str(i) + ".csv",))
            jobs.append(p)
            p.start()
    except:
        traceback.print_exc() 
        print("Error: unable to start thread")
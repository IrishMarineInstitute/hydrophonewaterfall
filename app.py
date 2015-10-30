#!/usr/bin/env python
from bottle import route, run, request, response
import numpy as np
import matplotlib as ml
ml.use('Agg')
import matplotlib.pyplot as plt
import cStringIO
from fdsend import send_file
import schedule
import threading
import time
import subprocess
import os
import glob

site="spiddal.marine.ie/data/hydrophones/SBF1323/"

class Scheduler(object):

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
           schedule.run_pending()
           time.sleep(1)

def load_files(n):
    data = []
    # might need line 30 from first file, and line 31 from the rest?
    skip_headers = 29
    first_file = True
    for f in find_files(n):
        a = np.genfromtxt(f, skip_header=skip_headers)
        data.append(a[:,6:]) # skipping first few cols
        if first_file:
           skip_headers = skip_headers + 1
           first_file = False
    return np.concatenate(data)

def find_files(n):
    found = []
    for root, dirs, files in os.walk(site, topdown=True):
        if dirs:
            dirs.sort(reverse=True)
        else:
            textfiles = glob.glob("{0}/*.txt".format(root))[::-1]
            for file in textfiles:
                found.append(file)
                if len(found) == n:
                    return found[::-1] # back tor proper order
    return found[::-1]

def get_request_int(key,value):
    try:
        value = int(str(request.GET.get(key,value)).strip())
    except ValueError:
        pass
    return value

@route('/')
def index():
    pages = get_request_int('pages',1)
    rows = get_request_int('rows',0)
    data = load_files(min(pages,100)) # max 100 pages
    if rows:
       data = data[:rows,:]
    H = np.array(data)
    H = np.log(H)
    fig = plt.figure()
    plt.imshow(H)
    sio = cStringIO.StringIO()
    plt.savefig(sio, format="png")
    response.set_header('Pragma', 'no-cache')
    response.set_header('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate')
    response.set_header('Expires', 'Thu, 01 Dec 1994 16:00:00 GMT')
    sio.seek(0)
    return send_file(sio, filename="chart.png", ctype="image/png")

def mirror_site():
    subprocess.call("wget -nc -r -w 0.5 {0}$(date -u +%Y/%m/%d)/".format(site), shell=True)

schedule.every(30).seconds.do(mirror_site)
Scheduler()
run(host='0.0.0.0',port=80)

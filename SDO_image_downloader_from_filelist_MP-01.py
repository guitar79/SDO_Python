# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from glob import glob
import os
import SDO_utility


################################################
### Multiprocessing instead of multithreading
################################################
import multiprocessing as proc
myQueue = proc.Manager().Queue()

# I love the OOP way.(Custom class for multiprocessing)
class Multiprocessor():
    def __init__(self):
        self.processes = []
        self.queue = proc.Queue()

    @staticmethod
    def _wrapper(func, args, kwargs):
        ret = func(*args, **kwargs)
        myQueue.put(ret)

    def restart(self):
        self.processes = []
        self.queue = proc.Queue()

    def run(self, func, *args, **kwargs):
        args2 = [func, args, kwargs]
        p = proc.Process(target=self._wrapper, args=args2)
        self.processes.append(p)
        p.start()

    def wait(self):
        for p in self.processes:
            p.join()
        rets = []
        for p in self.processes:
            ret = myQueue.get_nowait()

            rets.append(ret)
        for p in self.processes:
            p.terminate()
        return rets
 

###########################################
    
myMP = Multiprocessor()
num_cpu = 8

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
targets = ['2048_HMII.jpg','1024_HMII.jpg', '1024_0304.jpg', '1024_4500.jpg', '1024_HMIIB.jpg', '1024_HMIIC.jpg', '1024_0171.jpg', '1024_0131.jpg'] #this tpye of image will be downloading
time_gap = 1 #time gap
request_hour = range(0,24,time_gap) #make list                       
filelist_dir_name = '../SDO_lists/'

SDO_filelists = sorted(glob(os.path.join('{0}SDO_filelist_*.txt'.format(filelist_dir_name))))

for SDO_filelist in SDO_filelists:
        
    values = []
    num_batches = len(SDO_filelists) // num_cpu + 1
    for batch in range(num_batches):
        myMP.restart()
        for SDO_filelist in SDO_filelists[batch*num_cpu:(batch+1)*num_cpu] :
            print('url .. {0}'.format(SDO_filelist))
            #myMP.run(f, fullname)
            myMP.run(SDO_utility.SDO_image_downloader_from_filelist, SDO_filelist, targets, request_hour)
        print("Batch " + str(batch))
        myMP.wait()
        #values.append(myMP.wait())
        print("OK batch" + str(batch))
        
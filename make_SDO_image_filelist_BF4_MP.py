# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

import os
from datetime import datetime
import SDO_utilities

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
   
log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))

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
num_cpu = 365

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))
    
from dateutil.relativedelta import relativedelta
p_start_date = datetime(2021, 1, 1) #convert startdate to date type
p_end_date = datetime(2021, 12, 31)

dates = [p_start_date]
date1 = p_start_date
while date1 < p_end_date : 
    date1 += relativedelta(days=1)
    dates.append(date1)    

print(dates)

save_dir_name = '../SDO_filelists/'
if not os.path.exists('{0}'.format(save_dir_name)):
    os.makedirs('{0}'.format(save_dir_name))
    print ('*'*80)
    print ('{0} is created'.format(save_dir_name))
else :
    print ('*'*80)
    print ('{0} is exist'.format(save_dir_name))
        

values = []
num_batches = len(dates) // num_cpu + 1
for batch in range(num_batches):
    myMP.restart()
    for date in dates[batch*num_cpu:(batch+1)*num_cpu] :
        print('date : {0}'.format(date))
        myMP.run(SDO_utilities.SDO_image_list_to_filelist_1day, save_dir_name, date)
    print("Batch " + str(batch))
    myMP.wait()
    #values.append(myMP.wait())
    print("OK batch" + str(batch))

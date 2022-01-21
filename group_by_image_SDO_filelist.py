# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from glob import glob
from datetime import datetime
import pandas as pd
import os
import SDO_utilities

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'

#this tpye of image will be added
img_sizes = [4096, 3072, 2048, 1024, 512]
chls = ['0131', '0171', '0193', '0211',
        '0304', '0094', '0335', '1600', '1700', '0211', '4500', 
        'HMIB', 'HMIBC', 'HMID', 'HMII', 'HMIIC', 'HMIIF']
        #'211193171', '211193171n', '211193171rg']

targets = []
for img_size in img_sizes :
    for chl in chls : 
        targets.append('{0}_{1}.jpg'.format(str(img_size), chl))
  
filelist_dir_name = '../SDO_filelists/'
save_dir_name = '../wget_by_suffix/'
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)
    print ('*'*80)
    print ('{0} is created.'.format(save_dir_name))
else : 
    print ('*'*80)
    print ('{0} is already exist.'.format(save_dir_name))
                    
SDO_filelists = sorted(glob(os.path.join('{0}SDO_filelist_*.txt'
                                         .format(filelist_dir_name))))

url_lists = []
for SDO_filelist in SDO_filelists:    
    # Open the file with read only permit
    print ('Readding {0} file.'.format(SDO_filelist))
    f = open(SDO_filelist,'r')
    lines = f.readlines()
    
    n = 0    
    for line in lines:
        #fullname  = fullnames[0]
        n += 1
        print('#'*40,
            "\n{2:.01f}%  ({0}/{1}) {3}".format(n, len(lines), (n/len(lines))*100, SDO_filelist))

        line = line.rstrip()
        url_lists.append(line)
    # close the file after reading the lines.
    f.close()
#make Pandas Series from list
ser = pd.Series(url_lists)
      
for target in targets :
    
    if os.path.isfile('{0}{1}.csv'.format(save_dir_name, target)) :
        SDO_utilities.write_log(log_file, '{2} : {0}{1}.txt is already exist.'\
          .format(save_dir_name, target, datetime.now()))
    else :
        try : 
            ser_target = ser[ser.str.contains(target)]
            ser_target.to_csv('{0}{1}.csv'.format(save_dir_name, target))
            SDO_utilities.write_log(log_file, '{2} : {0}{1}.txt is created.'\
              .format(save_dir_name, target, datetime.now()))
                        
        except Exception as err : 
            SDO_utilities.write_log(err_log_file, '{2}: {0}, {1}'\
                  .format(err, target, datetime.now()))
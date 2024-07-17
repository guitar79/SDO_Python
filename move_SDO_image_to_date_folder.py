# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from datetime import datetime
import os
import shutil 
import _SDO_utilities

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

save_base_dr = "../browse/"
if not os.path.exists(save_base_dr):
    os.makedirs(save_base_dr)
    print ('{} is created...'.format(save_base_dr))
    
for dir in chls :
    #dir = chls[0]
    base_dr = "../4096_{}/".format(dir)
    fullnames = _SDO_utilities.getFullnameListOfallFiles(base_dr)
    
    n = 0    
    for fullname in fullnames :
        #fullname  = fullnames[0]
        n += 1
        print('#'*40,
            "\n{2:.01f}%  ({0}/{1}) {3}".format(n, len(fullnames), (n/len(fullnames))*100, os.path.basename(__file__)))
        print ("Starting...   fullname: {}".format(fullname))
        
        fullname_el = fullname.split("/")
        filename = fullname_el[-1]
        new_foldername = "{}{}/{}/{}/".format(save_base_dr, filename[0:4], 
                                              filename[4:6], filename[6:8])
        if not os.path.exists(new_foldername):
            os.makedirs(new_foldername)
            print ('{} is created...'.format(new_foldername))
        try : 
        
            if os.path.exists('{0}{1}'.format(new_foldername, filename)):
                _SDO_utilities.write_log(log_file, 
                     '{0}{1} is already exist...'.format(new_foldername, filename))
            else :
                shutil.move(r"{}".format(fullname), r"{}{}".format(new_foldername, filename))
                print ("move {}".format(fullname), "{}{}".format(new_foldername, filename))
                
        except Exception as err : 
            print("X"*60)
            _SDO_utilities.write_log(err_log_file, \
                 '{2} ::: {0} with move {1} '.format(err, fullname, datetime.now()))

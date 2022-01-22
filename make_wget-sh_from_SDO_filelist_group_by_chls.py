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
img_sizes = [4096]
chls = ['0131', '0171', '0193', '0211',
        '0304', '0094', '0335', '1600', '1700', '0211', '4500', 
        'HMIB', 'HMIBC', 'HMID', 'HMII', 'HMIIC', 'HMIIF']
        #'211193171', '211193171n', '211193171rg']

targets = []
for img_size in img_sizes :
    for chl in chls : 
        targets.append('{0}_{1}'.format(str(img_size), chl))
  
filelist_dir_name = '../SDO_filelists_by_chls/'
save_dir_name = '../wget_sh_by_chls/'
save_base_dr = "../browse/"

if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)
    print ('*'*80)
    print ('{0} is created.'.format(save_dir_name))
else : 
    print ('*'*80)
    print ('{0} is already exist.'.format(save_dir_name))
                          
for target in targets :
    #target = targets[0]
    try : 
        SDO_filelists = sorted(glob(os.path.join('{}{}*.txt'.format(filelist_dir_name, target))))
                
        for SDO_filelist in SDO_filelists:   
            #SDO_filelist = SDO_filelists[0]
            
            SDO_fullname_el = SDO_filelist.split("/")
            SDO_filename = SDO_fullname_el[-1]
            
            #make Pandas DataFrame from file
            df = pd.read_csv(SDO_filelist)
            print("df: {}".format(df))
            
            #df['wget_sh'] = 'str ' + df['#this file is created by guitar79@naver.com'].astype(str)
            wget_sh = ""    
            for index, value in df['#this file is created by guitar79@naver.com'].items():
                fullname_el = value.split("/")
                filename = fullname_el[-1]
                new_foldername = "{}{}/{}/{}/".format(save_base_dr, filename[0:4], 
                                                      filename[4:6], filename[6:8])
                if not os.path.exists(new_foldername):
                    os.makedirs(new_foldername)
                    print ('{} is created...'.format(new_foldername))
                    
                #wget -T 300 -t 1 -r -nd -np -l 1 -N --no-if-modified-since -P ../4096_HMIB/ https://sdo.gsfc.nasa.gov/assets/img/browse/2010/06/18/20100618_032603_4096_HMIB.jpg
                wget_sh += "wget -T 300 -t 1 -r -nd -np -l 1 -N --no-if-modified-since -P "
                wget_sh += "{} {}\n".format(new_foldername, value)
            
            with open("{}{}_wget.sh".format(save_dir_name, SDO_filename[:-4]), "w") as sh_file:
                sh_file.write(wget_sh)
                SDO_utilities.write_log(log_file,
                                        "{}{}_wget.sh is created...".format(save_dir_name, SDO_filename[:-4]))
        
    except Exception as err : 
        SDO_utilities.write_log(err_log_file,
                                "{2}: {0}, {1}".format(err, target, datetime.now()))
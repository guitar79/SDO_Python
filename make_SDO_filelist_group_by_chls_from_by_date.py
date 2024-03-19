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
        targets.append('{0}_{1}'.format(str(img_size), chl))
  
filelist_dir_name = 'SDO_filelists_by_date/'
save_dir_name = 'SDO_filelists_by_chls/'
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)
    print ('*'*80)
    print ('{0} is created.'.format(save_dir_name))
else : 
    print ('*'*80)
    print ('{0} is already exist.'.format(save_dir_name))
                          
for yr in range(2022,2024) :
    # yr = 2019
    try : 
        SDO_filelists = sorted(glob(os.path.join('{}SDO_filelist_{}*.txt'.format(filelist_dir_name, str(yr)))))

        # 빈 DataFrame 생성
        df = pd.DataFrame()

        for SDO_filelist in SDO_filelists:   
            #SDO_filelist = SDO_filelists[0]
            #make Pandas DataFrame from file
            df_one = pd.read_csv(SDO_filelist)
            df = df.append(df_one)
        print("df: {}".format(df))

    except Exception as err:
        SDO_utilities.write_log(err_log_file,
                        '{2}: {0}, {1}'.format(err, target, datetime.now()))
    try:
        for target in targets :
            #target = targets[0]
            df_target = df[df['#this file is created by guitar79@naver.com'].str.contains(target)]
            df_target.to_csv("{0}{1}_lists_{2}.txt".format(save_dir_name, target, str(yr)))
            SDO_utilities.write_log(err_log_file,
                        "{0}{1}_lists_{2}.txt".format(save_dir_name, target, str(yr)))

    except Exception as err : 
        SDO_utilities.write_log(err_log_file,
                        '{2}: {0}, {1}'.format(err, target, datetime.now()))
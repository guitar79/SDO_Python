# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg

from glob import glob
import os

if not os.path.exists('./log/'):
    os.makedirs('./log/')
    print ('*'*80)
    print ('./log/ is created')

suffix = '4096_HMIB'
save_dir_name = '../suffix_lists/'
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)
    print ('='*80)
    print (save_dir_name, 'is created')

for yr in range(2010,2020) :
    SDO_filelists = sorted(glob(os.path.join('../SDO_filelists/SDO_filelist_{}*.txt'.format(str(yr)))))
    try : 
        all_list = []
        for SDO_filelist in SDO_filelists:   
            read_filename = SDO_filelist
            read_file = open(read_filename,'r')
            raw_lists = read_file.read()
            url_lists = raw_lists.split('\n')
            suffix_list = [s for s in url_lists if suffix in s]
            print(url_lists) #debug
            all_list.extend(suffix_list)
            
        with open("{0}{1}_lists{2}.txt".format(save_dir_name, suffix, str(yr)), "w") as text_file:
            text_file.write("\n".join(all_list))
            print ("{0}{1}_lists{2}.txt is created...".format(save_dir_name, suffix, str(yr)))
    except Exception as err : 
        print(err)
            
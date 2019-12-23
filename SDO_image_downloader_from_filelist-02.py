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

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
targets = ['2048_HMII.jpg','1024_HMII.jpg', '1024_0304.jpg', '1024_4500.jpg', '1024_HMIIB.jpg', '1024_HMIIC.jpg', '1024_0171.jpg', '1024_0131.jpg'] #this tpye of image will be downloading
                       
filelist_dir_name = '../SDO_lists/'

SDO_filelists = sorted(glob(os.path.join('{0}SDO_filelist_*.txt'.format(filelist_dir_name))))

for SDO_filelist in SDO_filelists:
    
    # Open the file with read only permit
    f = open(SDO_filelist,'r')
    all_text = f.read()
    url_lists = all_text.split('\n')
    
    # close the file after reading the lines.
    f.close()

    time_gap = 1 #time gap
    request_hour = range(0,24,time_gap) #make list
    
    for url_list in url_lists:
        SDO_utility.SDO_image_downloader_from_filelist(url_list, targets, request_hour)
# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup
#%%
from glob import glob
from datetime import datetime
import os
import urllib.request

#%%
def filename_to_hour(filename):
    fileinfo = filename.split('_')
    return datetime.strptime(fileinfo[0]+fileinfo[1], '%Y%m%d%H%M%S')
#%%
# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
targets = ['2048_HMII.jpg','1024_HMII.jpg', '1024_0304.jpg', '1024_4500.jpg', '1024_HMIIB.jpg', '1024_HMIIC.jpg', '1024_0171.jpg', '1024_0131.jpg'] #this tpye of image will be downloading

#%%
SDO_filelists = sorted(glob(os.path.join('SDO_filelist_*.txt')))
for SDO_filelist in SDO_filelists:
    #read_filename = 'SDO_filelist_20120101_20120201.txt'
    read_filename = SDO_filelist
    read_file = open(read_filename,'r')
    raw_lists = read_file.read()
    url_lists = raw_lists.split('\n')
    
    read_filename_element1 = read_filename.split('.')
    read_filename_element2 = read_filename_element1[-2].split('_')
    startdate = read_filename_element2[-2] #start date
    enddate = read_filename_element2[-1] #end date
    time_gap = 1 #time gap
    request_hour = range(0,24,time_gap) #make list
    
    #variable for calculating date
    start_date = datetime.date(datetime.strptime(startdate, '%Y%m%d')) #convert startdate to date type
    end_date = datetime.date(datetime.strptime(enddate, '%Y%m%d')) #convert enddate to date type
    duration = (end_date - start_date).days #total days for downloading
    print ('*'*80)
    print ((duration+1), 'days', int((duration+1)*(24/time_gap)), 'files will be downloaded')
    
    #%%
    try : 
        for url_list in url_lists:
            filename_element = url_list.split('/')
            filename = filename_element[-1]
            for target in(targets):
                save_folder = target + '_' + filename_to_hour(filename).strftime('%Y') + '/'
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                    print ('*'*80)
                    print (save_folder, 'is created')
                    
                if (filename[(-len(target)):] == target) \
                    and int(filename_to_hour(filename).strftime('%H')) in(request_hour) :
                    try : 
                        print ('Trying %s' % filename)
                        if os.path.exists('%s/%s' % (save_folder, filename)):
                            print ('*'*40)
                            print (filename + 'is exist')
                        else :
                            urllib.request.urlretrieve(url_list, '%s/%s' % (save_folder, filename))
                            print ('*'*60)
                            print ('Downloading' + filename)
                        
                    except Exception as err : 
                        with open('downloader_errorlog_{0}_{1}.log'.format(startdate, enddate), "a") as downloader_errorlog :
                            downloader_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, target))
                        print ('*'*80)
                        print (err, url_list)
                else:
                    print ('Skipping ' + filename)
    except Exception as err : 
        with open('downloader_errorlog_{0}_{1}.log'.format(startdate, enddate), "a") as downloader_errorlog :
            downloader_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, url_list))
        print ('*'*80)
        print(err, url_list)
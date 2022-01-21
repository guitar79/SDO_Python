# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from glob import glob
import os
from datetime import datetime
import SDO_utilities
import urllib.request
import http.client

suffix = '4096_HMII'
if not os.path.exists('./log/'):
    os.makedirs('./log/')
    print ('*'*80)
    print ('./log/ is created')
                
filelist_dir_name = '../SDO_lists_by_suffix/'
save_dir_name = '../SDO_images/'
SDO_filelists_surffix = sorted(glob(os.path.join('{}SDO_filelist_{}*.txt'.format(filelist_dir_name, suffix))))
print(SDO_filelists_surffix)

   
for SDO_filelist_surffix in SDO_filelists_surffix :

    read_filename = SDO_filelist_surffix
    read_file = open(read_filename,'r')
    raw_lists = read_file.read()
    url_lists = raw_lists.split('\n')
    #print(url_lists) #debug
#    break
    read_filename_element1 = read_filename.split('.')
    #print(read_filename_element1) #debug
    #break
    read_filename_element2 = read_filename_element1[-2].split('_')
    download_date = read_filename_element2[-1] 
    print(download_date) #debug
    
    #convert download date to datetime.date type
    #DT_download_date = datetime.date(datetime.strptime(download_date, '%Y%m%d')) 
    
    #print(DT_download_date) #debug
    
    print ('*'*80)    
    for url_list in url_lists[1:]:
        try : 
            #'https://sdo.gsfc.nasa.gov/assets/img/browse/2010/05/19/20100519_091114_1024_0193.jpg',
            SDO_url_element = url_list.split('/')
            SDO_fullname = SDO_url_element[-1]
            SDO_fullname_element = SDO_fullname.split('.')
            SDO_filename_element = SDO_fullname_element[0].split('_')
            #print(SDO_fullname) #debug
            #break
            
            save_folder = "{}{}/{}/{}/{}/".format(save_dir_name,
                                                  SDO_filename_element[0][:4], 
                                                  SDO_filename_element[0],
                                                  SDO_filename_element[-1],
                                                  SDO_filename_element[-2])
            #print(save_folder) #debug
            
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
                print ('='*80)
                print (save_folder, 'is created')
                
                             
            try : 
                print ('Trying {}'.format(SDO_fullname))
                if os.path.exists('{}{}'.format(save_folder, SDO_fullname)):
                    print ('#'*40)
                    print ('{} is exist'.format(SDO_fullname))
                    
                    remote_file = urllib.request.get(url_list)
                    remote_meta = remote_file.headers['contents-length']
                    local_file = open('{}{}'.format(save_folder, SDO_fullname), 'wb')
                    

                    #----GET FILE SIZE----
                    meta = d.info()

                    print ("Download Details", meta)
file_size = int(meta.getheaders("Content-Length")[0])
                    urllib.request.urlretrieve(url_list, '{}{}'.format(save_folder, SDO_fullname))
                    resp = requests.get(url)
                else :
                    print ('*'*60)
                    print ('Downloading {}'.format(SDO_fullname))
                    urllib.request.urlretrieve(url_list, '{}{}'.format(save_folder, SDO_fullname))
                        
            except Exception as err : 
                with open('./log/download_error_{0}.log'.format(read_filename_element1[-2][-21:]), "a") as download_errorlog :
                    download_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, url_list))
                    print ('#'*40)
                    print (err, url_list)
            
        except Exception as err : 
            with open('./log/download_error_{0}.log'.format(read_filename_element1[-2][-21:]), "a") as download_errorlog :
                download_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, SDO_filelist_surffix ))
            print ('#'*40)
            print(err, SDO_filelist_surffix )
                
        
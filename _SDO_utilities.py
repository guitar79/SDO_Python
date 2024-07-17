# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from datetime import datetime
from urllib.request import urlopen

site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
    
# =============================================================================
# for log file
# =============================================================================
def write_log2(log_file, log_str):
    import os
    with open(log_file, 'a') as log_f:
        log_f.write("{}, {}\n".format(os.path.basename(__file__), log_str))
    return print ("{}, {}\n".format(os.path.basename(__file__), log_str))

def write_log(log_file, log_str):
    import time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = '[' + timestamp + '] ' + log_str
    print (msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')
        
# =============================================================================
# for checking time
# =============================================================================

cht_start_time = datetime.now()
def print_working_time(cht_start_time):
    from datetime import datetime
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))


# =============================================================================

# =============================================================================
def getFullnameListOfallFiles(dirName):
    ##############################################3
    import os
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = sorted(os.listdir(dirName))
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getFullnameListOfallFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

# =============================================================================

# =============================================================================
def getFullnameListOfallsubDirs1(dirName):
    ##############################################3
    import os
    allFiles = list()
    for file in sorted(os.listdir(dirName)):
        d = os.path.join(dirName, file)
        allFiles.append(d)
        if os.path.isdir(d):
            allFiles.extend(getFullnameListOfallsubDirs1(d))

    return allFiles


# =============================================================================

# =============================================================================
def getFullnameListOfallsubDirs(dirName):
    ##############################################3
    import os
    allFiles = list()
    for it in os.scandir(dirName):
        if it.is_dir():
            allFiles.append(it.path)
            allFiles.extend(getFullnameListOfallsubDirs(it))

    return allFiles


# =============================================================================

# =============================================================================

def filename_to_hour(filename):
    fileinfo = filename.split('_')
    return datetime.strptime(fileinfo[0]+fileinfo[1], '%Y%m%d%H%M%S')

# =============================================================================

# =============================================================================

def SDO_image_list_to_filelist_1day(save_dir_name, download_date):
    from bs4 import BeautifulSoup
    
    file_lists = '#this file is created by guitar79@naver.com\n'
    #directory = download_date.strftime('%Y') + '/' + download_date.strftime('%m') + '/' + download_date.strftime('%d') + '/'
    directory = download_date.strftime('%Y/%m/%d/')
    url = site + directory
    print ('*'*80)
    print ('trying %s ' % url)
    
    # using BeutifulSoup for crowling
    soup = BeautifulSoup(urlopen(url), "html.parser")
    print('soup: {}'.format(soup))
    
    # 
    # table_list = soup.find_all('table')
    # print('table_list: {}'.format(table_list))
    
    #
    file_list = soup.find_all('a')
    print('file_list', file_list)
    
    # select file fot downloading
    for i in range(5, len(file_list)):
        filename = file_list[i].text
        file_lists += site + download_date.strftime('%Y/%m/%d/') + filename + '\n'

    return file_lists      
                
            
        
            
    
    
# SDO_Python

가상환경 리스트 보기
> conda env list

#windows
##가상환경 생성하기 (windows)
conda create -n SDO_Python_win_env

##가상환경 시작하기 (windows)
conda activate SDO_Python_win_env

##install module
conda install BeautifulSoup4 spyder

##가상환경 내보내기 (windows)
conda env export > SDO_Python_win_env.yaml

##.yaml 파일로 새로운 가상환경 만들기  (windows)
conda env create -f SDO_Python_win_env.yaml

##deactivate 가상환경 종료
conda deactivate

##가상환경 제거하기 (windows)
conda env remove -n SDO_Python_win_env


#ubuntu

##가상환경 생성하기 (ubuntu)
conda create -n SDO_Python_ubuntu_env

##가상환경 시작하기 (ubuntu)
conda activate SDO_Python_ubuntu_env

##install module
conda install BeautifulSoup4 spyder

##가상환경 내보내기 (ubuntu)
conda env export > SDO_Python_ubuntu_env.yaml

##.yaml 파일로 새로운 가상환경 만들기 (ubuntu)
conda env create -f SDO_Python_ubuntu_env.yaml

##deactivate 가상환경 종료
conda deactivate

##가상환경 제거하기(ubuntu)
conda env remove -n SDO_Python_ubuntu_env

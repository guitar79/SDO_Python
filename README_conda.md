# SDO_Python

가상환경 리스트 보기
> conda env list

#windows
##가상환경 생성하기
conda create -n SDO_Python_env

##가상환경 시작하기 
conda activate SDO_Python_env

##install module
conda install BeautifulSoup4

##가상환경 내보내기
conda env export > SDO_Python_env.yaml

##.yaml 파일로 새로운 가상환경 만들기
conda env create -f SDO_Python_env.yaml

##deactivate 가상환경 종료
conda deactivate

##가상환경 제거하기
conda env remove -n SDO_Python_env
import pyrebase
import os
import json
from requests.packages.urllib3.packages.six.moves import urllib

config={
    "apiKey": "AIzaSyB5r_ChQiHWSjUwuywo-31g6cmzxW-LT9o",
    "authDomain": "twofactor-d19ed.firebaseapp.com",
    "databaseURL": "https://twofactor-d19ed.firebaseio.com",
    "projectId": "twofactor-d19ed",
    "storageBucket": "twofactor-d19ed.appspot.com",
    "messagingSenderId": "415712167872",
    "appId": "1:415712167872:web:9369b71a20494aba992a25",
    "measurementId": "G-93466FBBFV"
}

firebase=pyrebase.initialize_app(config)
firebase.database()
storage=firebase.storage()

#url불러오기
url=storage.get_url(None)

#url 내용 str타입으로 가져오기
url_str=urllib.request.urlopen(url).read().decode('utf-8')

#f=urllib.request.urlopen(path).read()

#str to json
url_json=json.loads(url_str)


#items에 있는 값 모두 가져오기
jsonArray=url_json.get("items")

#list 생성
jsonList=[]

#name에 있는 값 list에 모두 append
for list in jsonArray:
    jsonList.append(list.get("name"))

#print(jsonList[0])

path_on_cloud=jsonList[0]  #storage에서 다운받을 파일경로(파일 이름까지)

file_name=path_on_cloud[:-4] #경로에서 저장할 파일이름 추출->사번으로 저장

#storage.child(path_on_cloud).put(path_local) #storage에 파일 업로드

storage.child(path_on_cloud).download("recogVideo/"+file_name+".mp4") #다운받을때 저장될 파일 이름

dataset_path="C:\\Users\\sksms\\PycharmProjects\\combine1\\data\\data_faces_from_camera"

#dataset에 사용자 이름으로 된 디렉토리 파일 생성해주기
try:
    if not(os.path.isdir(dataset_path+file_name)):
        os.makedirs(os.path.join(dataset_path,file_name))
except OSError as e:
    print("Error:Creating directory."+file_name)

#gather_example.py파일 실행
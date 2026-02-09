import requests
import random
#本库是基于coyote game hub 的http api 所编写的郊狼控制程序（波形篇）
#默认url为"http://127.0.0.1:8920"
#id为客户端id
def getpulse(url,id):
    http=f"{url}/api/v2/game/{id}/pulse_list"
    response = requests.get(http, timeout=5)
    response.raise_for_status()
    data = response.json()
    if data.get("status") != 1:
        return False
    plist = data.get("pulseList", [])
    if not plist:
        return {}
    return {item["name"]: item["id"] for item in plist}
def set(url,id,value):
    http=f"{url}/api/v2/game/{id}/pulse"
    pluse=getpulse(url,id)
    if value not in list(pluse.values()):
        return False
    post={
        "pulseId":value
    }
    try:
        response = requests.post(http, json=post, timeout=5)
        response.raise_for_status()
        data = response.json()
        status = data.get("status")
        if status ==1:
            return True
        else:
            return False
    except :
        return False
def sets(url,id,plist):
    http=f"{url}/api/v2/game/{id}/pulse"
    #检验plist内的值是否有效并剔除无效值
    pluse=getpulse(url,id)
    plist_new=[]
    i=len(plist)
    for i in range(0,i):
        if plist[i] in list(pluse.values()):
            plist_new.append(plist[i])
    plist=plist_new
    #发送post
    if not bool(plist):
        return False
    else:
        post = {
            "pulseId": plist
        }
        try:
            response = requests.post(http, json=post, timeout=5)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            if status == 1:
                return True
            else:
                return False
        except:
            return False
def randomset(url,id):
    pluse=getpulse(url,id)
    plist=list(pluse.values())
    length=len(plist)
    i=random.randint(0,length-1)
    value=plist[i]
    sum=set(url,id,value)
    return sum
def randomsets(url,id,number):
    pluse=getpulse(url,id)
    plist_all=list(pluse.values())
    length=len(plist_all)
    plist=[]
    for j in range(0,number):
        i=random.randint(0,length-1)
        plist.append(plist_all[i])
    sum=sets(url,id,plist)
    return sum

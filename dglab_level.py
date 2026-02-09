import  requests
#本库是基于coyote game hub 的http api 所编写的郊狼控制程序（强度篇）
#默认url为"http://127.0.0.1:8920"
#id为客户端id
#way["not","yes"]是指是否改变强度范围大小
#set - 设置值为goal / add - 增加 add/a 的值 / minus - 减少 add/a 的值
#min-强度最小值/max-强度最大值
def getinfo(url,id):#获取基础信息，返回为词典info
    http=f"{url}/api/v2/game/{id}"
    info={}
    try:
        response = requests.get(http, timeout=5)
        data = response.json()
        level_min = data.get("strengthConfig", {}).get("strength")
        info['level_min'] = level_min
        level_change = data.get("strengthConfig", {}).get("randomStrength")
        info['level_change'] = level_change
        level_max = level_min + level_change
        info['level_max'] = level_max
        level_limit = data.get("clientStrength", {}).get("limit")
        info['level_limit'] = level_limit
    except :
        return info
    return info
def return_level(url,id):#恢复默认强度范围[5,10]
    http = f"{url}/api/v2/game/{id}/strength"
    post1 = {
        "strength": {
            "set": 5
        }
    }
    post2 = {
        "randomStrength": {
            "set": 5
        }
    }
    try:
        response = requests.post(http, json=post1, timeout=5)
        response = requests.post(http, json=post2, timeout=5)
        return 1
    except:
        return 0
def set__min(url,id,goal):
    http = f"{url}/api/v2/game/{id}/strength"
    info = getinfo(url,id)
    limit = info["level_limit"]
    if goal > limit:
        goal=limit
    post = {
        "strength": {
            "set": goal
        }
    }
    try:
        response = requests.post(http, json=post, timeout=5)
        return 1
    except:
        return 0
def add_min(url,id,add,way):
    http = f"{url}/api/v2/game/{id}/strength"
    info = getinfo(url, id)
    level_min = info["level_min"]
    level_change = info["level_change"]
    if way=="not":
        level_limit = info["level_limit"]
        level_min = level_min + add
        level_max = level_min + level_change
        if level_max > level_limit:
            level_change = 0
    else:
        level_min = level_min + add
        level_change=level_change-add
    post1 = {
        "strength": {
            "set": level_min
        }
    }
    post2={
        "randomStrength": {
            "set": level_change
        }
    }
    try:
        response = requests.post(http, json=post1, timeout=5)
        response = requests.post(http, json=post2, timeout=5)
        return 1
    except:
        return 0
def minus_min(url, id, add, way):
    http = f"{url}/api/v2/game/{id}/strength"
    info = getinfo(url, id)
    level_min = info["level_min"]
    level_change = info["level_change"]
    if way == "not":
        pass
    else:
        level_change=level_change+add
    level_min = level_min - add
    if level_min<0:
        level_min=0
    post1 = {
        "strength": {
            "set": level_min
        }
    }
    post2 = {
        "randomStrength": {
            "set": level_change
        }
    }
    try:
        response = requests.post(http, json=post1, timeout=5)
        response = requests.post(http, json=post2, timeout=5)
        return 1
    except:
        return 0
def set_max(url,id,goal,way):
    http = f"{url}/api/v2/game/{id}/strength"
    info = getinfo(url, id)
    level_change=info["level_change"]
    level_limit = info["level_limit"]
    level_max = info["level_max"]
    level_min = info["level_min"]
    if goal > level_limit:
        goal=level_limit
    a = goal - level_max
    if way=="not":
        level_change=level_change+a
    else:
        level_change=level_change+a
        level_min=level_min+a
    post1 = {
        "strength": {
            "set": level_min
        }
    }
    post2={
        "randomStrength": {
            "set": level_change
        }
    }
    try:
        response = requests.post(http, json=post1, timeout=5)
        response = requests.post(http, json=post2, timeout=5)
        return 1
    except:
        return 0
def add_max(url,id,a,way):
    http = f"{url}/api/v2/game/{id}/strength"
    info = getinfo(url, id)
    level_change=info["level_change"]
    level_limit = info["level_limit"]
    level_max = info["level_max"]
    level_min = info["level_min"]
    if level_max+a>level_limit:
        a=level_limit-level_max
    if way=="not":
        level_min=level_min+a
    else:
        level_change=level_change+a
    post1 = {
        "strength": {
            "set": level_min
        }
    }
    post2={
        "randomStrength": {
            "set": level_change
        }
    }
    try:
        response = requests.post(http, json=post1, timeout=5)
        response = requests.post(http, json=post2, timeout=5)
        return 1
    except:
        return 0
def minus_max(url,id,a,way):
    http = f"{url}/api/v2/game/{id}/strength"
    info = getinfo(url, id)
    level_change=info["level_change"]
    level_min = info["level_min"]
    if way=="not":
        level_min=level_min+a
    else:
        level_change=level_change-a
    if level_min<0:
        level_min=0
    post1 = {
        "strength": {
              "set": level_min
       }
    }
    post2={
        "randomStrength": {
            "set": level_change
        }
   }
    try:
        response = requests.post(http, json=post1, timeout=5)
        response = requests.post(http, json=post2, timeout=5)
        return 1
    except:
         return 0
def fire(url,id,value,times):#一键开火（增加value强度[<40]持续times秒[<30]
    http=f"{url}/api/v2/game/{id}/action/fire"
    if times>30:
        times=30
    if value>40:
        value=40
    times=int(times*100)
    post={
        "strength":value,
        "time":times
    }
    try:
        response = requests.post(http, json=post, timeout=5)
        return 1
    except:
        return 0
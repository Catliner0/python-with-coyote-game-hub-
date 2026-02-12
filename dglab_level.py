import requests
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
def post_number(url,id,level_min,level_change):
    http = f"{url}/api/v2/game/{id}/strength"
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
def levels(level_min,level_max):
    level={}
    if level_min>level_max:
        level_min,level_max=level_max,level_min
    level["level_min"] = level_min
    level["level_max"] = level_max
    return level
def post(url,id,level):
    #test
    try:
        level_min = level["level_min"]
        level_max = level["level_max"]
    except:
        return {}
    info=getinfo(url,id)
    level_limit = info["level_limit"]
    if level_max>level_limit :
        level_max=level_limit
    elif level_max<0:
        level_max=0
    if level_min<0:
        level_min=0
    elif level_min>level_limit:
        level_min=level_limit
    level_change=level_max-level_min
    value_return=post_number(url,id,level_min,level_change)#post
    return value_return
def test_error(value_return):
    type_value=type(value_return)
    if type_value=="dict":
        if value_return=={}:
            print("输入的level不符合标准格式{'level_min':level_min,'level_max':level_max},推荐使用levels()函数")
        else:
            print("未知的错误")
    elif type_value=="int":
        if value_return==0:
            print("通讯时出现错误")
        elif value_return==1:
            print("程序已经执行成功；若未生效，请检查id或yotome hub game 运行情况")
        else:
            print("未知的错误")
    else:
        print("未知的错误")
    return 1
def posts(url,id,level):
    value=post(url,id,level)
    if bool(value)==True:
        pass
    else:
        test_error(value)
def return_level(url,id):#返回默认强度[5,10]
    level=levels(5,10)
    post(url,id,level)
def fire(url,id,value,times):#一键开火（增加value强度[<40]持续times秒[<30]
    http=f"{url}/api/v2/game/{id}/action/fire"
    if times>30:
        times=30
    elif times<0:
        times=1
    if value>40:
        value=40
    elif value<0:
        value=0
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
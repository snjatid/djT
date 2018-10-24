import memcache
#连接
mc = memcache.Client(['127.0.0.1:11211'],debug=True)

def set_key(key=None,val=None,time=60):
    if key and val:
        mc.set(key,val,time)
        return True
    return False

def get_key(key=None):
    if key:
        val = mc.get(key)
        return val
    return None


def del_key(key=None):
    if key:
        mc.delete(key)
        return True
    return False

#测试
set_key("username","yangxiaoyuan")
print(get_key("username"))
print(del_key())
print(get_key("username"))

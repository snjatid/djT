import memcache
#连接
mc = memcache.Client(['127.0.0.1:11211'],debug=True)

mc.set(key="username",val="yang",time=60)

print(mc.get("username"))

mc.delete("username")

print(mc.get("username"))

x = {"user":"yang","age":33}

mc.set_multi(x,time=30)

print(mc.get_multi(x))
#全部清空
mc.flush_all()

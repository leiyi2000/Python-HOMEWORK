import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['test']
# 打印数据库
dblist = myclient.list_database_names()
print(dblist)
# 添加数据
mycol = mydb['sites']
mydict = {"name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
x = mycol.insert_one(mydict)
# 返回x为InsertOneResult对象， 包含属性inserted_id
print(x)
print(x.inserted_id)

# 多个文档插入
mylist = [
  {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
  {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
  {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
  {"name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
  {"name": "Github", "alexa": "109", "url": "https://www.github.com"}
]

x = mycol.insert_many(mylist)
print(x.inserted_ids)

# 指定id插入
data = {"_id": 1, "name": "leiyi"}
x = mycol.insert_one(data)
print(x.inserted_id)


# 查询一个

result = mycol.find_one()
print(result)
# 多个查询
for i in mycol.find():
    print(i)

# 指定查询
for i in mycol.find({}, {"_id": 0, "name": 1, "url": 1}):
    print(i)

query = {"name": "RUNOOB"}
for i in mycol.find(query):
    print(i)






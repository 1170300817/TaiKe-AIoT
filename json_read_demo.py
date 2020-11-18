import json

f = open("5f7d755424e3a102c33d1256_test1_20201118084848971_5680", "r")
str = f.read()
f.close()
print(type(str))
print(str)
dict = json.loads(str)
print(type(dict))
print(dict)
print(dict['notify_data']['body']['services'][0]["properties"]["time"])

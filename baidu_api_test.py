import requests
import base64
import json
import cv2

# 百度API相关信息
url_token = "https://aip.baidubce.com/oauth/2.0/token"
data_token = {"grant_type": "client_credentials", "client_id": "Z8eb9VSrPwQjR9Ocpqji783R",
              "client_secret": "hU2eOO3bDfoDxDCEvYr9aV7K2PRvzTlo"}
# 由于post请求的习惯是在body中放入要传给服务器的数据，因此，这里的post方法采用了data参数，而不是params参数。然而，采用params参数也是可以的
resp = requests.post(url_token, data=data_token)
# resp是一个http响应对象，resp.text则是一个json格式的字符串.json.loads()方法可以将json字符串转为字典。
resp_dict = json.loads(resp.text)
# 转为字典之后的好处就是，可以直接从键索引出值，access_token的获取相比用字符串处理要方便得多
access_token = resp_dict["access_token"]
url = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/planttest_1'
# url 参数
params = {'access_token': access_token}
# 请求头
headers = {
    'Content-Type': 'application/json'
}
filename = "G2D4_2020-01-17_21_45_05" + '.jpeg'  # 此时filename形如G2D4_2020-01-17_21_45_05.jpeg
with open(filename, 'rb') as file:  # 打开图片
    pic = base64.b64encode(file.read()).decode()
data = {'image': pic, 'threshold': 0.9}
response = requests.post(url, params=params, headers=headers, data=json.dumps(data))
print(json.loads(response.content))
results_arr = json.loads(response.content)["results"]

im = cv2.imread(filename)
for loc in results_arr:
    sx1 = loc["location"]["left"] - 1
    sy1 = loc["location"]["top"] - 1
    sx2 = loc["location"]["left"] + loc["location"]["width"]
    sy2 = loc["location"]["top"] + loc["location"]["height"]
    cv2.rectangle(im, (int(sx1), int(sy1)), (int(sx2), int(sy2)), (0, 255, 0), 3)
    text = "PER:" + loc["name"] + "  SCORE:" + format(loc["score"], '.4f')
    cv2.putText(im, text, (sx1, sy2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

new_name = "new" + filename
cv2.imwrite(new_name, im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


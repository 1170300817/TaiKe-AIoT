import os
import time
import base64
import cv2
import json
import requests
from obs import ObsClient

# 创建ObsClient实例
obsClient = ObsClient(
    access_key_id='RPGFXM7YS3NPLKWGNQEN',
    secret_access_key='2EBxGrnWk24ouPLdRtOUjdXLvJibHxvLOH4whXxc',
    server='https://obs.cn-north-4.myhuaweicloud.com'
)
# 百度API相关信息
url_token = "https://aip.baidubce.com/oauth/2.0/token"
data_token = {"grant_type": "client_credentials", "client_id": "Z8eb9VSrPwQjR9Ocpqji783R",
              "client_secret": "hU2eOO3bDfoDxDCEvYr9aV7K2PRvzTlo"}


def OBS_up(bucket, object_key, file_path):  # object_key为文件在OBS中的‘路径+名字’，file_path为文件本地地址
    print(object_key)
    resp = obsClient.putFile(bucket, object_key, file_path)
    if resp.status < 300:
        # 输出请求Id
        print('requestId:', resp.requestId)
    else:
        # 输出错误码
        print('errorCode:', resp.errorCode)
        # 输出错误信息
        print('errorMessage:', resp.errorMessage)


def OBS_get_url(bucketName, objectKey):
    res = obsClient.createSignedUrl('GET', bucketName, objectKey, expires=3600)
    url = res['signedUrl']
    print('Getting object using temporary signature url:')
    print(res['signedUrl'])
    return res['signedUrl']


# 调用百度API
def baidu_api(filename):
    resp = requests.post(url_token, data=data_token)
    resp_dict = json.loads(resp.text)
    access_token = resp_dict["access_token"]
    url = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/planttest_1'
    params = {'access_token': access_token}
    headers = {
        'Content-Type': 'application/json'
    }
    with open(filename, 'rb') as file:  # 打开图片
        pic = base64.b64encode(file.read()).decode()
    data = {'image': pic, 'threshold': 0.9}
    response = requests.post(url, params=params,
                             headers=headers, data=json.dumps(data))
    results_arr = json.loads(response.content)["results"]
    im = cv2.imread('/home/pi/Pictures/' + filename)
    for loc in results_arr:
        print(loc)
        sx1 = loc["location"]["left"] - 1
        sy1 = loc["location"]["top"] - 1
        sx2 = loc["location"]["left"] + loc["location"]["width"]
        sy2 = loc["location"]["top"] + loc["location"]["height"]
        cv2.rectangle(im, (int(sx1), int(sy1)), (int(sx2), int(sy2)), (0, 0, 255), 3)
        text = "PER:" + loc["name"] + "  SCORE:" + format(loc["score"], '.4f')
        cv2.putText(im, text, (sx1, sy2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    new_name = '/home/pi/Pictures/' + "new" + filename
    cv2.imwrite(new_name, im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return new_name


if __name__ == '__main__':
    now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    pic_name = 'test1_' + now_time + '.jpg'
    take_pic_command_string = "fswebcam -d /dev/video0 --no-banner -F 20 -r 1920*1080 /home/pi/Pictures/{}".format(
        pic_name)
    os.system(take_pic_command_string)
    # 第一次上传（原始图片）
    OBS_up('taike-raw-image', pic_name, '/home/pi/Pictures/' + pic_name)
    # 获取URL
    obs_url = OBS_get_url('taike-raw-image', pic_name)
    # 调用百度API
    new_name = baidu_api(pic_name)  # name此时形如'G2D4_2020-01-17_21_45_05'

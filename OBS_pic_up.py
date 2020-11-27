import os
import time
from obs import ObsClient

# 创建ObsClient实例
obsClient = ObsClient(
    access_key_id='RPGFXM7YS3NPLKWGNQEN',
    secret_access_key='2EBxGrnWk24ouPLdRtOUjdXLvJibHxvLOH4whXxc',
    server='https://obs.cn-north-4.myhuaweicloud.com'
)


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


if __name__ == '__main__':
    now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    pic_name = 'test1_' + now_time + '.jpg'
    take_pic_command_string = "fswebcam -d /dev/video0 --no-banner -F 20 -r 1920*1080 /home/pi/Pictures/{}".format(
        pic_name)
    os.system(take_pic_command_string)
    # 第一次上传（原始图片）
    OBS_up('taike-raw-image', pic_name, '/home/pi/Pictures/' + pic_name)
    # 获取URL
    OBS_get_url('taike-raw-image', pic_name)

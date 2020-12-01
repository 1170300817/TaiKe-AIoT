# coding: utf-8
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkiotda.v5 import *
import time


def createCommand(client):
    try:
        service_id = "control"
        command_name = "light_on"
        paras = {
            "time": 10
        }
        body = DeviceCommandRequest(paras=paras, service_id=service_id, command_name=command_name)
        device_id = "5f7d755424e3a102c33d1256_test1"
        request = CreateCommandRequest(device_id=device_id, body=body)
        response = client.create_command(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


def getDeviceShadow(client):
    try:
        deviceId = "5f7d755424e3a102c33d1256_test1"
        request = ShowDeviceShadowRequest(device_id=deviceId)
        response = client.show_device_shadow(request)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
    return response


if __name__ == '__main__':
    ak = "RPGFXM7YS3NPLKWGNQEN"
    sk = "2EBxGrnWk24ouPLdRtOUjdXLvJibHxvLOH4whXxc"
    endpoint = "https://iotda.cn-north-4.myhuaweicloud.com"
    project_id = "08efa18de38026502f13c0040bea3098"

    config = HttpConfig.get_default_config()
    config.ignore_ssl_verification = False
    credentials = BasicCredentials(ak, sk, project_id)

    iotda_client = IoTDAClient().new_builder(IoTDAClient) \
        .with_http_config(config) \
        .with_credentials(credentials) \
        .with_endpoint(endpoint) \
        .build()
    # createCommand(iotda_client)
    while True:
        device_shadow = getDeviceShadow(iotda_client)
        light = device_shadow.shadow[0].reported.properties['light']
        print("光照强度为" + light)
        if float(light) < 100:
            print("开始补光")
            createCommand(iotda_client)
        time.sleep(5)

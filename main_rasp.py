# -*- encoding: utf-8 -*-
import time
import logging
import random
import serial

from IoT_device.client.IoT_client_config import IoTClientConfig
from IoT_device.client.IoT_client import IotClient
from IoT_device.request.services_properties import ServicesProperties

# 日志设置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# 全局变量存放传感器数值
data_row = []  # index 0,1,2,3分别为温度湿度光照二氧化碳
# 串口初始化
ser = serial.Serial('/dev/ttyUSB0', 9600)


def run():
    # 客户端配置
    client_cfg = IoTClientConfig(server_ip='iot-mqtts.cn-north-4.myhuaweicloud.com',
                                 device_id='5f7d755424e3a102c33d1256_test1',
                                 secret='12345678', is_ssl=True)

    # 创建设备
    iot_client = IotClient(client_cfg)
    iot_client.connect()  # 建立连接
    iot_client.start()  # 线程启动

    # 第一次上传数据
    serial_get()
    huawei_report(iot_client)
    while True:
        if time.localtime().tm_min % 5 == 0:
            serial_get()
            huawei_report(iot_client)
            time.sleep(60)
        else:
            time.sleep(30)


# 将属性值上报IOTDA服务
def huawei_report(iot_client):
    global data_row
    service_property = ServicesProperties()
    service_property.add_service_property(service_id="sensorData", property='time',
                                          value=time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()))
    service_property.add_service_property(service_id="sensorData", property='temp', value=format(data_row[0], '.1f'))
    service_property.add_service_property(service_id="sensorData", property='humid', value=format(data_row[1], '.1f'))
    service_property.add_service_property(service_id="sensorData", property='light', value=format(data_row[2], '.1f'))
    service_property.add_service_property(service_id="sensorData", property='co2', value=format(data_row[3], '.1f'))
    iot_client.report_properties(service_properties=service_property.service_property, qos=1)


# 获取传感器读数函数
def serial_get():
    if ser.isOpen():
        send_data = '01 03 00 00 00 05 85 C9'
        send_bytes = bytes.fromhex(send_data)
        ser.write(send_bytes)  # 发送读取指令
        time.sleep(0.5)
        len_return = ser.inWaiting()  # 接收数据
        if len_return:  # 解析数据
            return_data = ser.read(len_return)
            hex_data = return_data.hex()
            temp = int(hex_data[6:10], 16)
            temp = 0.1 * temp
            humid = int(hex_data[10:14], 16)
            humid = 0.1 * humid
            light = int(hex_data[14:22], 16)
            light = light
            co2 = int(hex_data[22:26], 16)
            global data_row
            data_row = [temp, humid, light, co2]
            print(data_row)
        else:
            print('no data')
    else:
        print("port open failed")


if __name__ == '__main__':
    run()

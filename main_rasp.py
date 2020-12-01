# -*- encoding: utf-8 -*-
import time
import logging
import random
import threading
import os
import RPi.GPIO as gpio
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

    def command_callback(request_id, command):
        logger.info(('Command, device id:  ', command.device_id))
        logger.info(('Command, service id = ', command.service_id))
        logger.info(('Command, command name: ', command.command_name))
        logger.info(('Command. paras: ', command.paras))
        # result_code:设置为零相应命令下发成功，为 1 下发命令失败
        iot_client.respond_command(request_id, result_code=0)
        if command.command_name == 'fan_on':
            print("风扇开启：" + str(command.paras['time']))
            t1 = threading.Thread(target=fan_on, args=(command.paras['time'],))
            t1.start()
        if command.command_name == 'light_on':
            print("灯光开启：" + str(command.paras['time']))
            t2 = threading.Thread(target=light_on, args=(command.paras['time'],))
            t2.start()
        if command.command_name == 'take_a_pic':
            os.system('sudo python3 OBS_pic_up.py')

    # 设置响应命令的回调
    iot_client.set_command_callback(command_callback)
    iot_client.start()  # 线程启动

    # 第一次上传数据
    serial_get()
    huawei_report(iot_client)
    while True:
        if time.localtime().tm_min % 1 == 0:
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


# 开风扇函数
def fan_on(sec):
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)
    gpio.setup(8, gpio.OUT)
    gpio.output(8, gpio.HIGH)
    threading.Event().wait(sec)
    gpio.output(8, gpio.LOW)


# 开灯函数
def light_on(sec):
    gpio.setwarnings(False)
    R, G, B = 11, 12, 13
    gpio.setmode(gpio.BOARD)
    gpio.setup(R, gpio.OUT)
    gpio.setup(G, gpio.OUT)
    gpio.setup(B, gpio.OUT)
    pwmR = gpio.PWM(R, 100)
    pwmG = gpio.PWM(G, 100)
    pwmB = gpio.PWM(B, 100)
    pwmR.start(0)
    pwmG.start(0)
    pwmB.start(0)
    # 红灯，绿灯，蓝灯全亮（白色）
    pwmR.ChangeDutyCycle(100)
    pwmG.ChangeDutyCycle(100)
    pwmB.ChangeDutyCycle(100)
    threading.Event().wait(sec)
    pwmR.stop()
    pwmG.stop()
    pwmB.stop()
    gpio.cleanup()


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

import requests
import numpy
import cv2
from PIL import Image, ImageDraw, ImageFont


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    image_url = "https://taike-raw-image.obs.cn-north-4.myhuaweicloud.com:443/hzz.jpg?AccessKeyId=RPGFXM7YS3NPLKWGNQEN&Expires=1606997399&Signature=N4Hkq5PmtN2gHUAcn7kiPq/Z0wM%3D"
    api_url = 'https://senseagro.market.alicloudapi.com/api/senseApi'

    appcode = '02daab94c77e49919fe7bec5954f12be'
    header = {
        'Authorization': 'APPCODE ' + appcode
    }
    data = {
        'crop_id': 1,
        'image_url': image_url
    }

    content = requests.post(api_url, headers=header, data=data)
    print(content.text)
    filename="G2D4_2020-01-17_21_45_05.jpeg"
    im = cv2.imread(filename)
    sp = im.shape
    print(sp)
    im = cv2ImgAddText(im, '检测到病症:' + "disease", sp[1] - 350, sp[0] - 35, (255, 0, 0), 30)

    cv2.imwrite('test' + filename, im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

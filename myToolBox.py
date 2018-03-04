import random, string, os, zipfile
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, GT, pair
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def GenRandomSerial(length, Digit=True, Letter=False):
    #生成一个由数字或（和）字符的组成的随机序列
    numOfNum = 0
    numOfLetter = 0
    if Digit == True and Letter == True:
        numOfNum = random.randint(1, length - 1)
        numOfLetter = length - numOfNum
    elif Digit == True:
        numOfNum = length
    elif Letter == True:
        numOfLetter = length
    # 选中 numOfNum 个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    # 选中 numOfLetter 个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    # 打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    # 生成密码
    genPwd = ''.join([i for i in slcChar])
    return genPwd


def getUniqueRandomNum(sum, choice):
    selected = [i for i in range(sum)]
    random.shuffle(selected)
    selected = sorted(selected[:choice])

    return selected

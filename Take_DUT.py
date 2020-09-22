import subprocess
import os
import time
#import INI_r_w
from ast import literal_eval
import json
import serial
from tkinter import messagebox
import ctypes
import time
import shutil
import ADB
#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
#https://github.com/hoangvanmanh34
adb_path = r"D:\Test_Program\module\adb"
class Take_Image_D4():
    def __init__(self):
        self.Refresh_all()

    def Refresh_all(self):
        self.Error_Code = ''
        self.Log_Test = ''
        self.log_add = ''
        self.Log_Data = {}
        self.start_time = time.time()
        self.WIFI_MAC = ''

    def GetContent(self, buf, strstart, strend):
        # strresult="none"
        posstart = buf.find(strstart) + len(strstart)
        buf1 = buf[posstart: len(buf)]
        posend = buf1.find(strend)
        if strend == '':
            posend = len(buf1)
        strresult = buf1[0: posend]
        return strresult

    def Main(self):
        self.Error_Code = "ADB_ERROR"
        '''if not ADB.Send_ADB('adb devices', {1: 'device'}, 1, 0, 5):
            self.Error_Code = "DEVICE"
            return False, self.WIFI_MAC'''
        '''if not ADB.Send_ADB('adb root', {1: 'as', 2: 'root'}, 3, 0, 5):
            self.Error_Code = "DEVICE"
            return False, self.WIFI_MAC
        if not ADB.Send_ADB('adb shell settings put system screen_brightness_mode 1', {}, 1, 0, 5):
            self.Error_Code = "DEVICE"
            return False, self.WIFI_MAC
        if not ADB.Send_ADB('adb shell settings put system screen_off_timeout 600000', {}, 1, 0, 5):
            self.Error_Code = "DEVICE"
            return False, self.WIFI_MAC'''
        '''if not self.Check_WiFi_MAC():return False, self.WIFI_MAC
        self.Error_Code = ""
        return True, self.WIFI_MAC'''
        return True

    def Check_DUT_Alive(self):
        cmd = ADB.Send_ADB('adb devices', {1: 'device'}, 1, 0, 5, unexpect_line='List of devices attached')
        if not cmd[0]:
            self.Error_Code = "DEVICE"
            return False
        return True

    def Send_Command(self, cmd, expect = {}):
        cmd = ADB.Send_ADB(cmd, expect, 1, 0, 5)
        if not cmd[0]:
            self.Error_Code = "ADBFAILED"
            return False
        return True

    def Check_WiFi_MAC(self, itimeout=3):
        self.log_add += '***Check_WiFi_MAC***\r\n'
        cmd = ADB.Send_ADB("adb shell svc wifi enable", {}, 5, 0, 5, 'WiFMAC')
        if not cmd[0]:
            self.Error_Code = cmd[3]
            return False, self.WIFI_MAC
        time.sleep(itimeout)
        cmd = ADB.Send_ADB("adb shell  dumpsys wifi MAC", {1: '90:09:'}, 2, 0, 5, 'WiFMAC')
        if not cmd[0]:
            self.Error_Code = cmd[3]
            return False, self.WIFI_MAC
        log = cmd[1]
        for l in log:
            if l.find('90:09:') >= 0:
                self.WIFI_MAC = self.MAC_end(l.strip()[5:22])
        self.log_add += 'WIFI_MAC:' + self.WIFI_MAC + '\r\n'
        print('WIFI_MAC:' + self.WIFI_MAC)
        if len(self.WIFI_MAC) != 12:
            self.Error_Code = "WiFMAC"
            return False, self.WIFI_MAC
        return True, self.WIFI_MAC

    def Take_Image(self, topfront):
        print('Take_Image')
        if not ADB.Send_ADB('adb shell input keyevent 4', {}, 1, 0, 3):
            self.Error_Code = "DEVICE"
            return False
        if topfront.upper() == 'FRONT':
            if not ADB.Send_ADB('adb shell sh /system/etc/mid/mid.sh  --show  camera1', {1:'Please user order:adb pull  /sdcard/camera1.jpg .'}, 1, 3, 10):
                self.Error_Code = "DEVICE"
                return False
            if not ADB.Send_ADB('adb pull /sdcard/camera1.jpg D:/CameraVI/camera1.jpg', {1:'bytes'}, 1, 0, 3):
                self.Error_Code = "DEVICE"
                return False
        if topfront.upper() == 'TOP':
            if not ADB.Send_ADB('adb shell sh /system/etc/mid/mid.sh  --show  camera0', {1:'Please user order:adb pull  /sdcard/camera0.jpg .'}, 1, 3, 10):
                self.Error_Code = "DEVICE"
                return False
            if not ADB.Send_ADB('adb pull /sdcard/camera0.jpg D:/CameraVI/camera0.jpg', {1:'bytes'}, 1, 0, 3):
                self.Error_Code = "DEVICE"
                return False

    def MAC_end(self, macin):
        maclist = list(macin)
        macend = ''
        for li in maclist:
            if li == ':':
                maclist.remove(':')
        # print(maclist)
        macend = ''.join(map(str, maclist))
        return macend.upper()

    def Open_COM(self):
        try:
            self.ser = serial.Serial(self.Fixture_COM)
            print(self.ser.name)
            time.sleep(0.2)
            self.ser.flush()
            # self.ser.open()
            # self.ser.set_input_flow_control(enable=False)
            # self.ser.set_output_flow_control(enable=False)
            print('COM opened')
        except Exception as e:
            print('Open COM fail')
            print(e)

    def Close_COM(self):
        try:
            self.ser.flush()
            time.sleep(0.2)
            self.ser.close()
        except:
            print('close com fail')
        return True

    def Get_in(self):
        data_de = ''
        if not self.ser.is_open:
            print('re-open com')
            self.Open_COM()
        # time.sleep(0.1)
        # self.ser.flush()
        time.sleep(0.1)
        data_de = self.ser.read_all().strip()
        # time.sleep(0.1)
        self.ser.flush()
        if data_de != b'':
            print(self.ser.name)
            print('Fixture:' + str(data_de))
        return data_de

    def Send_COM(self, scmd):
        try:
            print(scmd)
            end = '\x0d\x0a'
            self.ser.write(scmd.encode() + end.encode())  # +'\r\n')#
        except Exception as e:
            print('send to com fail')
            print(e)

    def Mbox(self, title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

'''if __name__ == "__main__":
    MD = Take_Image_D4()
    if MD.Main():
        MD.Log_Data.update({"RESULT": "PASS"})
        print("Take_Image_D4 PASS")
        MD.Log_Data.update({"ERRORCODE": ""})
    else:
        MD.Log_Data.update({"RESULT": "FAIL"})
        print("Take_Image_D4 FAIL")
        print("Error_Code : " + MD.Error_Code)
        MD.Log_Data.update({"ERRORCODE": MD.Error_Code})
        MD.Log_Test += "Error_Code : " + MD.Error_Code + '\n'
    MD.Save_Log()'''

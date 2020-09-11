import subprocess
import os
import time
from ast import literal_eval
import json
import serial
from tkinter import messagebox
import ctypes
import time
import shutil
import cv2
import numpy as np
import operator
from datetime import datetime
from math import *
#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
class Image_Alz():
    def __init__(self):
        print('Image_Alz')

    def Main(self, mac, topfront, img_path, img_name, cfg_PRODUCT, cfg_SPECIFICATIONS, cfg_OPTION, golden_test=False):
        self.dev_result = 'PASS'
        self.MAC = mac
        dev1 = ['NA', 'NA']
        dev2 = ['NA', 'NA']
        dev3 = ['NA', 'NA']
        self.Offside_X = 'NA'
        self.Offside_Y = 'NA'
        self._Offset = 'NA'
        self.TopFront = topfront.upper()
        print(cfg_SPECIFICATIONS)
        self.OJ_MAX = cfg_SPECIFICATIONS['OJ_MAX']
        self.OJ_MIN = cfg_SPECIFICATIONS['OJ_MIN']
        self.thresh = cfg_OPTION["Thresh"]
        if self.TopFront == 'TOP':
            self.Sample_centre = cfg_PRODUCT['CAMERA_TOP']['GOLDEN_1']
        if self.TopFront == 'FRONT':
            self.Sample_centre = cfg_PRODUCT['CAMERA_FRONT']['GOLDEN_1']
        self.img_path = img_path
        self.save_img_name = img_name
        #self.image = cv2.imread(self.img_path)
        #self.image = cv2.resize(self.image, (800, 504))#(2304, 1536)
        self.image = img_path
        self.cnt_list = []
        self.cnt_list1 = []
        self.cnt_list2 = []
        self.cnt_list3 = []
        self.coor_list1= []
        self.coor_list2 = []
        self.coor_list3 = []
        self.Pretreatment()
        if not self.Start_Alz():
            return False, self.image, [dev1, dev2, dev3], [self.coor_list1, self.coor_list2, self.coor_list3]
        dev1 = self.Deviation(self.coor_list1)
        print(dev1)
        self.Show_Result(self.coor_list1, dev1, 1)
        dev2 = self.Offset(self.coor_list2, golden_test)
        #print('--------------------')
        #print(golden_test)
        if not golden_test:
            print(dev2)
            self.Show_Result(self.coor_list2, dev2, 2)
        print(self.dev_result)
        dev3 = self.Deviation(self.coor_list3)
        print(dev3)
        self.Show_Result(self.coor_list3, dev3, 3)
        #self.Save_Result(dev1[1], dev2[1], dev3[1])
        if self.dev_result != 'PASS':
            return False, self.image, [dev1, dev2, dev3], [self.coor_list1, self.coor_list2, self.coor_list3]
        return True, self.image, [dev1, dev2, dev3], [self.coor_list1, self.coor_list2, self.coor_list3]


    def Pretreatment(self):
        # Grayscale
        self.image = cv2.resize(self.image, (800, 504))
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Find Canny edges
        '''edged = cv2.Canny(gray, 50, 200)
        contours, hierarchy = cv2.findContours(edged,
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)'''
        a, binary = cv2.threshold(gray, self.thresh, 200, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        '''if self.TopFront == 'FRONT':
            boundingBox = [cv2.boundingRect(c) for c in contours]
            (contours, boundingBoxs) = zip(*sorted(zip(contours, boundingBox), key=lambda b: b[1][0], reverse=False))'''

        #print("Number of Contours found = " + str(len(contours)))
        self.cnt_list = []
        if len(contours) > 1:
            for c in range(0, len(contours)):
                try:
                    sx, sy, sw, sh = cv2.boundingRect(contours[c])
                    d_area = cv2.contourArea(contours[c])
                    
                    # print(xy)
                    #cv2.drawContours(self.image, contours, -1, (0, 255, 0), 2)
                    '''cv2.putText(self.image, str(d_area), (scX, scY),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0),
                                1, cv2.LINE_AA)'''
                    if d_area > self.OJ_MIN and d_area < self.OJ_MAX and sx > 50 and sy > 50 and sx < 700 and sy < 450:
                        print('---------------')
                        print(d_area)
                        print('---------------')
                        sM = cv2.moments(contours[c])
                        scX = int(sM["m10"] / sM["m00"])
                        scY = int(sM["m01"] / sM["m00"])
                        xy = [scX, scY, round(sh / 2)]
                        if scX > 50 and scY > 50 and scX < 700 and scY < 450:
                            self.cnt_list.append(contours[c])

                except Exception as e:
                    print(e)
                    #continue

    def Start_Alz(self):
        try:
            '''self.image1 = cv2.resize(self.image, (800, 504))
            cv2.drawContours(self.image1, self.cnt_list, -1, (0, 255, 0), 3)
            cv2.imshow('ss', self.image1)
            cv2.waitKey()
            print('Block num: ' + str(len(self.cnt_list)))
            for i in range(0, len(self.cnt_list)):
                sx, sy, sw, sh = cv2.boundingRect(self.cnt_list[i])
                d_area = cv2.contourArea(self.cnt_list[i])
                sM = cv2.moments(self.cnt_list[i])
                scX = int(sM["m10"] / sM["m00"])
                scY = int(sM["m01"] / sM["m00"])
                xy = [scX, scY, round(sh / 2)]
                print(str(i) + ':' + str(sx) + '-' + str(sy) + ', ' + str(d_area))
                self.coor_list1.append([sx, sy, sw, sh, scX, scY, d_area])
                # self.coor_list1.append([scX, scY])
                cv2.circle(self.image, (scX, scY), 2, (0, 255, 0), 6)
                cv2.putText(self.image, str(i)+':'+str(scX)+':'+str(scY), (scX, scY), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0),
                            1, cv2.LINE_AA)
            print('++++++++++++')'''
            
            if len(self.cnt_list) != 5:
                print('FAIL')
                return False
            self.cnt_list1 = [self.cnt_list[0], self.cnt_list[1]]
            self.cnt_list2 = [self.cnt_list[2]]
            self.cnt_list3 = [self.cnt_list[3], self.cnt_list[4]]

            for i in range(0, len(self.cnt_list1)):
                sx, sy, sw, sh = cv2.boundingRect(self.cnt_list1[i])
                d_area = cv2.contourArea(self.cnt_list1[i])
                sM = cv2.moments(self.cnt_list1[i])
                scX = int(sM["m10"] / sM["m00"])
                scY = int(sM["m01"] / sM["m00"])
                xy = [scX, scY, round(sh / 2)]
                print(str(i) + ':' + str(sx) + '-' + str(sy) + ', ' + str(d_area))
                self.coor_list1.append([sx, sy, sw, sh, scX, scY, d_area])
                # self.coor_list1.append([scX, scY])
                cv2.circle(self.image, (scX, scY), 2, (0, 255, 0), 6)
                # cv2.putText(self.image, str(i)+':'+str(scX)+':'+str(scY), (scX, scY), cv2.FONT_HERSHEY_SIMPLEX,
                #            1, (0, 112, 255),
                #            1, cv2.LINE_AA)
            print('===================================')
            for i in range(0, len(self.cnt_list2)):
                sx, sy, sw, sh = cv2.boundingRect(self.cnt_list2[i])
                d_area = cv2.contourArea(self.cnt_list2[i])
                sM = cv2.moments(self.cnt_list2[i])
                scX = int(sM["m10"] / sM["m00"])
                scY = int(sM["m01"] / sM["m00"])
                xy = [scX, scY, round(sh / 2)]
                print(str(i) + ':' + str(sx) + '-' + str(sy) + ', ' + str(d_area))
                self.coor_list2.append([sx, sy, sw, sh, scX, scY, d_area])
                # self.coor_list2.append([scX, scY])
                cv2.circle(self.image, (scX, scY), 2, (0, 255, 0), 6)
                # cv2.putText(self.image, str(i)+':'+str(scX)+':'+str(scY), (scX, scY), cv2.FONT_HERSHEY_SIMPLEX,
                #            1, (0, 112, 255),
                #            1, cv2.LINE_AA)
            print('===================================')
            for i in range(0, len(self.cnt_list3)):
                sx, sy, sw, sh = cv2.boundingRect(self.cnt_list3[i])
                d_area = cv2.contourArea(self.cnt_list3[i])
                sM = cv2.moments(self.cnt_list3[i])
                scX = int(sM["m10"] / sM["m00"])
                scY = int(sM["m01"] / sM["m00"])
                xy = [scX, scY, round(sh / 2)]
                print(str(i) + ':' + str(sx) + '-' + str(sy) + ', ' + str(d_area))
                self.coor_list3.append([sx, sy, sw, sh, scX, scY, d_area])
                # self.coor_list3.append([scX, scY])
                cv2.circle(self.image, (scX, scY), 2, (0, 255, 0), 6)
                # cv2.putText(self.image, str(i)+':'+str(scX)+':'+str(scY), (scX, scY), cv2.FONT_HERSHEY_SIMPLEX,
                #            1, (0, 112, 255),
                #            1, cv2.LINE_AA)
            print('===================================')
            if self.TopFront == 'TOP':
                self.coor_list1 = self.Sort(self.coor_list1, 0)
                self.coor_list2 = self.Sort(self.coor_list2, 0)
                self.coor_list3 = self.Sort(self.coor_list3, 0)
            if self.TopFront == 'FRONT':
                self.coor_list1 = self.Sort(self.coor_list1, 5)
                self.coor_list2 = self.Sort(self.coor_list2, 5)
                self.coor_list3 = self.Sort(self.coor_list3, 5)
            print(self.coor_list1)
            print(self.coor_list2)
            print(self.coor_list3)
            return True
        except Exception as e:
            print(e)
            return False

    def Show_Result(self, lineS, dev, index):
        try:
            color = (0,0,255)
            print(dev[0])
            if dev[0]:
                color = (255, 200, 0)
            print(lineS)
            if index == 2:
                cv2.putText(self.image, str(dev[1]), (lineS[0][4], lineS[0][5]), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
                cv2.circle(self.image, (self.Sample_centre[0][4], self.Sample_centre[0][5]), 22, (0, 255, 0), 2)
            else:
                '''cv2.line(self.image, (lineS[0][0], lineS[0][1]),
                             (lineS[-1][0] + lineS[0][2], lineS[-1][1]), color, 2)'''
                '''if self.TopFront == 'TOP':
                    cv2.line(self.image, (lineS[0][0], lineS[0][1]),
                             (lineS[-1][0] + lineS[0][2], lineS[-1][1]), color, 2)
                if self.TopFront == 'FRONT':
                    cv2.line(self.image, (lineS[0][0], lineS[0][1]),
                             (lineS[-1][0], lineS[-1][1] + lineS[0][1]), color, 2)'''
                cv2.line(self.image, (lineS[0][4], lineS[0][5]),
                        (lineS[-1][4], lineS[-1][5]), color, 2)
                cv2.putText(self.image, str(dev[1]), (round((lineS[-1][4] + lineS[0][3] + lineS[0][4]) / 2), lineS[0][5]),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
                cv2.circle(self.image, (self.Sample_centre[0][4], self.Sample_centre[0][5]), 2, (255, 0, 0), 6)
            return True
        except Exception as e:
            print(e)
            print('fail show')
            return False

    def Save_Result(self, dev1, dev2, dev3):
        self.Save_Log(dev1, dev2, dev3)
        #self.image = cv2.resize(self.image, (int(self.image.shape[1]/2.5), int(self.image.shape[0]/2.5)))
        #cv2.imshow('Contours', self.image)
        #cv2.waitKey(0)

    def Save_Log(self, dev1, dev2, dev3):
        datetosave = str(datetime.now().__format__('%d-%B-%Y'))
        timetosave = str(datetime.now().__format__('%d-%B-%Y_%H-%M-%S'))
        full_savedir = 'D:/Logs/CameraVI/' + datetosave
        if not os.path.isdir(full_savedir): os.makedirs(full_savedir)
        if not os.path.isdir(full_savedir + '\\images'): os.makedirs(full_savedir + '\\images')
        cv2.imwrite(full_savedir + '\\images\\' + self.MAC + '_' + timetosave + '.jpg', self.image)
        if not os.path.isfile(full_savedir + '/Camera_Log.txt'):
            sum_file = open(full_savedir + '/Camera_Log.txt', 'w')
            Sum_File_Head = 'MAC\tTOP/FRONT\tRESULT\tDATE_TIME\tLINE_1\tOFFSET\tLINE_2\n'
            sum_file.write(Sum_File_Head)
            sum_file.close()
            time.sleep(0.5)
        sum_file = open(full_savedir + '/Camera_Log.txt', 'a')
        sum_file.write(self.MAC + '\t' + str(self.TopFront).upper() + '\t' + self.dev_result + '\t' + timetosave + '\t' + str(dev1) + '\t' + str(dev2) + '\t' + str(dev3) + '\n')
        sum_file.close()

    def Sort(self, sub_li, topfront):
        l = len(sub_li)
        for i in range(0, l):
            for j in range(0, l - i - 1):
                if (sub_li[j][topfront] > sub_li[j + 1][topfront]):
                    tempo = sub_li[j]
                    sub_li[j] = sub_li[j + 1]
                    sub_li[j + 1] = tempo
        return sub_li

    def Deviation(self, lineS):
        dev_result = 'NA'
        try:
            print('*************************')
            print(lineS)
            print('*************************')
            dev = np.arctan2(lineS[-1][5] - lineS[0][5], lineS[-1][4] - lineS[0][4]) * 180 / np.pi
            dev_result = round(dev, 2)
            if abs(dev) > 90:
                dev_result = round(180 - dev_result, 2)
            if abs(dev_result) > 0.6:
                self.dev_result = 'FAIL'
                return False, dev_result
            else:
                #self.dev_result = 'FAIL'
                return True, dev_result
            '''elif abs(180 - dev_result) < 0.6:
                dev_result = round(abs(180 - dev_result),2)
                #self.dev_result = 'PASS'
                return True, dev_result'''
            
            '''if self.TopFront == 'TOP':
                dev = np.arctan2(lineS[-1][5] - lineS[0][5], lineS[-1][4] - lineS[0][4]) * 180 / np.pi
                dev_result = round(dev, 2)
                if abs(round(dev, 2)) > 1:
                    self.dev_result = 'FAIL'
                    return False, dev_result
                return True, dev_result
            if self.TopFront == 'FRONT':
                dev = np.arctan2(lineS[-1][4] - lineS[0][4], lineS[-1][5] - lineS[0][5]) * 180 / np.pi
                dev_result = round(dev, 2)
                if abs(round(dev, 2)) > 1:
                    self.dev_result = 'FAIL'
                    return False, dev_result
                return True, dev_result
            return False, dev_result'''
        except Exception as e:
            print(e)
            self.dev_result = 'FAIL'
            print('fail dev')
            return False, dev_result

    def Offset(self, lineS, golden_test):
        try:
            voffset_Hoz = pow(lineS[0][4] - self.Sample_centre[0][4], 2)
            voffset_Ver = pow(lineS[0][5] - self.Sample_centre[0][5], 2)
            self._Offset = round(sqrt(voffset_Hoz + voffset_Ver), 2)
            if self._Offset > 20:# and not golden_test:
                self.dev_result = 'FAIL'
                return False, self._Offset
            return True, self._Offset
        except Exception as e:
            print(e)
            return False, self._Offset

    def Offside(self, lineS):
        try:
            voffside_X = abs(lineS[0][4] - self.Sample_centre[0][4])
            voffside_Y = abs(lineS[0][5] - self.Sample_centre[0][5])
            self.Offside_X = voffside_X
            self.Offside_Y = voffside_Y
            if self.Offside_X > 100 or self.Offside_Y > 100:
                self.dev_result = 'FAIL'
                return False, (self.Offside_X, self.Offside_Y)
            return True, (self.Offside_X, self.Offside_Y)
        except Exception as e:
            print(e)
            return False, (self.Offside_X, self.Offside_Y)


#iFucn = Image_Alz()
#iFucn.Main('images\\D4_Camera\\new_camera\\030_camera0.jpg')
#iFucn.Main('images\\D4_Camera\\1_camera0.jpg')

#a  = np.arctan2(443-439, 1395-541)*180/np.pi
#print('Deviation: '+str(round(a,2)))

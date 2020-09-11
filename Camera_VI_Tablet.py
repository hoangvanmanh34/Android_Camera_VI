import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
import cv2
import PIL.Image, PIL.ImageTk
import time
import imutils
import numpy as np
from tkinter import *
from threading import Thread
from PIL import Image, ImageTk
import os
import Camera_D4
import Take_DUT
from tkinter import messagebox
import tempfile
from win32api import GetSystemMetrics
import socket
from ast import literal_eval
import hashlib
import json
from dannyview import DannyViewer
import subprocess
#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
ftemp = tempfile.TemporaryDirectory()
class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #self.window = master
        self.Screen_Width = GetSystemMetrics(0)
        self.Screen_Height = GetSystemMetrics(1)
        self.logwidth = int(self.Screen_Width / 3 - 20)
        self.logheight = int(self.Screen_Height / 3 - 20)
        self.cwidth = int(self.Screen_Width / 3 * 2)
        self.cheight = int(self.Screen_Height / 3 * 2)
        self.master.title('Danny. CameraVI')
        self.grid()
        #self.master.rowconfigure(100, weight=1)
        #self.master.columnconfigure(10, weight=1)
        Frame.__init__(self, master)
        self.grid()
        self.PC_Name = socket.gethostname()
        self.PC_IP_Addr = socket.getaddrinfo(socket.gethostname(), None)
        self.master.title("Camera_VI.     @Danny_TE_2020")
        self.tStyle = ttk.Style()
        self.tStyle.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.tStyle.configure('green.Horizontal.TProgressbar', foreground='green', background='green')
        #print(self.tStyle.theme_names())
        # ---------------------------------------------------------------------
        self.master.rowconfigure(13, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.Frame1 = Frame(master, bg="lightskyblue")
        self.Frame1.grid(row=0, column=0, sticky=W + E + N + S, pady=10, padx=5)
        self.Frame2 = Frame(master, bg="lightskyblue")
        self.Frame2.grid(row=1, column=0, sticky=W + E + N + S, pady=10, padx=5)
        self.Frame3 = Frame(master, bg="lightskyblue")
        self.Frame3.grid(row=0, column=1, sticky=W + E + N + S, pady=10, padx=5)
        self.Frame4 = Frame(master, bg="lightskyblue")
        self.Frame4.grid(row=1, rowspan=10, column=1, columnspan = 5, sticky=W + E + N + S, pady=10, padx=5)
        # -------create user interface--------------------------------------------------
        menuBar = Menu(self.master)
        self.master.config(menu=menuBar)
        self.fileMenu = Menu(menuBar, tearoff=0)
        self.fileMenu.add_command(label="Configure", command=None)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Start", command=self.Play)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Golden Test", command=self.Golden_Test)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Test Without Product", command=self.Manual_Test)
        self.fileMenu.add_separator()
        menuBar.add_cascade(label="File", menu=self.fileMenu)

        self.MITMenu = Menu(menuBar, tearoff=0)
        self.MITMenu.add_command(label="MIT", command=None)
        self.MITMenu.add_separator()
        self.MITMenu.add_command(label="Touch", command=self.MIT)
        self.MITMenu.add_separator()
        menuBar.add_cascade(label="MIT", menu=self.MITMenu)
        # --------------------------------------------
        self.lbStation = tk.Label(self.Frame1, text='CAMERA VI', borderwidth=4, font='serif 25',
                                  width=14, height=2, bg='white', fg='black')
        self.lbStation.grid(row=0, column=0, sticky=E, padx=5, pady=5)
        # --------------------------------------------
        self.lbStatus = tk.Label(self.Frame1, text='STANDBY', borderwidth=4, font='serif 25',
                                 width=31, height=2,
                                 bg='white', fg='blue')
        self.lbStatus.grid(row=0, column=1, columnspan=2, sticky=W, padx=5, pady=5)
        # -------------------------------------------
        '''self.lbTime = tk.Label(self.Frame1, text='TIME', borderwidth=4, font='serif 25',
                               width=10, height=2,
                               bg='white', fg='black')
        self.lbTime.grid(row=0, column=2, sticky=W, padx=5, pady=5)'''
        # --------------------------------------------
        self.canvas = Canvas(self.Frame2, width=self.cwidth-30, height=self.cheight)
        self.canvas.grid(row=0, rowspan=10, column=0, columnspan=6, sticky=W + E + N + S, padx=5)
        # --------------------------------------------
        self.lbspace1 = tk.Label(self.Frame3, text='    ', borderwidth=4, font='serif 14',
                                 bg='lightskyblue', fg='black')
        self.lbspace1.grid(row=0, column=0, sticky=W)
        self.lbspace2 = tk.Label(self.Frame3, text='   ', borderwidth=4, font='serif 14',
                                 bg='lightskyblue', fg='black')
        self.lbspace2.grid(row=2, column=0, sticky=W)
        self.progress_bar = ttk.Progressbar(self.Frame3, orient="horizontal", mode="determinate", maximum=40, value=0, length=400)
        self.progress_bar.grid(row=1, rowspan=2, column=0, sticky=W)
        # -------------------------------------------
        self.bCameraSelect = IntVar()
        self.bCameraSelect.set(0)
        self.btnChangeCamera = Button(self.Frame4, text="Switch", fg='white', bg='blue', font='serif 14', width=6,
                              command=self.btnSwitch)
        self.btnChangeCamera.grid(row=0, column=0, sticky=W)
        self.rNone = tk.Radiobutton(self.Frame4, text="STOP", variable=self.bCameraSelect, value=0,
                         bg="lightskyblue",	highlightbackground="green", font='serif 14', command=self.rChange, selectcolor="red")
        #self.rNone.grid(row=0, column=0, sticky=W)

        self.rTop = Radiobutton(self.Frame4, text="CAMERA TOP", variable=self.bCameraSelect, value=1,
                         bg="lightskyblue",	highlightbackground="green", font='serif 14', command=self.rChange, selectcolor="white")
        self.rTop.grid(row=0, column=1, sticky=W)

        self.rFront = tk.Radiobutton(self.Frame4, text="CAMERA FRONT", variable=self.bCameraSelect, value=2,
                         bg="lightskyblue",	highlightbackground="green", font='serif 14', command=self.rChange, selectcolor="white")
        self.rFront.grid(row=0, column=2, sticky=W)
        # -------------------------------------------
        '''self.btnPlay = Button(self.Frame4, text="View_Screen", fg='white', bg='blue', font='serif 14', width=15,
                              command=self.View_Direct)
        self.btnPlay.grid(row=0, column=0, sticky=W)
        self.btnContinue = Button(self.Frame4, text="Continue", fg='white', bg='blue', font='serif 14', width=15,
                              command=self.Continue_test)
        self.btnContinue.grid(row=0, column=1, sticky=W, padx=5)'''

        self.log = Text(self.Frame4, height=26, width=48, font='serif 12')
        self.log.grid(row=1, column=0, columnspan=3, sticky=W, pady=5)
        scrollb = Scrollbar(self.Frame4, command=self.log.yview)
        scrollb.grid(row=1, column=3, sticky='nsew', pady=5)
        self.log['yscrollcommand'] = scrollb.set

        self.iFucn = Camera_D4.Image_Alz()
        self.iTake = Take_DUT.Take_Image_D4()
        self.isRun = False
        self.Start_Time = time.time()  # datetime.now()
        self.End_Time = time.time()
        self.Test_Flag = False
        self.Allo_Continue = True
        self.countTime = 0
        self.TimeOut = 300
        self.CAMloaded = False
        self._isManual_Test = False
        self.OLD_WIFI_MAC = ''
        self._isGoldenTest = False
        self.bfront = True
        self.btop = False
        self.bViewScreen = False
        self._brChange = False
        self.cfg_value_list = {}
        self.Load_CFG()
        #self.Golden_Test()
        self.Play()
        #self.rChange_update()

    def rChange_update(self):
        Thread(target=self.rChange).start()

    def rChange(self):
        self._brChange = True
        rValue = self.bCameraSelect.get()
        self.Change_Camera_Product()
        self.canvas.delete('all')
        if rValue == 0:
            self.rNone.configure(selectcolor="red")
            self.rFront.configure(selectcolor="white")
            self.rTop.configure(selectcolor="white")
        elif rValue == 1:
            self.rTop.configure(selectcolor="red")
            self.rFront.configure(selectcolor="white")
            self.rNone.configure(selectcolor="white")
        elif rValue == 2:
            self.rFront.configure(selectcolor="red")
            self.rTop.configure(selectcolor="white")
            self.rNone.configure(selectcolor="white")
        self._brChange = False
        self.Allow_Update = True

    def Load_CFG(self):
        CFG_file = open('D:\\CameraVI\\camera.json', 'r')
        CFG_data = CFG_file.read().strip()
        CFG_file.close()
        self.cfg_value_list = literal_eval(CFG_data)
        self.cfg_PRODUCT = self.cfg_value_list['PRODUCT']
        self.cfg_SPECIFICATIONS = self.cfg_value_list['SPECIFICATIONS']
        self.cfg_OPTION = self.cfg_value_list['OPTION']

    def Play(self):
        Thread(target=self.Check_DUT_Alive).start()

    def Continue_test(self):
        Thread(target=self.Close_Camera_To_Adjust).start()
        self.isRun = False
        self.Test_Flag = False

    def Change_theme(self, itheme, istyle):
        self.tStyle.theme_use('winnative')
        self.tStyle.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        self.tStyle.configure('green.Horizontal.TProgressbar', foreground='limegreen', background='limegreen')
        mstyle = istyle.lower()+'.Horizontal.TProgressbar'
        self.progress_bar.configure(style=mstyle)

    def Update_Progress(self, value, itheme, istyle):
        self.Change_theme(itheme, istyle)
        self.progress_bar['value'] = value
        self.progress_bar.update_idletasks()

    def Check_DUT_Alive(self):
        while True:
            try:
                if self.bCameraSelect.get() == 0 and not self._isGoldenTest and not self._isManual_Test and not self.bViewScreen:
                    self.lbStatus.configure(text='STANDBY', fg='blue')
                self.countTime = 0
                #self.Test_Flag = False
                alive = False
                if not self.isRun and not self._isGoldenTest and not self._isManual_Test:
                    alive = self.iTake.Check_DUT_Alive()
                #print('alive:'+str(alive))
                if alive:
                    if not self.isRun and not self.bViewScreen and not self._isGoldenTest and not self._isManual_Test:
                        self.lbStatus.configure(text='RUNNING', fg='gold')
                        self.bViewScreen = True
                        Take_DUT.Take_Image_D4.Send_Command('', 'adb kill-server')
                        '''for i in range(0, 10):
                            #os.system('taskkill /f /im adb.exe')
                            subprocess.call('taskkill /f /im adb.exe', shell=True)'''
                        time.sleep(2)
                        self.View_Direct()
                else:
                    if not self._isGoldenTest and not self._isManual_Test:
                        self.isRun = False
                        self.Test_Flag = False
                        self.bViewScreen = False
                        self.bCameraSelect.set(0)
                        
            except Exception as e:
                print(e)
            time.sleep(1)

    def Golden_Test(self):
        self.isRun = True
        self.Test_Flag = True
        self._isGoldenTest = True
        self.Allow_Update = False
        self.bViewScreen = False
        if messagebox.askokcancel('Golden Test Task', 'Bạn có muốn Test Golden không ?\n Do you want to Test Golden ?',
                                  icon='warning'):
            if os.path.isfile('D:\\CameraVI\\me.id'):
                USER_INP = simpledialog.askstring(title="ME password", prompt="Enter Password", show='#')
                usercode = hashlib.md5(USER_INP.encode()).hexdigest()
                ufile = open('D:\\CameraVI\\me.id', 'r')
                ufinfo = ufile.read()
                if usercode.upper() == str(ufinfo).upper():
                    self._isGoldenTest = True
                    Thread(target=self._golden_test).start()
                else:
                    tk.messagebox.askquestion('User warning', 'Mật khẩu không đúng, liên hệ với chủ quản của bạn !\r\nPassword does not match, pls contact your leader!',
                                              icon='warning')
                    self._isGoldenTest = False
                    self.isRun = False
                    self.Test_Flag = False
                    self.Allow_Update = True
            else:
                tk.messagebox.askquestion('User warning', 'Không có thông tin người dùng, liên hệ với chủ quản của bạn !\r\nNo user info, pls contact your leader!',
                                          icon='warning')
                self._isGoldenTest = False
                self.isRun = False
                self.Test_Flag = False
                self.Allow_Update = True
        else:
            self._isGoldenTest = False
            self.isRun = False
            self.Test_Flag = False
            self.Allow_Update = True

    def _golden_test(self):
        self.Allow_Update = False
        self.isRun = True
        self.Test_Flag = True
        self.Main(golden_test=True)
        self.isRun = False
        self.Test_Flag = False
        self._isGoldenTest = False
        self.Allow_Update = True
        self.bViewScreen = True
        self.isRun = False

    def Manual_Test(self):
        self.isRun = True
        self.Test_Flag = True
        self._isGoldenTest = True
        self._isManual_Test = True
        self.bViewScreen = False
        self.Load_CFG()
        if messagebox.askokcancel('Golden Test Task', 'Bạn có muốn Test Manual không ?\n Do you want to Test Manual ?',
                                  icon='warning'):
            if os.path.isfile('D:\\CameraVI\\me.id'):
                USER_INP = simpledialog.askstring(title="ME password", prompt="Enter Password", show='#')
                usercode = hashlib.md5(USER_INP.encode()).hexdigest()
                ufile = open('D:\\CameraVI\\me.id', 'r')
                ufinfo = ufile.read()
                if usercode.upper() == str(ufinfo).upper():
                    self._isManual_Test = True
                    Thread(target=self._manual_test).start()
                else:
                    tk.messagebox.askquestion('User warning', 'Mật khẩu không đúng, liên hệ với chủ quản của bạn !\r\nPassword does not match, pls contact your leader!',
                                              icon='warning')
                    self._isGoldenTest = False
                    self.isRun = False
                    self.Test_Flag = False
                    self._isManual_Test = False
            else:
                tk.messagebox.askquestion('User warning', 'Không có thông tin người dùng, liên hệ với chủ quản của bạn !\r\nNo user info, pls contact your leader!',
                                          icon='warning')
                #root.destroy()
                self._isGoldenTest = False
                self.isRun = False
                self.Test_Flag = False
                self._isManual_Test = False
        else:
            self._isGoldenTest = False
            self.isRun = False
            self.Test_Flag = False
            self._isManual_Test = False

    def _manual_test(self):
        self.Manual()
        self.isRun = False
        self.Test_Flag = False
        self._isGoldenTest = True
        self._isManual_Test = True
        self.bViewScreen = True

    def Main(self, golden_test=False):
        try:
            self.Load_CFG()
            self.Test_Flag = True
            self.countTime = 0
            #Thread(target=self.Test_Time()).start()
            if os.path.isfile('D:\\CameraVI\\camera0.jpg'):
                os.remove('D:\\CameraVI\\camera0.jpg')
            if os.path.isfile('D:\\CameraVI\\camera1.jpg'):
                os.remove('D:\\CameraVI\\camera1.jpg')
            self.Update_Progress(10, itheme='default', istyle='green')
            self.log.delete(1.0, END)
            self.log.insert(END, '-->Start test\r\n')
            self.isRun = True
            self.canvas.delete('all')
            self.lbStatus.configure(text='RUNNING', fg='gold')
            takeMain = self.iTake.Main()
            self.lbStatus.configure(text='CHECK MAC', fg='gold')
            self.log.insert(END, '-->CHECK MAC\r\n')
            mac = self.iTake.Check_WiFi_MAC(5)
            # result = iFucn.Main('030_camera0', 'TOP', 'images\\D4_Camera\\new_camera\\030_camera0.jpg', '030_camera0')
            # result = iFucn.Main('073_camera1', 'FRONT', 'images\\D4_Camera\\new_camera\\073_camera1.jpg', '073_camera1')
            # result = iFucn.Main('030_camera0', 'TOP', 'images\\D4_Camera\\new_camera\\030_camera0.jpg', '030_camera0')
            # result = iFucn.Main('1_camera0', 'TOP', 'images\\D4_Camera\\1_camera0.jpg','1_camera0')
            # result = iFucn.Main('2_camera0', 'TOP', 'images\\D4_Camera\\1_camera0.jpg','2_camera0')
            # result = iFucn.Main(mac, 'FRONT', 'images\\D4_Camera\\2_camera1.jpg', '2_camera1')

            if mac[0]:
                self.OLD_WIFI_MAC = mac[1]
                self.log.insert(END, '-->'+str(mac)+'\r\n')
                self.log.insert(END, '-->CHECK MAC PASS\r\n\n')
                self.Update_Progress(20, itheme='default', istyle='green')
                self.lbStatus.configure(text='CHECK CAMERA FRONT', fg='gold')
                self.log.insert(END, '-->CHECK CAMERA FRONT\r\n')
                self.log.insert(END, '-->Parallela spec: [-2:2]\r\n')
                self.log.insert(END, '-->OffSide spec: [100]\r\n')
                self.bfront = True
                img_data = self.iTake.Take_Image('FRONT')
                if golden_test:
                    result = self.iFucn.Main(mac[1], 'FRONT', 'D:\\CameraVI\\camera1.jpg', 'camera1', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION, golden_test)
                else:
                    result = self.iFucn.Main(mac[1], 'FRONT', 'D:\\CameraVI\\camera1.jpg', 'camera1', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION)
                self.log.insert(END, '-->Result: '+ str(result[0]) + ',' + str(result[2]) +'\r\n')
                self.Allow_Update = False
                self.photo = PIL.Image.fromarray(result[1])
                #self.photo.thumbnail((self.cwidth, self.cheight))
                self.photo = PIL.ImageTk.PhotoImage(image=self.photo)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                if not result[0]:
                    self.Update_Progress(40, itheme='clam', istyle='red')
                    self.lbStatus.configure(text='CAMERA FRONT FAILED', fg='red')
                    self.log.insert(END, '-->CAMERA FRONT FAILED\r\n')
                    self.Test_Flag = False
                else:
                    if golden_test:
                        self.cfg_value_list['PRODUCT'].update({"CAMERA_FRONT": {
                                "GOLDEN_1": result[3][1]
                            }
                        })
                    self.Update_Progress(30, itheme='default', istyle='green')
                    self.log.insert(END, '-->CHECK CAMERA FRONT PASS\r\n\n')
                    tk.messagebox.showinfo('CHECK CAMERA FRONT PASS',
                                              'CHECK CAMERA FRONT PASS !',
                                              icon='warning')
                    self.lbStatus.configure(text='CHECK CAMERA TOP', fg='gold')
                    self.log.insert(END, '-->CHECK CAMERA TOP\r\n')
                    self.log.insert(END, '-->Parallela spec: [-1:1]\r\n')
                    self.log.insert(END, '-->OffSet spec: [22]\r\n')
                    self.bfront = False
                    img_data = self.iTake.Take_Image('TOP')
                    if golden_test:
                        result = self.iFucn.Main(mac[1], 'TOP', 'D:\\CameraVI\\camera0.jpg', 'camera0', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION, golden_test)
                    else:
                        result = self.iFucn.Main(mac[1], 'TOP', 'D:\\CameraVI\\camera0.jpg', 'camera0', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION)
                    self.log.insert(END, '-->Result: '+ str(result[0]) + ',' + str(result[2]) +'\r\n\n')
                    self.Allow_Update = False
                    self.photo = PIL.Image.fromarray(result[1])
                    #self.photo.thumbnail((self.cwidth, self.cheight))
                    self.photo = PIL.ImageTk.PhotoImage(image=self.photo)
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                    if not result[0]:
                        self.lbStatus.configure(text='CAMERA TOP FAILED', fg='red')
                        self.log.insert(END, '-->CAMERA TOP FAILED\r\n')
                        self.Update_Progress(40, itheme='clam', istyle='red')
                        self.Test_Flag = False
                        self.View_Camera_To_Adjust()
                    else:
                        if golden_test:
                            self.cfg_value_list['PRODUCT'].update({"CAMERA_TOP": {
                                    "GOLDEN_1": result[3][1]
                                }
                            })
                            jdata_value_list = json.dumps(self.cfg_value_list)
                            SFC_data_file = open('D:\\CameraVI\\camera.json', 'w')
                            SFC_data_file.write(str(jdata_value_list))
                            SFC_data_file.close()
                        self.Update_Progress(40, itheme='default', istyle='green')
                        self.lbStatus.configure(text='PASS', fg='blue')
                        self.log.insert(END, '-->CAMERA TOP PASS\r\n')
                        self.Test_Flag = False
            else:
                self.Update_Progress(40, itheme='clam', istyle='red')
                self.lbStatus.configure(text='CAMERA MAC FAILED', fg='red')
                self.log.insert(END, '-->CHECK MAC FAILED\r\n')
                self.Test_Flag = False
            print(result)
            if golden_test:
                if messagebox.askokcancel('Golden Test Task',
                                          'Golden đã test xong, hãy rút dây kết nối ?\n Golden test done, please un-plug USB cable ?',
                                          icon='warning'):
                    self.isRun = True

        except Exception as e:
            self.lbStatus.configure(text='Exception', fg='red')
            self.log.insert(END, '-->Exception\r\n')
            self.Update_Progress(40, itheme='clam', istyle='red')
            self.Test_Flag = False
            print(e)

    def Manual(self, golden_test=False):
        try:
            self.Load_CFG()
            self.Test_Flag = True
            self.countTime = 0
            #Thread(target=self.Test_Time()).start()
            self.Update_Progress(10, itheme='default', istyle='green')
            self.log.delete(1.0, END)
            self.log.insert(END, '-->Start test\r\n')
            self.isRun = True
            self.canvas.delete('all')
            self.lbStatus.configure(text='RUNNING', fg='gold')
            self.Update_Progress(20, itheme='default', istyle='green')
            self.lbStatus.configure(text='CHECK CAMERA FRONT', fg='gold')
            self.log.insert(END, '-->CHECK CAMERA FRONT\r\n')
            self.log.insert(END, '-->Parallela spec: [-2:2]\r\n')
            self.log.insert(END, '-->OffSide spec: [22]\r\n')
            self.bfront = True
            result = self.iFucn.Main('Manual', 'FRONT', 'D:\\CameraVI\\OK_camera1.jpg', 'camera1', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION)
            self.log.insert(END, '-->Result: '+ str(result[0]) + ',' + str(result[2]) +'\r\n')
            self.Allow_Update = False
            self.photo = PIL.Image.fromarray(result[1])
            self.photo.thumbnail((self.cwidth, self.cheight))
            self.photo = PIL.ImageTk.PhotoImage(image=self.photo)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            if not result[0]:
                self.Update_Progress(40, itheme='clam', istyle='red')
                self.lbStatus.configure(text='CAMERA FRONT FAILED', fg='red')
                self.log.insert(END, '-->CAMERA FRONT FAILED\r\n')
                self.Test_Flag = False
            else:
                result = [False]
                if tk.messagebox.askquestion('Manual Test',
                                             'Bước tiếp theo đến CAMERA TOP !\r\nNext step to CAMERA TOP!',
                                             icon='warning'):
                    self.Update_Progress(30, itheme='default', istyle='green')
                    self.log.insert(END, '-->CHECK CAMERA FRONT PASS\r\n\n')
                    self.lbStatus.configure(text='CHECK CAMERA TOP', fg='gold')
                    self.log.insert(END, '-->CHECK CAMERA TOP\r\n')
                    self.log.insert(END, '-->Parallela spec: [-1:1]\r\n')
                    self.log.insert(END, '-->OffSide spec: [22]\r\n')
                    self.bfront = False
                    result = self.iFucn.Main('Manual', 'TOP', 'D:\\CameraVI\\OK_camera0.jpg', 'camera0', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION)
                    self.log.insert(END, '-->Result: ' + str(result[0]) + ',' + str(result[2]) + '\r\n\n')
                    self.Allow_Update = False
                    self.photo = PIL.Image.fromarray(result[1])
                    self.photo.thumbnail((self.cwidth, self.cheight))
                    self.photo = PIL.ImageTk.PhotoImage(image=self.photo)
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                if not result[0]:
                    self.lbStatus.configure(text='CAMERA TOP FAILED', fg='red')
                    self.log.insert(END, '-->CAMERA TOP FAILED\r\n')
                    self.Update_Progress(40, itheme='clam', istyle='red')
                    self.Test_Flag = False
                else:
                    self.Update_Progress(40, itheme='default', istyle='green')
                    self.lbStatus.configure(text='PASS', fg='blue')
                    self.log.insert(END, '-->CAMERA TOP PASS\r\n')
                    self.Test_Flag = False
            print(result[0])

        except Exception as e:
            self.lbStatus.configure(text='Exception', fg='red')
            self.log.insert(END, '-->Exception\r\n')
            self.Update_Progress(40, itheme='clam', istyle='red')
            self.Test_Flag = False
            print(e)

    def Main_RealTime(self, rImage):
        try:
            self.Load_CFG()
            self.log.delete(1.0, END)
            if self.bCameraSelect.get() == 1:
                #self.lbStatus.configure(text='CHECK CAMERA FRONT', fg='gold')
                self.log.insert(END, '-->CHECK CAMERA TOP\r\n')
                self.log.insert(END, '-->Parallela spec: [-0.6:0.6]\r\n')
                self.log.insert(END, '-->OffSet spec: [20]\r\n')
                result = self.iFucn.Main('TOP', 'TOP', rImage, 'camera0', self.cfg_PRODUCT, self.cfg_SPECIFICATIONS, self.cfg_OPTION)
                self.log.insert(END, '-->Result: '+ str(result[0]) + ',' + str(result[2]) +'\r\n')
                self.Allow_Update = False
                photo = PIL.Image.fromarray(cv2.cvtColor(result[1], cv2.COLOR_BGR2RGB))
                photo.thumbnail((self.cwidth, self.cheight))
                photo = PIL.ImageTk.PhotoImage(image=photo)
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.photo = photo
                if not result[0]:
                    self.Update_Progress(40, itheme='clam', istyle='red')
                    self.lbStatus.configure(text='CAMERA TOP FAILED', fg='red')
                    self.log.insert(END, '-->CAMERA TOP FAILED\r\n')
                    return False, False
                else:
                    self.log.insert(END, '-->CHECK CAMERA TOP PASS\r\n\n')
                    self.lbStatus.configure(text='CAMERA TOP PASS', fg='blue')
                    self.log.insert(END, '-->CAMERA TOP PASS\r\n')
                    return True, result[1]
            if self.bCameraSelect.get() == 2:
                #self.lbStatus.configure(text='CHECK CAMERA TOP', fg='gold')
                self.log.insert(END, '-->CHECK CAMERA FRONT\r\n')
                self.log.insert(END, '-->Parallela spec: [-0.6:0.6]\r\n')
                self.log.insert(END, '-->OffSet spec: [20]\r\n')
                result = self.iFucn.Main('FRONT', 'FRONT', rImage, 'camera1', self.cfg_PRODUCT,
                                         self.cfg_SPECIFICATIONS, self.cfg_OPTION)
                self.log.insert(END, '-->Result: ' + str(result[0]) + ',' + str(result[2]) + '\r\n')
                self.Allow_Update = False
                photo = PIL.Image.fromarray(cv2.cvtColor(result[1], cv2.COLOR_BGR2RGB))
                photo.thumbnail((self.cwidth, self.cheight))
                photo = PIL.ImageTk.PhotoImage(image=photo)
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.photo = photo
                if not result[0]:
                    self.lbStatus.configure(text='CAMERA FRONT FAILED', fg='red')
                    self.log.insert(END, '-->CAMERA FRONT FAILED\r\n')
                    return False, False
                else:
                    self.log.insert(END, '-->CHECK CAMERA FRONT PASS\r\n\n')
                    self.lbStatus.configure(text='CAMERA FRONT PASS', fg='blue')
                    self.log.insert(END, '-->CAMERA FRONT PASS\r\n')
                    #self.Test_Flag = False
                    return True, result[1]

        except Exception as e:
            self.lbStatus.configure(text='CAMERA FAIL', fg='red')
            self.log.insert(END, '-->CAMERA FAIL\r\n')
            print(e)
            self.Allow_Update = True
            return False, False

    def Test_Time(self):
        if self.countTime <= self.TimeOut and self.Test_Flag:
            self.countTime += 1
            self.lbTime.configure(text='Time: {}'.format(self.countTime))
            self.lbTime.after(1000, self.Test_Time)
        if self.countTime > self.TimeOut:
            #print('open com')
            #self.Open_COM()
            #self.Return_Result(False)
            self.Test_Flag = False
            self.lbStatus.configure(text='Time Out', fg='white', bg='chocolate')
            self.countTime = 0
            #self.Stop_Proc_OnFail()

    def View_Camera_To_Adjust(self):
        self.bViewScreen = True
        self.Close_Camera_To_Adjust()
        self.bViewScreen = True
        Take_DUT.Take_Image_D4.Send_Command('', 'adb shell am start -a android.media.action.IMAGE_CAPTURE')
        if not self.bfront:
            Take_DUT.Take_Image_D4.Send_Command('', 'adb shell input tap 50 50')
        Take_DUT.Take_Image_D4.Send_Command('', 'adb kill-server')
        os.system('taskkill /f /im adb.exe')
        os.startfile('D:/CameraVI/view_camera/scrcpy.exe')

    def Close_Camera_To_Adjust(self):
        self.bViewScreen = False
        Take_DUT.Take_Image_D4.Send_Command('', 'adb kill-server')#adb shell am start -a android.media.action.IMAGE_CAPTURE
        os.system('taskkill /f /im scrcpy.exe')
        os.system('taskkill /f /im adb.exe')

    def Start_Camera(self):
        if self.btnPlay['text'] == 'View_Screen':
            self.btnPlay.configure(fg='white', bg='tomato', text='Close_Screen')
            try:
                Thread(target=self.View_Camera_To_Adjust).start()
                '''if not self.CAMloaded:
                    self.vid = MyVideoCapture(0)
                    self.CAMloaded = True
                print(self.vid)
                self.Allow_Update = True
                self.update()'''
            except Exception as e:
                print(e)
        else:
            self.btnPlay.configure(fg='white', bg='blue', text='View_Screen')
            Thread(target=self.Close_Camera_To_Adjust).start()
            '''self.Allow_Update = False
            self.CAMloaded = False
            self.vid.__del__()
            self.canvas.delete('all')'''

    def update(self):
        #self.vid.vid.set(cv2.CAP_PROP_BRIGHTNESS, self.vBRI.get())
        #self.vid.vid.set(cv2.CAP_PROP_CONTRAST, self.vCONTRA.get())
        if self.Allow_Update:
            self.image_mode = False
            ret, img = self.vid.get_frame()
            iret, iimg = self.vid.get_frame()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.master.after(15, self.update)

    def update_direct(self):
        if self.Allow_Update:
            self.image_mode = False
            try:
                frame = self.fframe
                #print(self.fframe.shape)
                photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                self.photo = photo
                #self.master.after(15, self.update_direct)
            except Exception as e:
                print(e)

    def View_Screen_Direct(self):
        self.Allow_Update = True
        # This will deploy and run server on android device connected to USB
        self.tablet = DannyViewer()
        Thread(target=self.Start_Camera_Product).start()
        while self.bViewScreen and not self._isGoldenTest and not self._isManual_Test:
            frames = self.tablet.next_frames()
            try:
                if not self._brChange:
                    if frames is None:
                        continue
                    else:
                        for frame in frames:
                            #frame = cv2.resize(frame, (740, 480))
                            self.fframe = frame
                        #print(self.bCameraSelect.get())
                        if self.bCameraSelect.get() != 0:
                            #fframe = False
                            fframe = self.Main_RealTime(self.fframe)#('D:\\CameraVI\\OK_camera1.jpg')#
                            #print(fframe)
                            #print(type(fframe))
                            if not fframe[0]:
                                self.fframe = fframe[1]
                                self.Allow_Update = True
                                self.update_direct()
                                #time.sleep(0.03)
                    
                        if self.bCameraSelect.get() == 0:
                            self.update_direct()
                            time.sleep(0.03)
                
            except Exception as e:
                print(e)
                #time.sleep(0.03)
            
                    

    def View_Direct(self):
        Thread(target=self.View_Screen_Direct).start()

    def Start_Camera_Product(self):
        #Take_DUT.Take_Image_D4.Send_Command('', 'adb shell am force-stop -a android.media.action.IMAGE_CAPTURE')
        #time.sleep(1)
        Take_DUT.Take_Image_D4.Send_Command('', 'adb shell am start -a android.media.action.IMAGE_CAPTURE')

    def Change_Camera_Product(self):
        if self.bCameraSelect.get() == 2 and (not self.btop or self.bfront):
            Take_DUT.Take_Image_D4.Send_Command('', 'adb shell input tap 50 50')
            time.sleep(2)
            self.btop = True
            self.bfront = False
        if self.bCameraSelect.get() == 1 and (not self.bfront or self.btop): 
            Take_DUT.Take_Image_D4.Send_Command('', 'adb shell input tap 50 50')           
            self.bfront = True
            self.btop = False
            time.sleep(2)

    def btnSwitch(self):
        if self.bViewScreen:
            Take_DUT.Take_Image_D4.Send_Command('', 'adb shell input tap 50 50')

    def MIT(self):
        Thread(target=self.MIT_Touch).start()

    def MIT_Touch(self):
        w = 800
        h = 489
        for i in range(0, 25):
            self.tablet.swipe(w, h, w, h)
            w -= 33
            h -= 20
            time.sleep(0.1)
            print(i)
        w = 0
        h = 489
        for i in range(0, 25):
            self.tablet.swipe(w, h, w, h)
            w += 33
            h -= 20
            time.sleep(0.1)

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.Screen_Width = GetSystemMetrics(0)
        self.Screen_Height = GetSystemMetrics(1)
        self.cwidth = int(self.Screen_Width / 3 * 2)
        self.cheight = int(self.Screen_Height / 3 * 2)
        self.vid.set(3, self.cwidth)
        self.vid.set(4, self.cheight)
        #self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        #self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #self.vid.set(cv2.CAP_PROP_BRIGHTNESS, 80)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def on_Closing():
    if messagebox.askokcancel('Exit Test Message', 'Bạn có chắc muốn thoát ?\n Are you sure you want to exit ?',
                              icon='warning'):
        ftemp.cleanup()
        root.destroy()
root = Tk()
#root.geometry("400x200+200+200")
#root.attributes('-fullscreen',True)
root.state('zoomed')
root.protocol('WM_DELETE_WINDOW', on_Closing)
#root.iconbitmap('D:/Test_Program/Module/Main/icon.ico')
root.configure(background='lightskyblue')
app = App(master=root)
app.mainloop()

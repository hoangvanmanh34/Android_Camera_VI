import logging
import os
import socket
import struct
import subprocess
import sys
from queue import Queue
from time import sleep

import av
from control import ControlMixin
#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
#https://github.com/hoangvanmanh34
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class DannyViewer(ControlMixin):
    video_socket = None
    control_socket = None
    resolution = None

    video_data_queue = Queue()

    def __init__(self, max_width=0, bitrate=8000000, max_fps=30, adb_path='',
                 ip='127.0.0.1', port=8081):
        """

        :param max_width: frame width that will be broadcast from android server
        :param bitrate:
        :param max_fps: 0 means not max fps.
        :param ip: android server IP
        :param adb_path: path to ADB
        :param port: android server port
        """
        self.ip = ip
        self.port = port

        self.adb_path = adb_path

        assert self.deploy_server(max_width, bitrate, max_fps)

        self.codec = av.codec.CodecContext.create('h264', 'r')
        self.init_server_connection()
        print('+++++')


    def receiver(self):
        """
        Read h264 video data from video socket and put it in Queue.
        This method should work in separate thread since it's blocking.
        """
        try:
            while True:
                raw_h264 = self.video_socket.recv(0x10000)

                if not raw_h264:
                    continue

                self.video_data_queue.put(raw_h264)
        except Exception as e:
            print(e)

    def init_server_connection(self):
        """
        Connect to android server, there will be two sockets, video and control socket.
        This method will set: video_socket, control_socket, resolution variables
        """
        try:
            logger.info("Connecting video socket")
            self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.video_socket.connect((self.ip, self.port))

            dummy_byte = self.video_socket.recv(1)
            if not len(dummy_byte):
                raise ConnectionError("Did not receive Dummy Byte!")

            #deviceName = self.video_socket.recv(64)
            #logger.info("Device Name:", deviceName.decode("utf-8"))
            logger.info("Connecting control socket")
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.connect((self.ip, self.port))

            device_name = self.video_socket.recv(64).decode("utf-8")

            if not len(device_name):
                raise ConnectionError("Did not receive Device Name!")
            logger.info("Device Name: " + device_name)

            res = self.video_socket.recv(4)
            self.resolution = struct.unpack(">HH", res)
            logger.info("Screen resolution: %s", self.resolution)
            self.video_socket.setblocking(False)
        except Exception as e:
            print(e)
            #continue

    def deploy_server(self, max_width=1024, bitrate=8000000, max_fps=0):
        try:
            logger.info("Upload JAR...")
            CREATE_NO_WINDOW = 0x08000000
            server_root = 'D:/CameraVI'#os.path.abspath(os.path.dirname(__file__))
            server_file_path = 'D:/CameraVI/scrcpy-server.jar'
            adb_push = subprocess.Popen('D:/CameraVI/adb/adb push D:/CameraVI/adb/scrcpy-server.jar /sdcard/scrcpy-server.jar',
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
            adb_push_comm = ''.join([x.decode("utf-8") for x in adb_push.communicate() if x is not None])
            print('----------------------')
            print(adb_push_comm)

            if "error" in adb_push_comm:
                logger.critical("Is your device/emulator visible to ADB?")
                raise Exception(adb_push_comm)

            logger.info("Running server...")

            subprocess.Popen('D:/CameraVI/adb/adb root')
            import time
            time.sleep(2)
            '''subprocess.Popen(
                ['D:/CameraVI/adb/', 'adb shell',
                 'CLASSPATH=/sdcard/scrcpy-server.jar',
                 'app_process', '/', 'com.genymobile.scrcpy.Server 1.12.1 {} {} {} true - true true'.format(
                    max_width, bitrate, max_fps)])'''
            subprocess.Popen('D:/CameraVI/adb/adb shell CLASSPATH=/sdcard/scrcpy-server.jar app_process / com.genymobile.scrcpy.Server 1.12.1 800 8000000 30 true - false true', creationflags=CREATE_NO_WINDOW)
            sleep(1)

            logger.info("Forward server port...")
            #subprocess.Popen(['D:/CameraVI/adb/', 'forward', 'tcp:8081', 'localabstract:scrcpy']).wait()
            subprocess.Popen('D:/CameraVI/adb/adb forward tcp:8081 localabstract:scrcpy', creationflags=CREATE_NO_WINDOW).wait()
            sleep(2)
        except Exception as e:#FileNotFoundError:
            raise FileNotFoundError("Couldn't find ADB at path ADB_bin: " + str(self.adb_path))
            print(e)

        return True

    def next_frames(self):
        """
        Get raw h264 video, parse packets, decode each packet to frames and convert
        each frame to numpy array.
        :return:
        """

        packets = []

        try:
            raw_h264 = self.video_socket.recv(0x10000)
            packets = self.codec.parse(raw_h264)

            if not packets:
                return None

        except socket.error as e:
            return None

        if not packets:
            return None

        result_frames = []

        for packet in packets:
            frames = self.codec.decode(packet)
            for frame in frames:
                result_frames.append(frame.to_ndarray(format="bgr24"))

        return result_frames or None

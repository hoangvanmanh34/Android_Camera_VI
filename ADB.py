from subprocess import Popen, PIPE, STDOUT
import time
import Watchdog
#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
#https://github.com/hoangvanmanh34
def Send_ADB(cmd, expect_dic = {}, dtime1=0, dtime2=0, itimeout=10,Error_Code='No_Error_Code', unexpect_line='', sendFixture=''):
    adb_path = "D:\\CameraVI\\adb"
    ADB_RES_1 = []
    ADB_RES_1.append(cmd)
    expect_line = ""
    Error_Code = Error_Code
    print(cmd)
    bresult = False
    check_expect = False
    res = expect_dic.copy()
    print(len(res))
    CREATE_NO_WINDOW = 0x08000000
    if len(res) <= 0:
        bresult = True
    if len(res) > 0 :
        check_expect = True
    with Popen(adb_path + "\\" + cmd, stdout=PIPE, stderr=STDOUT,
               universal_newlines=True, creationflags=CREATE_NO_WINDOW) as process:  # text mode
        # kill process in timeout seconds unless the timer is restarted
        time.sleep(dtime1)
        watchdog = Watchdog.WatchdogTimer(itimeout, callback=process.kill, daemon=True)
        watchdog.start()
        print('-Expect:' + str(res))
        '''if len(res) <= 0:
            print('OKOKOKOKOK')
            return True'''
        for line in process.stdout:
            # don't invoke the watcthdog callback if do_something() takes too long
            with watchdog.blocked:
                if len(line.strip()) > 0:
                    print(line)
                    ADB_RES_1.append(line)
                #res = {}
                for re in expect_dic.keys():
                    if re in res:
                        if (line).find(res[re]) >= 0:
                            if unexpect_line != '':
                                if line.find(unexpect_line) < 0:
                                    print('detect:' + str(res[re]))
                                    del res[re]
                            else:
                                print('detect:' + str(res[re]))
                                del res[re]
                if len(res) <= 0 and check_expect:
                    process.kill()
                    expect_line = line
                    bresult = True
                    print('OKOKOKOKOK')
                    #break
                if (line).find('error: device') >= 0:
                    Error_Code = "DEVICE"
                    bresult = False
                    break

                '''if (line.find(res)) >= 0:  # some criterium is not satisfied
                    process.kill()
                    break'''
                watchdog.restart()  # restart timer just before reading the next line
        time.sleep(dtime2)
        watchdog.cancel()
    return bresult, ADB_RES_1, expect_line, Error_Code

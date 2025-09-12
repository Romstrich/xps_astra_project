'''
    ==============================Модуль системной информации============
    ---------------------------------------------------------------------
    Версия 0.1 для xps_astra 0.5

        Модуль получения информации по системным ресурсам (железу), а
    также севедений о ядре системы и пользователях компьютера.

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''

from module_messenger import My_logger
from module_permissions import My_Permissions
from chardet import detect
import os

import subprocess

VERSION = '0.1'
logger = My_logger


class My_System():
    def __init__(self, permis=False):
        self.priveleges = permis
        if not self.priveleges:
            self.priveleges = My_Permissions()
        self.lshwInstalled = self.checkhLSHW()

    def updateInfo(self):
        '''
        Запускает информационные функции
        :return:
        '''

    def manufacture(self):
        '''
        Производитель
        :return:
        '''
        counter=0
        manuf=[]
        if self.priveleges.sudoCanRun:
            proc = os.popen('sudo lshw')
        for i in proc:
            manuf.append(i)
            counter+=1
            if counter==9:
                break
        return manuf


    def processor(self):
        '''
        процессор
        :return:
        '''
        processor=[]
        if self.priveleges.sudoCanRun:
            proc = os.popen('sudo lshw -class cpu')
            for i in proc:
                processor.append(i)
        return processor[1:-1]

    def memory(self):
        mem = []
        if self.priveleges.sudoCanRun:
            proc = os.popen('sudo lshw -short -class memory')  # .read()
            for i in proc:
                if 'System memory' in i:
                    mem = i.split()
                    break
        return mem[-3]

    def showGPU(self):
        GPU = []
        if self.priveleges.sudoCanRun:
            proc = os.popen('sudo lshw -short -class display')
            for i in proc:
                if 'display' in i:
                    GPU.append(i.split('display')[-1])
        return GPU

    def netInterface(self):
        net = []
        if self.priveleges.sudoCanRun:
            proc = os.popen('sudo lshw -short -class network')  # .read()
            for i in proc:
                if 'network' in i:
                    net.append(i.split('network')[-1])
        return net

    def diskInfo(self):
        disk = []
        if self.priveleges.sudoCanRun:
            proc = os.popen('sudo lshw -class disk')
            for i in proc:
                print(i.split())

    def cernelAndUsers(self):
        resDict={}
        if self.priveleges.sudoCanRun:
            os.popen('sudo uname -r')
            os.popen('sudo uname -v')
            os.popen('sudo uname -m')
            os.popen("sudo awk -F: '$3 >= 1000 {print $1}' /etc/passwd  | grep -v nobody")

    def checkhLSHW(self):
        '''наличие пакета для диагностики
        оборудования
        !!!Забери вывод
        '''
        cmd = 'dpkg --status lshw'.split()  # | grep "ok installed"'#.split(' ')
        # check = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)#.read()#, stdout=subprocess.PIPE)
        check = subprocess.run(cmd, stdout=subprocess.PIPE)
        try:
            resault = check.stdout.decode(detect(check.stdout)['encoding']).split()
            # print(resault)
        except BaseException as error:
            logger.error(f'Ошибка {error}')
            return False
        else:
            # print('else except')
            if 'Status:' in resault:
                if 'ok' in resault:
                    # print(resault)
                    return True
            else:
                # print(resault)
                return False

    def cliOutput(self):
        if self.priveleges.sudoCanRun:
            # print(self.manufacture())
            # print(self.processor())
            # print(self.memory())
            # print(self.showGPU())
            # print(self.netInterface())
            print(self.diskInfo())
            # self.cernelAndUsers()
        else:
            logger.warning('Нет прав')


if __name__ == "__main__":
    logger.info(f'module_sysinfo was loading like programm.\nVersion: {VERSION}')
    inspector = My_System()
    # print(inspector.lshwInstalled)
    inspector.cliOutput()
    logger.info('штатное завершение')
else:
    logger.info(f'module_permissions was loading like module.\nVersion: {VERSION}')

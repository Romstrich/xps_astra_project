'''
    ==============================Модуль обработки прав==================
    ---------------------------------------------------------------------
        Модуль выявления пользователя, получения прав и выполнения команд
        - Определяет владельца сессии
        - Определяет права sudo
        - Находит рабочий стол пользователя
        - Запрашивает пароль администратора для выполнения команды su
    ---------------------------------------------------------------------
'''

import os
import subprocess
from pwinput import pwinput
from chardet import detect
from chardet import detect

from module_messenger import Messenger

# TEST_SUDO_COMMAND="if sudo -S -p '' echo -n < /dev/null 2> /dev/null ; then echo 'enabled.' ; else echo 'disabled' ; fi"
class My_Permissions():
    '''
    user - Владелец сессии
    sudoCanRun - возможность выполнить команду su
    '''
    def __init__(self):
        self.user=self.detectUserName() #пользователь сессии
        self.sudoAccess = self.checkSudoAccess()  # причастность к административным группам
        self.sudoCanRun = self.checkSudoRun()  # Текущее право выполнять команды sudo
        self.sudoUser=self.detectSudoUser() #пользователь терминала



    def detectUserName(self):
        '''
        Здесь будем разбираться кто наш пользователь
        !!!Включить цикл try-except
        return:
        '''
        usrDetect=subprocess.run(['logname'],stdout=subprocess.PIPE)
        user=usrDetect.stdout.decode(detect(usrDetect.stdout)['encoding'])
        return user.strip()

    def detectSudoUser(self):
        '''
        Должно возвращать True , если sudo или root или bash
        :return:
        '''
        sudoDetect = subprocess.run(['whoami'],stdout=subprocess.PIPE)
        sudoUser = sudoDetect.stdout.decode(detect(sudoDetect.stdout)['encoding'])
        return sudoUser.strip()

    def checkSudoRun(self,p=False):
        '''Проверка на выполнение SUDO
        проверочная команда :ls /root'''
        if self.sudoAccess:
            sudoTest = subprocess.run(['ls','/root'], stdout=subprocess.PIPE)
        else:
            pass
            # raise BaseException
        try:
            sudoResult = sudoTest.stdout.decode(detect(sudoTest.stdout)['encoding'])#Разобраться со случаем, где ошибка!!!!
        except BaseException as error:
            print('Команду от sudo мы не выполним')
            return False
        else:
            print('------------------Всё ОК - ПОЕХАЛИ!------------------')
            return True

    def checkSudoAccess(self):
        '''Проверка доступа к командам sudo
        Просто узнаём, есть ли пользователь в группе sudo
        '''
        testCommand='groups'
        sudoDetect = subprocess.run(testCommand, stdout=subprocess.PIPE)
        result = sudoDetect.stdout.decode(detect(sudoDetect.stdout)['encoding']).split()
        #если мы root либо в гпуппе sudo то можем получить доступ
        if 'sudo' in result:
            return True
        elif 'root' in result:
            return True
        else:
            return False
        #print(result)

    def getSudoAccess(self, passwd=False):
        '''
        Получим пароль(если он нам нужен
        :return:
        '''
        if passwd:
            psw=passwd
        else:
            psw=pwinput('Введите пароль администратора: ')
        if self.checkSudoRun(psw):
            print('пароль принят')
        else:
            print('пароль не принят')
            psw=False
        return psw


    def runSudoCommand(self,command):
        '''
        выполнить команду с sudo правами.
        :param command:
        :return:
        '''
        #сначала проверим, есть ли у нас прямая возможность выполнить,
        #затем, если её нет, можно ли получить доступ
        #тогда либо отказываем, либо запрашиваем пароль
        if self.permission:
            print('Вполним команду SUDO')
        elif self.sudoAccess:
            print('Проверим пароль, если пароля нет, либо он не рабочий - сообщим')
        else:
            print('КОМАНДА НЕ ВЫПОЛНЕНА - РАЗБИРАЙСЯ')

if __name__ == '__main__':
    print(__doc__)
    my_perm=My_Permissions()
    print(f'USER_NAME: {my_perm.user}')
    print(f'SUDO_USER: {my_perm.sudoUser}')
    print(f'USER_HAVE_SUDO_ATTRIBUTES: {my_perm.sudoAccess}')
    print(f'USER_CAN_SUDO_COMMAND: {my_perm.sudoAccess}')

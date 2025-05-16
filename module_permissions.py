'''
    ==============================Модуль обработки прав==================
    ---------------------------------------------------------------------
    Версия 0.2 для xps_astra 0.4

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

VERSION='0.2'

# TEST_SUDO_COMMAND="if sudo -S -p '' echo -n < /dev/null 2> /dev/null ; then echo 'enabled.' ; else echo 'disabled' ; fi"
class My_Permissions():
    '''
    user - Владелец сессии
    terOwner - Владелец терминала (текущей команды)
    sudoAccess - Доступность su по группам
    sudoCanRun - возможность выполнить команду su ( True - можем
                                                    False - не можем
                                                    password - с паролем)
    '''
    def __init__(self):
        self.user=self.detectUserName() #пользователь сессии
        self.termOwner = self.detectSudoUser()  # пользователь терминала
        self.sudoAccess = self.checkSudoAccess()  # причастность к административным группам
        self.sudoCanRun = self.checkSudoRun()  # Текущее право выполнять команды sudo




    def detectUserName(self):
        '''
        Здесь будем разбираться кто наш пользователь
        !!!Включить цикл try-except
        return: Имя пользователя сессии
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
        elif 'astra-admin' in result:
            return True
        elif 'astra-admin' in result:
            return True
        else:
            return False
        #print(result)

    def checkSudoRun(self,password=False):
        '''Проверка на выполнение SUDO
        проверочная команда :ls /root
        !!! параметр -А !!!
        даёт в конкретном случае проверку выполнения на ходу:
            а) либо владелец текущего запроса root
            б) user    ALL=NOPASSWD:ALL в /etc/sudoers
        echo password | sudo -S command
        '''

        if password:
            print('Проверка пароля ')#,password)
            sudoTest = subprocess.run(['sudo', '-S', 'ls', '/root'], input=password.encode(),stdout=subprocess.PIPE)#, stdout=subprocess.PIPE)
            #sudoTest = subprocess.run(['sudo', '-S','<<<', str(password),'ls', '/root'], stdin=subprocess.PIPE,stdout=subprocess.PIPE)#, stdout=subprocess.PIPE)
        else:
            # if self.termOwner == 'root':
            if self.sudoAccess:
                print('permissions проверка при инициализации')
                sudoTest = subprocess.run(['sudo','-A','ls','/root'], stdout=subprocess.PIPE)
            #elif not self.sudoAccess:
            else:
                print('Внимание! Пользователь не состоит в группах администрирования!')
                return False
        try:
            sudoResult = sudoTest.stdout.decode(detect(sudoTest.stdout)['encoding'])#Разобраться со случаем, где ошибка!!!!
        except BaseException as error:
            print('Команду от sudo мы не выполним')
            if password:
                print('!!!Пароль не принят!!!')
            return False
        else:
            print('------------------Всё ОК - ПОЕХАЛИ!------------------')
            if password:
                print('--------------------Пароль принят--------------------')
                self.sudoCanRun='password'
            return True

    def getSudoAccess(self, passwd=False):
        '''
        Получим пароль(если он нам нужен)
        Если пароль передан - проверяем,
        Если нет - получаем
        После проверки возвращаем пароль, если рабочий,
        ложь - если нет.
        :return:
        '''
        if passwd:
            psw=passwd
        else:
            psw=pwinput('Введите пароль администратора: \n')
        if self.checkSudoRun(psw):
            print('пароль принят')
            return psw
        else:
            print('пароль не принят')
            return False


    def runSudoCommand(self,command, password = False):
        '''
        выполнить команду с sudo правами.
        :param command:
        :return:
        '''
        #сначала проверим, есть ли у нас прямая возможность выполнить,
        #затем, если её нет, можно ли получить доступ
        #тогда либо отказываем, либо запрашиваем пароль
        # if self.permission:
        #     print('Вполним команду SUDO')
        # elif self.sudoAccess:
        #     print('Проверим пароль, если пароля нет, либо он не рабочий - сообщим')
        # else:
        #     print('КОМАНДА НЕ ВЫПОЛНЕНА - РАЗБИРАЙСЯ')
        shString = []


        if self.sudoCanRun == True:
            shString=['sudo']
        else:
            #Вводим пароль и проверяем
            password=self.getSudoAccess(password)
            if password:
                print(f'Выполняю команду {command}')
                shString=['sudo']
            else:
                print('Команда выполнена не будет: не верный пароль')
                return False

        for i in command.split(' '):
            shString.append(i)
        print(shString)

        try:
            print('Запуск команды')
            #shTest = subprocess.run(shString, capture_output=True, text=True)#, shell=True)# ,stdout=subprocess.PIPE)#capture_output=True,
            os.system('sudo '+command) #тестовый вариант)
            #вариант команды:vipnetclient stop; sudo yes | sudo vipnetclient deletekeys - работает удовлетворительно

        except BaseException as error:
            print(f'Возникла ошибка {error}')
            return False
        else:
            print('Проверь выполнение команды')
            # Возвращаем
            #return shTest.stdout.decode(detect(shTest.stdout)['encoding'])



    def permissionRezume(self):
        print(f'USER_NAME: {self.user}')
        print(f'TERM_OWNER: {self.termOwner}')
        print(f'USER_HAVE_SUDO_ATTRIBUTES: {self.sudoAccess}')
        print(f'USER_CAN_RUN_SUDO_COMMAND: {self.sudoCanRun}')


if __name__ == '__main__':
    print(__doc__)
    my_perm=My_Permissions()
    my_perm.permissionRezume()
    # my_perm.checkSudoRun('1')
    # my_perm.permissionRezume()
    # if my_perm.sudoCanRun:
    com=input('Введите команду для выполнения в режиме su\n')
    my_perm.runSudoCommand(com)
    #my_perm.runSudoCommand('ls \\n| grep .py')
        # my_perm.checkSudoRun('1')
else:
    print('module_permissions was loading like module')
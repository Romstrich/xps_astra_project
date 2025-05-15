'''
    ==============================Модуль работы с VipNet=================

        Поиск/проверка dst - файла
        Проверка установленного VipNet,
        Проверка наличия установленного ключа для системы/пользователей
        Удаление текущего ключа у пользователей

        Установка нового ключа в систему


    Класс работы с dst-файлами и ViPNet
    My_ViPNet
    Свойства класса:
        self.ViPNetInfo = False
        self.error = []
        self.privileges = None
        self.filePath = False
    Методы класса:

'''

import os.path
import subprocess
from pathlib import Path


class My_ViPNet():
    def __init__(self, file_name=''):
        self.installed=False
        self.ViPNetInfo = False
        self.error = []
        self.privileges = False
        self.filePath = False

        self.installed=self.checkViPNet()

    def checkViPNet(self):
        '''
        В этой функции определяем наличие ViPNet-клиента
        vipnetclient --version
        :return:
        '''
        try:
            # command2 = ['vipnetclient', '--verson']
            ViPNetInfo2 = os.popen('vipnetclient --version').read()
        # subprocess.run(command2, stdin=comm1.stdout)
            #comm2 = subprocess.run(command2, stdout=subprocess.PIPE)
            #ViPNetInfo2 = comm2.stdout.decode('utf-8').split()
        # print(type(ViPNetInfo2))
            #self.show_message(f'ВЕРСИЯ: {ViPNetInfo2.split()[-1]}')
            return ViPNetInfo2.split()[-1]
        except BaseException as e:
            self.error.append(e)
            self.show_message(f'Ошибка {e}')
            return False
        else:
            pass


        # for i in ViPNetInfo2:
        #     print(str(i))

    # def checkPrivileges(self):
    #     '''
    #         Функция, которая проверяет su
    #             !!!ACHTUNG!!!
    #             Не даст нашего пользователя если мы были запущены
    #                 ->sudo bash
    #                 ->sudo <exe_name>
    #             будет пара (root,root)
    #         :return: (root,имя пользователя) - привилегии
    #                  (имя пользователя)      - привилегий нет.
    #         '''
    #     # узнаем от чьего имени
    #     print(os.get_exec_path())
    #     try:
    #         user = os.environ['USER']
    #     except KeyError:
    #         print('Что-то не так с пользователем')
    #     # print(os.getuid())
    #     if user == 'root':
    #         print('Выполняемся с привилегиями')
    #         try:
    #             su = os.environ['SUDO_USER']
    #         except KeyError:
    #             # sudo не выполнялось - мы root
    #             print('Выполнение в среде root')
    #             return (user, user)
    #         else:
    #             # sudo выполнялось - мы не root
    #             print('Выполнение в среде c повышением привилегий')
    #             return (user, su)
    #
    #     else:
    #         print('Привилегий при выполнении нет')
    #         return (user,)
    #     # print(os.environ['SUDO_USER'])

    def ViPNetInfo(self):
        pass
    def installKey(self):
        pass

    def deleteKey(self):
        try:
            command1=['sudo','-S','vipnetclient', 'stop']
            command2 = ['sudo','-S', 'vipnetclient', 'deletekeys']
            com1 = subprocess.call(command1)#, stdout=subprocess.PIPE, encoding='utf-8')
            # subprocess.run(com1,stdin=com1.stdout)
            # com2 = subprocess.Popen(command2)#, stdout=subprocess.PIPE, encoding='utf-8')
            subprocess.call(command2)# stdin=com2.stdout)
            print('Ключи удалены из системы')
        except BaseException as e:
            print(e)
        else:
            pass

    def ViPNetStart(self):
        pass

    def ViPNetStop(self):
        pass

    def ViPNetGUI(self):
        pass

    def show_message(self, text='', gui=False):
        '''
        Функция вывода сообщений
        :param gui:     передача сообщения в графическую оболочку (gui- объект передачи)
        :param text:
        :param error:
        :return:
        '''
        message = text
        if gui:
            if gui.statusbar:
                try:
                    gui.statusbar.config(text=message)
                except BaseException as error:
                    print(f'Ошибка графического интефейса: {error}')
                else:
                    pass
        else:
            print(message)


if __name__ == '__main__':
    print('Тестовая работа с классом MyViPNet')
    print(__doc__)
    vpn = My_ViPNet()
    # vpn.deleteKey()
    # vpn.checkPrivileges()

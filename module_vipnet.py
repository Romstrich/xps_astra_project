'''
    ==============================Модуль работы с VipNet=================
    ---------------------------------------------------------------------
    Версия 0.1 для xps_astra 0.4

        Модуль работы с ViPNet
        - Определяет установленный клиент
        - Определяет установленный ключ (!системный!)

    ---------------------------------------------------------------------
'''

import os.path
import subprocess
from pathlib import Path

from module_permissions import My_Permissions

VERSION = '0.1'


class My_ViPNet():
    '''
    installed   установле ли випнет
    priveliges  возможность пользоваться su
    sysKeyInfo  информация об установленном ключе
    '''

    def __init__(self):
        self.installed = self.checkViPNet()
        self.privileges = My_Permissions()
        if self.installed:
            self.sysKeyInfo = self.getSysKeyInfo()
        else:
            self.sysKeyInfo = False
        # self.ViPNetInfo = False
        # self.error = []

    def checkViPNet(self):
        '''
        В этой функции определяем наличие ViPNet-клиента
        vipnetclient --version
        :return:
        !!!!!!!!ПРОСТО ПОЛУЧИ ЗДЕСЬ ВЕРСИЮ И НИЧЕГО НЕ ТРОГАЙ!!!!!!!
        '''
        try:
            # command2 = ['vipnetclient', '--verson']
            ViPNetInfo2 = os.popen('vipnetclient --version').read()
            # subprocess.run(command2, stdin=comm1.stdout)
            # comm2 = subprocess.run(command2, stdout=subprocess.PIPE)
            # ViPNetInfo2 = comm2.stdout.decode('utf-8').split()
            # print(type(ViPNetInfo2))
            # self.show_message(f'ВЕРСИЯ: {ViPNetInfo2.split()[-1]}')
            return ViPNetInfo2.split()[-1]
        except BaseException as e:
            # self.error.append(e)
            print('Возможно, ViPNet не установлен в системе.')
            print(f'Ошибка: {e}')
            return False
        else:
            return False

    def getSysKeyInfo(self):
        '''
        VPN status              STATUS          состояние Включён/выключен
        Host name               NAME            Имя ключа
        Host ID                 ID
        Active coordinator      COORDINATOR     Имя координатора
        ViPNet network name     NETNAME         Имя сети
        ViPNet network ID       NETID           Идентификатор сети
        Keys                    KEYSTATUS       Состояние ключа
        User - должен быть root USER            Доп проверка для системного пользователя
        Autostart               AUTOSTART       Автозапуск Включён/выключен
        :return:
        '''
        try:
            if self.installed:
                if self.privileges.sudoCanRun:
                    statusDict = {}  # словарь статуса ключа
                    resultDict = {}  # словарь для возврата
                    print('Попробуем узнать информацию о системном ключе')
                    sysKey = os.popen('sudo vipnetclient info').read()
                    for line in sysKey.splitlines():
                        # Преобразовать в словарь по первым словам
                        if len(line):
                            if line.split()[0] == 'Host':
                                statusDict.update({' '.join(line.split()[0:2]): line.split()[2:]})
                            elif line.split()[0] == 'ViPNet':
                                statusDict.update({' '.join(line.split()[0:3]): line.split()[3:]})
                            elif 'coordinator' in line.split():
                                statusDict.update({'Coordinator': line.split()[2:]})
                            else:
                                statusDict.update({line.split()[0]: line.split()[1:]})
                        if 'VPN' in line.split():
                            # Включён/выключен:
                            if line.split()[-1] == 'enabled':
                                print('Сейчас ViPNet включён')
                            else:
                                print('Сейчас ViPNet выключён')
                    # print(statusDict)
                    # Заодно заполним свой словарь
                    for key, value in statusDict.items():
                        # print(f'-----{key}\t\t\t{value}')
                        if key == 'VPN':
                            if value[-1] == 'enabled':
                                resultDict.update({'STATUS': True})
                            else:
                                resultDict.update({'STATUS': False})
                        if key == 'Host name':
                            resultDict.update({'NAME': value})
                        if key == 'Host ID':
                            resultDict.update({'ID': value})
                        if key == 'Coordinator':
                            resultDict.update({'COORDINATOR': value})
                        if key == 'ViPNet network name':
                            resultDict.update({'NETNAME': value})
                        if key == 'ViPNet network ID':
                            resultDict.update({'NETID': value})
                        if key == 'Keys':
                            if 'failed' in value:
                                resultDict.update({'KEYSTATUS': False})
                            elif 'verified' in value:
                                resultDict.update({'KEYSTATUS': True})
                        if key == 'User':
                            resultDict.update({'USER': value})
                        if key == 'Autostart':
                            if 'enabled' in value:
                                resultDict.update({'AUTOSTART': True})
                            else:
                                resultDict.update({'AUTOSTART': False})

                    # print('===========РЕЗУЛЬТИРУЮЩИЙ СЛОВАРЬ=============')
                    # for key, value in resultDict.items():
                    #     print(f'-----{key}\t\t\t{value}')
                    return resultDict
                else:
                    print('Привелегии не позволяют узнать информацию о системном ключе')
                    return False
            else:
                print('Возвращаю FALSE')
                return False
        except BaseException as error:
            print(f'При определении установленного ключа возникла ошибка:\n\t{error}')
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
            command1 = ['sudo', '-S', 'vipnetclient', 'stop']
            command2 = ['sudo', '-S', 'vipnetclient', 'deletekeys']
            com1 = subprocess.call(command1)  # , stdout=subprocess.PIPE, encoding='utf-8')
            # subprocess.run(com1,stdin=com1.stdout)
            # com2 = subprocess.Popen(command2)#, stdout=subprocess.PIPE, encoding='utf-8')
            subprocess.call(command2)  # stdin=com2.stdout)
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
    vpn.privileges.permissionRezume()
    print(f'Результат проверки установленной версии ViPNet: {vpn.installed}')
    # vpn.privileges.permissionRezume()
    # vpn.deleteKey()
    # vpn.checkPrivileges()
else:
    print('module_vipnet was loading like module')

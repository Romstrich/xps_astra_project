'''
    ==============================Модуль работы с VipNet=================
    ---------------------------------------------------------------------
    Версия 0.2 для xps_astra 0.5

        Модуль работы с ViPNet
        - Определяет установленный клиент
        - Определяет установленный ключ (!системный!)
        - Операции с ключём (системным)
        - Операции с випнет-клиентом

        0.1.1

        - добавлена функция обновления состояния
        *- атрибут ошибки клиента (неправильно установлен, не может
            ответить)
        - атрибут наличия ключа

        0.2
        - Реализация логирования
        - Получение прав в качестве параметра
        *- вынесение функционала из CLI_module

    *не реализовано/не доработано

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''

import os.path
from os import system
import subprocess
from pathlib import Path

from module_permissions import My_Permissions
from module_xps import ReaderXPS
from module_messenger import My_logger

VERSION = '0.2'
HELP = __doc__
logger=My_logger

class My_ViPNet():
    '''
    Класс работы с випнет
    Атрибуты
        installed   установле ли випнет
        priveliges  возможность пользоваться su
        sysKeyInfo  информация об установленном ключе
    Методы:

    '''

    def __init__(self,permis=False):
        self.error = False
        self.installed = self.checkViPNet()
        self.privileges=permis
        if not self.privileges:
            self.privileges = My_Permissions()
        if self.installed:
            self.sysKeyInfo = self.getSysKeyInfo()
        else:
            self.sysKeyInfo = False
        self.installedKey = False
        if self.sysKeyInfo:
            try:
                #если клиент работает:
                self.installedKey = self.sysKeyInfo['KEYSTATUS']
            except BaseException as error:
                print('No_key')
            else:
                pass
        self.error=None

        # print(f'KEYSTATUS:\t {self.sysKeyInfo["KEYSTATUS"]}')
        # print(f'installedKey:\t {self.installedKey}')

        # self.ViPNetInfo = False
        # self.error = []
    def refresh(self):
        '''
        Обновление состояния
        :return:
        '''
        logger.info('Обновление информации ViPNet...')
        self.error=False
        self.installed = self.checkViPNet()
        if self.installed:
            self.sysKeyInfo = self.getSysKeyInfo()
        else:
            self.sysKeyInfo = False
        self.installedKey=False
        if self.sysKeyInfo:
            try:
                self.installedKey= self.sysKeyInfo['KEYSTATUS']
            except BaseException as error:
                logger.warning('No_key')
            else:
                pass
        logger.info('Обновление информации ViPNet завершено.')

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
            logger.error('Возможно, ViPNet не установлен в системе.')
            logger.error(f'Ошибка: {e}')
            self.error=True
            return False
        else:
            return False

    def getSysKeyInfo(self):
        '''
        Сбор необходимой информации о ключе:
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
                    logger.info('Попробуем узнать информацию о системном ключе')
                    sysKey = os.popen('sudo vipnetclient info').read()
                    # print(f'Выявлено: {sysKey}')
                    if self.installed:
                        if len(sysKey)==0:
                            logger.info('!Возможно, випнет  установлен, но не настроен/настроен с ошибкой.')
                            logger.info('Возможное решение: переустановка через dpkg.')
                            self.error=True
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
                                logger.info('Сейчас ViPNet включен')
                            else:
                                logger.info('Сейчас ViPNet выключен')
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
                                if 'not' in value:
                                    resultDict.update({'KEYSTATUS': False})
                                else:
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
                    logger.error('Привелегии не позволяют узнать информацию о системном ключе')
                    return False
            else:
                print('Возвращаю FALSE')
                return False
        except BaseException as error:
            print(f'При определении установленного ключа возникла ошибка:\n\t{error}')
            self.error=True
            return False
        else:
            pass

    def ViPNetInfo(self):
        pass

    def findFirstInDir(self,dirname):
        '''
        найдём первый попавшийся дстешник в каталоге
        '''
        if os.path.isdir(dirname):
            print(f'Каталог {dirname} существует')

            out = []
            if dirname:
                logger.info(f'Получим список файлов с расширением dst.\t{dirname}')
                filelist = os.listdir(dirname)
                # print(filelist)
                for i in filelist:
                    if Path(i).suffix == '.dst':
                        # print(os.path.join(self.dirName,i))
                        out.append(os.path.join(dirname, i))
                if len(out):
                    logger.info(f'Файлы dst обнаружены: {out[0]}')
                    return out[0]
                else:
                    logger.warning('Файлы dst не обнаружены')
                    return False

            else:
                logger.warning(f'Не могу получить список файлов.\n\tСостояние каталога: {self.dirName}')
                return False
        else:
            logger.error(f'Каталог {dirname} по указанному пути не существует.\n\tПроверьте путь.')
            # self.error.append('file_not_exists')
            return False

    def installKey(self,dstFile=False,xpsFile=False):
        '''
        Установка ключа
        :return:
        '''
        command='sudo vipnetclient installkeys '
        if dstFile:
            command+=dstFile #+ ' --psw rdfveiecn,ek'
            if xpsFile:
                #print(ReaderXPS(xpsFile).getPasswd())
                #xps=ReaderXPS(xpsFile)

                command+=' --psw '+ReaderXPS(xpsFile).getPasswd()
            else:
                password=input('Отсутствует файл пароля на рабочем столе.\n\tВВЕДИТЕ ПАРОЛЬ:')
                command += ' --psw ' + password
            #print(command)

            system(command)
        else:
            print('Нет файла ключа на входе.')
            return False

    def deleteKey(self):
        try:
            if self.ViPNetStop():
                # command2 = ['sudo', '-S', 'vipnetclient', 'deletekeys']
                # command3 = ['yes','|','sudo', 'vipnetclient', 'deletekeys']
                system('yes | sudo vipnetclient deletekeys ')
            #com1 = subprocess.call(command1)  # , stdout=subprocess.PIPE, encoding='utf-8')
            # subprocess.run(com1,stdin=com1.stdout)
            # com2 = subprocess.Popen(command2)#, stdout=subprocess.PIPE, encoding='utf-8')
                #subprocess.call(command3)  # stdin=com2.stdout)

        except BaseException as e:
            logger.error(f'При удалении установленного ключа возникла ошибка:\n\t{e}')
            return False
        else:
            logger.info('Ключи удалены из системы')
            return True

    def ViPNetStart(self):
        '''
        Запуск клиента
        :return:
        '''
        if self.privileges.sudoCanRun:
            try:
                command1 = ['sudo', '-S', 'vipnetclient', 'start']
                subprocess.call(command1)
            except BaseException as error:
                logger.error(f'При запуске ViPNet возникла ошибка:\n\t{error}')
                return False
            else:
                logger.info('Клиент запущен')
                return True
        else:
            logger.warning('Привелегии не позволяют запустить клиент.')
            return False

    def ViPNetStop(self):
        '''
        Останов клиента
        :return:
        '''
        if self.privileges.sudoCanRun:
            try:
                command1 = ['sudo', '-S', 'vipnetclient', 'stop']
                subprocess.call(command1)
            except BaseException as error:
                logger.error(f'При остановке ViPNet возникла ошибка:\n\t{error}')
                return False
            else:
                logger.info('Клиент остановлен')
                return True
        else:
            logger.warning('Привелегии не позволяют остановить клиент.')
            return False


    def ViPNetGUI(self):
        pass

    def printKeyInfo(self):
        try:
            print(f"{self.sysKeyInfo['STATUS']}")
            print(f"{self.sysKeyInfo['NAME']}" )
            print(f"{self.sysKeyInfo['ID']}  ")
            print(f"{self.sysKeyInfo['COORDINATOR']}")
            print(f"{self.sysKeyInfo['NETNAME']    }")
            print(f"{self.sysKeyInfo['NETID']      }")
            print(f"{self.sysKeyInfo['KEYSTATUS']  }")
            print(f"{self.sysKeyInfo['USER']       }")
            print(f"{self.sysKeyInfo['AUTOSTART']  }")
        except BaseException as error:
            print(f'При выведении информации установленного ключа возникла ошибка:\n\t{error}')
            print(f'Состояние installedKey:\t{self.installedKey}')
            return False
        else:
            return True

    def printKeyInfoWide(self):
        try:
            if self.installedKey:
                print(f"Состояние клиента (вкл/выкл):\t{self.sysKeyInfo['STATUS']}")
                print(f"Имя ключа:\t {' '.join(self.sysKeyInfo['NAME'])}" )
                print(f"Идентифткатор ключа:\t{''.join(self.sysKeyInfo['ID'])}  ")
                print(f"Координатор:\t{' '.join(self.sysKeyInfo['COORDINATOR'])}")
                print(f"Имя сегмента сети:\t{' '.join(self.sysKeyInfo['NETNAME'])    }")
                print(f"Идентификатор сети:\t{' '.join(self.sysKeyInfo['NETID'])      }")
                print(f"Пользователь ключа:\t{''.join(self.sysKeyInfo['USER'])       }")
                print(f"Запуск с системой (вкл/выкл):\t{self.sysKeyInfo['AUTOSTART']  }")
            else:
                print('Ключ не установлен')
        except BaseException as error:
            print(f'При выведении информации установленного ключа возникла ошибка:\n\t{error}')
            print(f'Состояние installedKey:\t{self.installedKey}')
            return False
        else:
            return True
    # def show_message(self, text='', gui=False):
    #     '''
    #     Функция вывода сообщений
    #     :param gui:     передача сообщения в графическую оболочку (gui- объект передачи)
    #     :param text:
    #     :param error:
    #     :return:
    #     '''
    #     message = text
    #     if gui:
    #         if gui.statusbar:
    #             try:
    #                 gui.statusbar.config(text=message)
    #             except BaseException as error:
    #                 print(f'Ошибка графического интефейса: {error}')
    #             else:
    #                 pass
    #     else:
    #         print(message)


if __name__ == '__main__':
    logger.info(f'Тестовая работа с классом MyViPNet.\nVersion: {VERSION}')
    print(__doc__)
    vpn = My_ViPNet()
    # vpn.privileges.permissionRezume()
    logger.info(f'Результат проверки установленной версии ViPNet: {vpn.installed}')
    if vpn.sysKeyInfo:
        for key, value in vpn.sysKeyInfo.items():
            print(f'-----{key}\t\t\t{value}')
    # vpn.privileges.permissionRezume()
else:
    logger.info(f'module_vipnet was loading like module.\nVersion: {VERSION}')

'''
    ==============================Модуль данных об АРМ====================
    ---------------------------------------------------------------------
    Версия 0.3 для xps_astra 0.4

                            В данном модуле получаем сведения
        1. Серийные номера и модели носителей*
        2. MAC-адреса сетевых интерфейсов
        3. Версия ViPNet
        4. Версия KESL
        5. Информация о КриптоПро
        6. Информация о системе Astra linux
        7. Информация о пакетах SUDIS
        8. Информация об установленном системном ключе ViPNet

    *Возможно попадпние SD-карт в список несъёмных носителей

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''
import os

from diskinfo import DiskInfo
from getmac import get_mac_address
from socket import gethostname
from os import popen
from os.path import isfile, isdir, abspath
from re import search

from module_vipnet import My_ViPNet
from module_permissions import My_Permissions

VERSION = '0.3'
HELP = __doc__
SEPORATOR = '-----\n\t'
# {SEPORATOR}
SEPOR_SECTION = '     -------------------------------------'
SEPOR_RUN = '\n     =====================================\n'


class My_pasport:
    '''
    Класс отработки паспортных данных системы
    Атрибуты:
        permissions
        hostname
        astra_version
        astra_update_version
        astra_build_version
        ip
        mac
        volumes
        #-interfaces=[] не работает
        cpro
        cproLic
        sudisInfo
        kesl
        vipnet
        vipnetKey
    Методы:
        __init__
        getVolumes
        printVolumes
        printViPNet
        printViPNetKey
        getMac
        printMac
        getIPaddres
        printIP
        printHostName
        getKesl
        printKesl
        getCpro
        getCproLicense
        printCpro
        printCproLicense
        getAstraVersion
        getAstraUpdate
        getAstraBuild
        printAstraVersion
        printAstraUpdate
        printAstraBuild
        getSudisInfo
        printSudisInfo
        runCLI

    '''

    def __init__(self):
        try:
            priv = My_Permissions()
            self.permissions = priv
            if priv.sudoCanRun:
                pass
            else:
                print('!!!Нет привелегий, данные могут быть неверны, либо не получены!!!')
        except BaseException as error:
            print('!!!Нет привелегий, данные могут быть неверны, либо не получены!!!')

        try:
            self.hostname = gethostname()  # +
            self.astra_version = self.getAstraVersion()  # +
            self.astra_update_version = self.getAstraUpdate()  # +
            self.astra_build_version = self.getAstraBuild()  # +
            self.ip = self.getIPaddres()  # +
            self.mac = self.getMac()  # +
            self.volumes = self.getVolumes()  # +
            # self.interfaces=[] считаем, что у нас один сетефой интерфейс  # -
            self.cpro = self.getCpro()  # +
            self.cproLic = self.getCproLicense()  # +
            self.sudisInfo = self.getSudisInfo()  # +
            self.kesl = self.getKesl()  # +

            print('Получение информации о ViPNet...')
            vpn = My_ViPNet()
            self.vipnet = vpn.installed  # +
            self.vipnetKey = vpn.sysKeyInfo  # +

        except BaseException as error:
            print(f'{SEPORATOR}Ошибка инициализации:\n\t{error}')

    def getVolumes(self):
        '''Возвращает список несъёмых носителей
        словарь диска:
                    path    /dev/sda/ (sdb,nvme итд)
                    model   модель
                    serial  серийный номер
                    size    размер (попробуем в гигабайтах)
                    !!! Есть недостаток !!!
                    Может вернуть SD-карту
                    '''
        volumes = []
        try:
            volumeList = DiskInfo().get_disk_list()
            for i in volumeList:
                if not 'sr' in i.get_name():  # исключаем дисководы
                    # Исключить SD-карты! if not 'mmc' in i.get_name()?
                    if not 'loop' in i.get_name():
                        if not 'usb' in str(i.get_byid_path()):  # исключаем usb-носители
                            # print(f'{i.get_name()},{i.get_path()},{i.get_model()},{i.get_serial_number()},{int(i.get_size()/2097152)} GB')#напечатаем список. После контрольной проверки зарядим единую функцию
                            volumes.append({'name': i.get_name(),
                                            'path': i.get_path(),
                                            'model': i.get_model(),
                                            'serial': i.get_serial_number(),
                                            'size': int(i.get_size() / 2097152)})
        except BaseException as error:
            print(f'При определении носителей возникла ошибка: {error}')
        return volumes

    def printVolumes(self):
        '''
        Распечатка несъёмных носителей
        '''
        if len(self.volumes):
            print(f'{SEPORATOR}Список несъёмных носителей:')
            for i in self.volumes:
                print(f'-Диск: {i.get("name")};')
                print(f'\tМодель: {i.get("model")};')
                print(f'\tСерийный номер: {i.get("serial")};')
                print(f'\tОбъём: {i.get("size")} GB;')
                print(f'\tРасположение: {i.get("path")};')
        else:
            print(f'{SEPORATOR}Список несъёмных носителей пуст.')

    def printViPNet(self):
        if self.vipnet:
            print(f'{SEPORATOR}Установлен ViPNet-клиент версии:\n\t{self.vipnet}')
        else:
            print(f'{SEPORATOR}Вероятно, ViPNet-клиент в данной системе не установлен')

    def printViPNetKey(self):
        if self.vipnetKey:
            if self.vipnetKey['KEYSTATUS']:
                print(f'{SEPORATOR}Информация о системном ключе ViPNet:')
                print(f'\tИмя ключа: {" ".join(self.vipnetKey["NAME"])}')
                print(f'\tИмя сети: {" ".join(self.vipnetKey["NETNAME"])}')
                print(f'\tИдентификатор сети: {" ".join(self.vipnetKey["NETID"])}')
                if self.vipnetKey["AUTOSTART"]:
                    print(f'\tАвтоматический запуск ViPNet с системой: Включен')
                else:
                    print(f'\tАвтоматический запуск ViPNet с системой: Выключен')
                if self.vipnetKey["STATUS"]:
                    print(f'\tТекущее состояние ViPNet: Включен')
                else:
                    print(f'\tТекущее состояние ViPNet: Выключен')
                print(f'\tКоординатор: {" ".join(self.vipnetKey["COORDINATOR"][3:-1])}')
            else:
                print(f'{SEPORATOR}Ключ ViPNet для системы не установлен')
        else:
            # print(f'{SEPORATOR}Ключ ViPNet в для системы не установлен')
            if not self.permissions.sudoCanRun:
                print('Нет привелегий! КЛЮЧ ДЛЯ ПОЛЬЗОВАТЕЛЯ НЕ ОПРЕДЕЛЯЮ')
            else:
                print(f'{SEPORATOR}Ключ ViPNet для системы не установлен')

    def getMac(self):
        '''Возвращаем активный mac
        Считаем, что у нас толко один сетевой интерфейс'''
        return [get_mac_address()]

    def printMac(self):
        if len(self.mac):
            print(f'{SEPORATOR}Список MAC-адресов:')
            for i in self.mac:
                print(f'\t{i}')
        else:
            print(f'{SEPORATOR}Список MAC-адресов пуст.')

    def getIPaddres(self):
        '''
        Вернём ip - адрес активного соединения
        '''
        try:
            out = popen('ip -h -br a | grep UP').read()
            ip = search(r'\d+\.\d+\.\d+\.\d+', out).group()
            return ip
        except BaseException as error:
            print(f'При определении IP-адреса возникла ошибка: {error}')
            return False

    def printIP(self):
        if self.ip:
            print(f'{SEPORATOR}Текущий IPv4-адрес:\n\t{self.ip}')
        else:
            print(f'{SEPORATOR}IP-адрес не определён.\n\tВозможно отсутствует соединение.')

    def printHostName(self):
        if self.hostname:
            print(f'{SEPORATOR}Сетевое имя:\n\t{self.hostname}')
        else:
            print(f'{SEPORATOR}Сетевое имя не определено.')

    def getKesl(self):
        try:
            out = popen('kesl-control --app-info').read()
            out = out.split()
            for i in range(0, len(out) - 1):
                # print(out[i])
                if out[i] == 'Version:':
                    return out[i + 1]
        except BaseException as error:
            print(f'При определении версии Касперский для Linux возникла ошибка: {error}')
            return False

    def printKesl(self):
        if self.kesl:
            print(f'{SEPORATOR}Версия Касперский для Linux:\n\t{self.kesl}')
        else:
            print(f'{SEPORATOR}Версия Касперский для Linux не определена.')

    def getCpro(self):
        try:
            verFile = ''
            if isdir('/etc/opt/cprocsp/'):
                for i in os.listdir('/etc/opt/cprocsp/'):
                    if 'release' in i:
                        verFile = abspath('/etc/opt/cprocsp/' + i)
                out = popen(f'cat {verFile}').read().split()[-1]
                # Возможно устаревшее:
                # if isfile('/opt/cprocsp/bin/amd64/csptestf'):
                #     out = popen('/opt/cprocsp/bin/amd64/csptestf -enum -info | head -n 1').read()
                #     #out = out.split()
                return out
            else:
                return False
        except BaseException as error:
            print(f'При определении версии КриптоПро для Linux возникла ошибка: {error}')
            return False

    def getCproLicense(self):
        #     /opt/cprocsp/sbin/amd64/cpconfig -license -view лицензия
        try:
            if isfile('/opt/cprocsp/sbin/amd64/cpconfig'):
                out = popen('/opt/cprocsp/sbin/amd64/cpconfig -license -view').read()
                # out = out.split()
                return out
            else:
                return False
        except BaseException as error:
            print(f'При определении лицензии КриптоПро для Linux возникла ошибка: {error}')
            return False

    def printCpro(self):
        if self.cpro:
            print(f'{SEPORATOR}Версия КриптоПро для Linux:\n\t{self.cpro}')
        else:
            print(f'{SEPORATOR}Версия КриптоПро для Linux не определена.')

    def printCproLicense(self):
        if self.cproLic:

            print(f'{SEPORATOR}Информация о лицензии КриптоПро для Linux:')
            for i in self.cproLic.split('\n'):
                print(f'\t{i}')
        else:
            print(f'{SEPORATOR}Лицензия КриптоПро для Linux не определена.')

    def getAstraVersion(self):
        try:
            if isfile('/etc/astra_version'):
                out = popen('cat /etc/astra_version').read()
                # out = out.split()
                return out
            else:
                return False
        except BaseException as error:
            print(f'При определении версии Astra Linux возникла ошибка: {error}')
            return False

    def getAstraUpdate(self):
        try:
            if isfile('/etc/astra_update_version'):
                out = popen('cat /etc/astra_update_version').read()
                # out = out.split()
                return out
            else:
                return False
        except BaseException as error:
            print(f'При определении обновления Astra Linux возникла ошибка: {error}')
            return False

    def getAstraBuild(self):
        try:
            if isfile('/etc/astra/build_version'):
                out = popen('cat /etc/astra/build_version').read()
                # out = out.split()
                return out
            else:
                return False
        except BaseException as error:
            print(f'При определении сборки Astra Linux возникла ошибка: {error}')
            return False

    def printAstraVersion(self):
        if self.astra_version:
            print(f'{SEPORATOR}Информация о системе Astra Linux:\n\t{self.astra_version}')
        else:
            print(f'{SEPORATOR}Версия Astra Linux не определена.')

    def printAstraUpdate(self):
        if self.astra_update_version:
            print(f'{SEPORATOR}Информация об обновлениях Astra Linux:\n\t{self.astra_update_version}')
        else:
            print(f'{SEPORATOR}Информация об обновлениях Astra Linux не определена.')

    def printAstraBuild(self):
        if self.astra_build_version:
            print(f'{SEPORATOR}Информация о сборке Astra Linux:\n\t{self.astra_build_version}')
        else:
            print(f'{SEPORATOR}Информация о сборке Astra Linux не определена.')

    def getSudisInfo(self):
        try:
            out = []
            tmpStr = ''
            info = popen('apt-cache show sudis*').read()
            for line in info.splitlines():
                for i in range(len(line.split())):
                    if line.split()[i - 1] == 'Package:':
                        tmpStr = line.split()[i]
                        # print(tmpStr)
                    elif line.split()[i - 1] == 'Version:':
                        # print(line.split()[i])
                        if tmpStr != '':
                            tmpStr = tmpStr + ' ' + line.split()[i]
                            out.append(tmpStr)
                            # print(tmpStr)
            # print(out)
            # ВОЗМОЖНО НАДО БУДЕТ ДОБАВИТЬ, ЕСЛИ СПИСОК НУЛЕВОЙ - ВЕРНУТЬ False
            return out
        except BaseException as error:
            print(f'При определении пакетов СУДИС возникла ошибка: {error}')
            return False

    def printSudisInfo(self):
        if self.sudisInfo:
            print(f'{SEPORATOR}Информация о пакетах СУДИС:')
            for i in self.sudisInfo:
                print(f'\t{i}')
        else:
            print(f'{SEPORATOR}Информация о пакетах СУДИС: не определена.')

    def runCLI(self):
        print(f'Тест модуля "паспорт АРМ {VERSION}" :')
        # Получаем информацию через модуль permissions
        # Отдаём необходимые предупреждения
        try:
            import module_permissions
        except BaseException as error:
            print(f'{SEPORATOR}Ошибка подключения module_permissions:\n\t{error}')

        print(SEPOR_RUN)

        print(SEPOR_SECTION)
        self.printAstraVersion()
        self.printAstraUpdate()
        self.printAstraBuild()

        print(SEPOR_SECTION)
        self.printHostName()
        self.printIP()
        self.printMac()

        print(SEPOR_SECTION)
        self.printVolumes()

        print(SEPOR_SECTION)
        self.printViPNet()
        self.printViPNetKey()
        print(SEPOR_SECTION)
        self.printKesl()
        print(SEPOR_SECTION)
        self.printCpro()
        self.printCproLicense()

        print(SEPOR_SECTION)
        self.printSudisInfo()

        print(SEPOR_RUN)
        if not self.permissions.sudoCanRun:
            print('!!!Нет привелегий, данные могут быть неверны, либо не получены!!!')
        print(SEPOR_SECTION)
        print(f"\tASTRA PASPORT V.{VERSION}\n\tМотрич Р.Д.\n\tascent.mrd@yandex.ru\n\t2025 г.\n")

        return 0


if __name__ == '__main__':

    try:
        pasport = My_pasport()
        pasport.runCLI()

    except BaseException as error:
        print(f'Ошибка выполнения:\n\t{error}')

else:
    print(f'module_passport was loading like module.\nVersion: {VERSION}')

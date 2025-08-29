'''
    ==============================Модуль режима терминала================
    ---------------------------------------------------------------------
    Версия 0.4.a для xps_astra 0.4

        Модуль работает без ключей - режим поиска файла xps на рабочем
    столе, вывод содержимого первой страницы, выявление и
    прередача пароля в буфер обмена*.
        Ключи:
            -i  Установка ключа с рабочего стола
                Ответы, если уже имеется установленный ключ:
                y   Замена текущего ключа на новый
                n   Оставить текущий ключ и выйти
                d   Удалить текущий ключ и выйти
            -p  Выводит паспортную информацию о системе
            -t  Сохраняет xps с рабочего стола в txt
            -d  Сохраняет все xps из указанного каталога в txt
            -h  Выводит текущее сообщение, либо html* помощь.
            --autorun*   Включить автозапуск клиента с системой, если
                выключено.
            -m Режим меню.
            --hardware - краткая сводка по железу и системе

    *не реализовано

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''
import sys
import time

from module_permissions import My_Permissions
from module_xps import ReaderXPS, Mass_ReaderXPS
from module_vipnet import My_ViPNet

VERSION = '0.4.a'
HELP = __doc__


class CLI_class:
    '''Класс работы CLI'''

    def __init__(self):
        self.permissions=My_Permissions()

    def argReseption(self,args=None):
        '''
        Посмотрим прилетевший ключ
        :return:
        '''

        from sys import argv

        if args:
            print("Взятие рукописного ключа.")
           # print(args.split(' '))
            argv = args.split(' ')
        print(argv)
        if '-h' in argv:
            print('Help')
            self.help()
        elif '-p' in argv:
            print('Pasport')
            self.pasport()
        elif '-i' in argv:
            print('Install')
            self.installKey()
        elif '-t' in argv:
            print('Save txt')
            self.saveTxt()
        elif '-d' in argv:
            print('Save txt directory')
            self.saveTxtDir(args)
        elif '-m' in argv:
            print('Menu mode')
            self.menu()
        elif '--hardware' in argv:
            print('Hardvare info')
            self.hardwareInfo()

        else:
            print('Only xps read')
            self.passwordXps()

    def help(self,menuY=False):
        '''Вывод справки'''
        if not menuY:
            print('Help_start.')
        try:
            print(HELP)
            if not menuY:
                input('Enter для выхода.')
        except BaseException as error:
            print(f'Ошибка функции помощь:\n\t{error}')
            return False
        else:
            return True

    def pasport(self):
        '''Вывод паспорта'''
        print('Pasport_start.')
        try:
            from module_pasport import My_pasport
            currentPasport = My_pasport()
            currentPasport.runCLI()
        except BaseException as error:
            print(f'Ошибка функции паспорт:\n\t{error}')
            return False
        else:
            return True
    def hardwareInfo(self):
        print('hardwareInfo run')
        self.permissions.runSudoCommand('./sysinfo.sh')


    def installKey(self):
        '''
        Установка ключа:
            Проверка випнет,
            Проверка ключа,
            Проверка автозапуска
        '''
        reinstall='N'
        print('Install_key_start.')
        if self.permissions.sudoCanRun:
            print('Привелегии соответствуют требованиям операции.')
            print('Получение входных данных.')
            directory=self.permissions.userDesktop.split()[0]
            client=My_ViPNet()
            print(f'!!!!!!!!!!!!!!!!!!\nОШИБКА КЛИЕНТА\n{client.error}\n!!!!!!!!!!!!!!!!!')
            if client.installed :
                print(f'Версия ViPNet: {client.installed}')
                if not client.installedKey:
                    print('Считаю, что DST-ключ не установлен.')
                    client.printKeyInfoWide()
                    print('Поиск dst-файла на Рабочем столе...')
                    dstFile=client.findFirstInDir(dirname=self.permissions.userDesktop.split()[0])
                    print('Поиск xps-файла на Рабочем столе...')
                    try:
                        xpsFile=Mass_ReaderXPS(dirname=self.permissions.userDesktop.split()[0]).fileList[0]
                    except BaseException as error:
                        xpsFile=None
                    #print(xpsFile)
                    print('Установка нового ключа.')
                    client.installKey(dstFile,xpsFile)
                    print('Проверка состояния.')
                    client.refresh()
                    client.printKeyInfoWide()
                else:
                    print('!!!-----DST-ключ уже установлен.\nИНФОРМАЦИЯ:')
                    client.printKeyInfoWide()
                    reinstall=input('!!!-----Желаете переустановить?(y/n/d):')
                    if reinstall == 'y':
                        print('Приступаю к замене ключа.')
                        print('Поиск dst-файла на Рабочем столе...')
                        dstFile = client.findFirstInDir(dirname=self.permissions.userDesktop.split()[0])
                        print('Поиск xps-файла на Рабочем столе...')
                        try:
                            xpsFile = Mass_ReaderXPS(dirname=self.permissions.userDesktop.split()[0]).fileList[0]
                        except BaseException as error:
                            xpsFile = None
                        if dstFile:
                            print('Удаление текущего ключа.')
                            client.deleteKey()
                            client.refresh()
                            print('Проверка состояния.')
                            client.printKeyInfoWide()
                            print('Установка нового ключа.')
                            client.installKey(dstFile,xpsFile)
                            print('Проверка состояния.')
                            client.refresh()
                            client.printKeyInfoWide()
                        else:
                            print('Файл ключа на рабочем столе не найден.')
                    elif reinstall == 'd':
                        print('Приступаю к удалению ключа.')
                        client.deleteKey()
                        client.refresh()
                        print('Проверка состояния.')
                        client.printKeyInfoWide()
                    else:# reinstall == 'n':
                        print('Отмена...')
            else:
                print('Клиент не установлен.\nЗавершаю работу.')
                return False
        else:
            print('Повторите запуск с повышением привелегий. (Возможная команда: "sudo !!")')
            return False
        return True

    def saveTxt(self):
        print('Save_txt_start.')
        print(self.permissions.userDesktop.split()[0])
        dirInfo = Mass_ReaderXPS(dirname=self.permissions.userDesktop.split()[0])  # ,fulldada=True)
        # dirInfo.printDataList(showfull=True)
        if dirInfo.dirName:
            if dirInfo.fileList:
                doc = ReaderXPS(dirInfo.fileList[0])
                # print(f'\tСОДЕРЖИМОЕ:\n{" ".join(doc.readList)}')
                # print(f'\tПАРОЛЬ:\n{doc.getPasswd()}')
                doc.saveAsTxt()
                return True
            else:
                print('Ошибка поиска файлов.')
                return False
        else:
            print(f'Ошибка работы с каталогом.')
            return False

    def saveTxtDir(self,args=None):
        from sys import argv
        print('Save txt dir start')
        try:

            if args:
                dir=args.split(' ')[-1]
                docs=Mass_ReaderXPS(dirname=dir)
                docs.writeDirToTXT()
            else:
                dir = sys.argv[-1]
                docs = Mass_ReaderXPS(dirname=dir)
                docs.writeDirToTXT()

        except BaseException as error:
            print(f'Возникла ошибка {error} на ключе -d')
        else:
            return True

    def passwordXps(self):
        print('Password_start.')
        print(self.permissions.userDesktop.split()[0])
        dirInfo=Mass_ReaderXPS(dirname=self.permissions.userDesktop.split()[0])#,fulldada=True)
        # dirInfo.printDataList(showfull=True)
        if dirInfo.dirName:
            if dirInfo.fileList:
                doc=ReaderXPS(dirInfo.fileList[0])
                print(f'\tСОДЕРЖИМОЕ:\n{" ".join(doc.readList)}')
                print(f'\tПАРОЛЬ:\n{doc.getPasswd()}')
                return doc.getPasswd()
            else:
                print('Ошибка поиска файлов.')
                return False
        else:
            print(f'Ошибка работы с каталогом.')
            return False

    def menu(self):
        try:
            self.help(True)
            article=input("Введите необходимый ключ:\n")
        except BaseException as error:
            print(f'Ошибка функции меню:\n\t{error}')
            return False
        else:
            self.argReseption(article)
            return True



if __name__ == '__main__':
    print(f'CLI_module was loading like program.\nVersion: {VERSION}')
    run = CLI_class()
    run.argReseption()
    print('Выход...')
    time.sleep(5)
    input("press Enter to exit")
    # Проверим аргументы
else:
    print(f'CLI_module was loading like module.\nVersion: {VERSION}')

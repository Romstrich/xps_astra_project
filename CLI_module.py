'''
    ==============================Модуль режима терминала================
    ---------------------------------------------------------------------
    Версия 0.4 для xps_astra 0.4

        Модуль работает без ключей - режим поиска файла xps на рабочем
    столе, вывод содержимого первой страницы, выявление и прередача
    пароля в буфер обмена.
        Ключи:
            *-i  Установка ключа с рабочего стола
            -p  Выводит паспортную информацию о системе
            -t  Сохраняет xps с рабочего стола в txt
            *-d  Сохраняет все xps из указанного каталога в txt
            -h  Выводит текущее сообщение, либо *html - помощь

    *не реализовано

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''
from module_permissions import My_Permissions
from module_xps import ReaderXPS, Mass_ReaderXPS

VERSION = '0.4'
HELP = __doc__


class CLI_class:
    '''Класс работы CLI'''

    def __init__(self):
        self.permissions=My_Permissions()

    def argReseption(self):
        '''
        Посмотрим прилетевший ключ
        :return:
        '''

        from sys import argv

        print(argv)
        if '-h' in argv:
            print('Help')
            self.help()
        elif '-p' in argv:
            self.pasport()
        elif '-i' in argv:
            print('Install')
        elif '-t' in argv:
            print('Save txt')
            self.saveTxt()
        elif '-d' in argv:
            print('Save txt directory')
        else:
            print('Only xps read')
            self.passwordXps()

    def help(self):
        '''Вывод справки'''
        print('Help_start.')
        try:
            print(HELP)
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

    def installKey(self):
        print('Install_key_start.')
        pass

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

    def saveTxtDir(self):
        from sys import argv
        print('Save txt dir start')

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
                return True
            else:
                print('Ошибка поиска файлов.')
                return False
        else:
            print(f'Ошибка работы с каталогом.')
            return False



if __name__ == '__main__':
    print(f'CLI_module was loading like program.\nVersion: {VERSION}')
    run = CLI_class()
    run.argReseption()

    # Проверим аргументы
else:
    print(f'CLI_module was loading like module.\nVersion: {VERSION}')

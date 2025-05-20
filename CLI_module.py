'''
    ==============================Модуль режима терминала================
    ---------------------------------------------------------------------
    Версия 0.4 для xps_astra 0.4

        Модуль работает без ключей - режим поиска файла xps на рабочем
    столе, вывод содержимого первой страницы, выявление и прередача
    пароля в буфер обмена.
        Ключи:
            -i  Установка ключа с рабочего стола
            -p  Выводит паспортную информацию о системе
            -t  Сохраняет xps с рабочего стола в txt
            -h  Выводит текущее сообщение, либо html - помощь

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''

HELP=__doc__

class CLI_class:
    '''Класс работы CLI'''
    def __init__(self):
        pass

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
        else:
            print('Only xps read')

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
        print('Pa_start.')
        pass

    def saveTxt(self):
        print('Pasport_start.')
        pass

    def passwordXps(self):
        print('Pasport_start.')
        pass


if __name__ == '__main__':
    print('CLI_module was loading like program')
    run=CLI_class()
    run.argReseption()

    # Проверим аргументы
else:
    print('CLI_module was loading like module')

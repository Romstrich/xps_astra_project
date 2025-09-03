'''
    ==============================Модуль режима GUI-интерфейса===========
    ---------------------------------------------------------------------
    Версия 0.3 для xps_astra 0.5

        Модуль реализации графического интерфейса, включаещего в себя:
        - главное окно программы
        - Приветственное сообщение
        *- окно состояния ViPNet
        *- окно информации о программе
        *- окно паспортной информации
        *- окно системной информации
        *- вызов локальной веб-справки
        *- диалоговые окна
        *- ведение логов

    Сейчас: Наладка главного окна, шрифта и т.д. (оформление)


    *не реализовано

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''
'''
    Файлы для доп импорта:
        lib/PT-Astra-Serif_Regular.ttf
'''

import logging, os.path
# import tkinter
from tkinter import filedialog, ttk, font, Tk, Menu
from module_permissions import My_Permissions
from module_messenger import My_logger
from module_vipnet import My_ViPNet
from pathlib import Path

VERSION = '0.3'
HELP = __doc__
TITLE='xps_astra v0.5 in development'
    # =============Настройка логирования
logger=My_logger
    #логи в консоль

    # =============Настройка логирования конец

    # =============Класс, определяющий поведение окна
class mainWin(Tk):
    '''
    GUI сборка приложения
    '''
    def __init__(self,title='',*args, **kwargs):
        super().__init__(*args, **kwargs)
        # -----------Объект работы с данными
        logger.info('Загрузка BACKEND')
        self.backEnd = BackEndWork()
        self.xfilepath=False
        self.dfilepath = False
        self.xdirpath=False
        self.xddirpath = False
        # -----------Загрузим кастомный шрифт
        try:
            logger.info('Загрузка шрифта')
            custom_font_path = "lib/PT-Astra-Serif_Regular.ttf"
            custom_font = font.Font(family="AstraFont", size=12, name="custom_font")
            custom_font.configure(family=custom_font_path)
            self.option_add('*Font', custom_font)
            logger.info('Шрифт загружен')
        except BaseException as error:
            logger.error("Неудачная загрузка шрифта")

        # -----------Геометрия главного окна
        self.resizable(width=False, height=False)
        self.geometry("500x300")
        self.title(title)
        # -----------Определим состоянме вспомогательных окон
        # -----------Соберём главное меню
        self.mainmenu = Menu(self)


        # =============Сборка раздела "Файл"
        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Открыть xps", command=lambda: self.openXPSFile(self.backEnd.permission.userDesktop.split()[0]))
        self.filemenu.add_command(label="Открыть dst", command=lambda: self.openDSTFile(self.backEnd.permission.userDesktop.split()[0]))
        self.filemenu.add_command(label="Открыть каталог (xps+dst)",command=lambda: self.openDirxpsdst(self.backEnd.permission.userDesktop.split()[0]))
        self.filemenu.add_command(label="Открыть каталог (все xps)",command=lambda: self.openDirxps(self.backEnd.permission.userDesktop.split()[0]))
        # =============Сборка раздела экспорта в txt
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Сохранить как txt", state='disabled')  # , command=self.openfile)
        self.filemenu.add_command(label="Сохранить все как txt", state='disabled')  # , command=self.openfile)
        # =============Сборка пункт меню выход - завершает программу
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Выход", command=self.destroy)
        # =============Сборка раздела "ViPNet"
        #
        self.vipnetmenu = Menu(self.mainmenu, tearoff=0)
        self.vipnetmenu.add_command(label="Информация о ViPNet (система)")  # , command=self.openfile)
        self.vipnetmenu.add_command(label="Установить ключ (система)")  # , command=self.openfile)
        self.vipnetmenu.add_separator()
        self.vipnetmenu.add_command(label="Запуск ViPNet (система)")  # , command=self.openfile)
        # self.vipnetmenu.add_command(label="Остановить ViPNet (система)")  # , command=self.openfile)
        self.vipnetmenu.add_command(label="Отключить автозапуск ViPNet")
        self.vipnetmenu.add_separator()
        self.vipnetmenu.add_command(label="ViPNet-GUI (система)")  # , command=self.openfile)
        self.vipnetmenu.add_separator()
        self.vipnetmenu.add_command(label="Удалить системный ключ")  # , command=self.openfile)
        # =============Сборка раздела "Система"
        self.sysmenu=Menu(self.mainmenu,tearoff=0)
        self.sysmenu.add_command(label='Информация для паспорта')
        self.sysmenu.add_command(label='Информация системная')
        # =============Сборка раздела "Справка"
        self.helpmenu = Menu(self.mainmenu,tearoff=0)#, tearoff=0)
        self.helpmenu.add_command(label="Инструкция")#, command=self.open_help)
        self.helpmenu.add_command(label="Помощь")#, command=self.openManual)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="О программе")#, command=self.open_about)
        # =============Добавление разделов в главное меню
        self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)
        self.mainmenu.add_cascade(label="ViPNet", menu=self.vipnetmenu)#, state='disabled')
        self.mainmenu.add_cascade(label='Система',menu=self.sysmenu)
        self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)

        self.config(menu=self.mainmenu)

        self.greetMessage()

        # =============Проверка для пунктов меню
    def refreshMenu(self):
            '''Отключение пунктов меню по "показаниям"
            self.backend=BackEndWork()
            '''
            pass
        # =============Окончание сборки главного окна
    # =============Процедура при запуске: 1.права, 2. випнет и ключ, 3. дст и xps
        # =============Выдача окна с сообщением, предложением установки
    def greetMessage(self):
        '''Окно приветствия
                                ЕСТЬ            НЕТ
        Права
        Випнет                  устан
        установленный ключ      удал+устан      устан
        ключ на столе           устан
        пароль на столе         устан           устан+введите пароль

        '''
        can_instlall=False
        refresh_key=False
        message=''
        resumeMsg=''

        if self.backEnd.permission.sudoCanRun:
            can_instlall = True and can_instlall
            message += 'Привелегии исполнения есть\n'
            if self.backEnd.xpsFile:
                message += 'Файл пароля есть\n'
                can_instlall = True
            else:
                message += 'Файла пароля нет\n'  # установка из программы
                can_instlall = False
            if self.backEnd.dstFile:
                message += 'Файл ключа есть\n'
                can_instlall = True and can_instlall
            else:
                message += 'Файла ключа нет\n'  # установка из программы
                can_instlall = False and can_instlall
            if self.backEnd.vipnet.installed:
                if self.backEnd.vipnet.installedKey:
                    refresh_key = True
                    message += 'Имеется установленный ключ:\n'
                    message += ' '.join(self.backEnd.vipnet.sysKeyInfo['NAME']) + '\n'
                    can_instlall = True and can_instlall
                else:
                    message += 'Установленного ключа нет\n'
                    can_instlall = True and can_instlall
            else:
                message += 'Клиент не установлен\n'
                can_instlall = False and can_instlall
        else:
            message += 'Перезапустите программу с повышением привелегий\n'
            can_instlall = False and can_instlall
        logger.info(message)
        logger.info(f'Замена ключа-{refresh_key}')
        logger.info(f'Установить сейчас-{can_instlall}')

        # =============Открытие документа и каталога
    def openXPSFile(self,path=False):
        fTypes = [('Файлы xps', '.xps')]#, ('Файлы txt', '.txt')]  # ,('Текстовые файлы','.txt')]
        if path:
            self.xfilepath = filedialog.askopenfilename(filetypes=fTypes,initialdir=path)
        else:
            self.xfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir='/home')

    def openDSTFile(self,path=False):
        fTypes = [('Файлы dst', '.dst')]  # , ('Файлы txt', '.txt')]  # ,('Текстовые файлы','.txt')]
        if path:
            self.dfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir=path)
        else:
            self.dfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir='/home')

    def openDirxps(self,path=False):
        if path:
            self.xdirpath = filedialog.askdirectory(initialdir=path)
        else:
            self.xdirpath = filedialog.askdirectory(initialdir='/home')
        #Проверяем, есть ли xps в даннном каталоге, если есть - включаем пункт меню, -нет вывключаем

    def openDirxpsdst(self,path=False):
        if path:
            self.xddirpath = filedialog.askdirectory(initialdir=path)
        else:
            self.xddirpath = filedialog.askdirectory(initialdir='/home')
    #Проверяем есть ли в данном каталоге xps и дст


class BackEndWork():
    '''Класс внутренней работы'''
    def __init__(self):
        '''
        Стартовая проверка
            права
            випнет
            наличие ключа и дст на рабочем столе
        '''
        logger.info("Проверка разрешений")
        self.permission=My_Permissions()
        logger.info("Проверка ViPNet клиента")
        self.vipnet=My_ViPNet()
        #передача пароля с рабочего стола
        self.xpsFile=self.checkXPSfile(dirpath=self.permission.userDesktop.split()[0])
        self.dstFile=self.checkDSTfile(dirpath=self.permission.userDesktop.split()[0])
        pass

    # =============Проверки по файлам и каталогам

    def checkXPSfile(self,filepath=False,dirpath=False):
        '''Наличие xps'''
        if dirpath:
            return self.searchBySuffix(dirname=dirpath,suff='.xps')
        elif filepath:
            pass
        else:
            return False

    def checkDSTfile(self,filepath=False,dirpath=False):
        '''наличие dst'''
        if dirpath:
            return self.searchBySuffix(dirname=dirpath, suff='.dst')
        elif filepath:
            pass
        else:
            return False

    def checkXPSdir(self):
        '''Проверка предполагаемой дирректории с xps-сами'''
        return False

    def checkXPSDSTdir(self):
        '''В каталоге должен быть и xps и дст'''
        return False

    def searchBySuffix(self,dirname,suff):
        '''поиск по расширению файла'''
        if os.path.isdir(dirname):
            logger.info(f'Каталог {dirname} существует')
            dirName=os.path.abspath(dirname)
            if dirName:
                logger.info(f'Получим список файлов с расширением {suff}\t{dirName}')
                filelist = os.listdir(dirName)
                for i in filelist:
                    if Path(i).suffix == suff:
                        logger.info(f'Получили файл: {Path(i)}')
                        return Path(i)
                else:
                    logger.info(f'Файлы {suff} в каталоге {dirname} не обнаружены')
                    return False
            else:
                logger.error(f'Не могу получить список файлов.\n\tСостояние каталога: {dirName}')
                return False
        else:
            logger.error(f'Каталог {dirname} по указанному пути не существует.\n\tПроверьте путь.')
            return False



if __name__ == '__main__':
    logger.info(f'GUI_module was loading like program.\nVersion: {VERSION}')
    testWindow=mainWin(title=TITLE)
    testWindow.mainloop()
    logger.info("Завершение и выход.")
else:
    logger.info(f'GUI_module was loading like module.\nVersion: {VERSION}')

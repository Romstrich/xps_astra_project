'''
    ==============================Модуль режима GUI-интерфейса===========
    ---------------------------------------------------------------------
    Версия 0.3 для xps_astra 0.5

        Модуль реализации графического интерфейса, включаещего в себя:
        - главное окно программы
        - Приветственное сообщение, оно же  диагностическое
        *- окно состояния ViPNet
        *- окно информации о программе
        *- окно паспортной информации
        *- окно системной информации
        *- вызов локальной веб-справки от лица пользователя
        *- диалоговые окна
        - ведение логов
        - загрузка шрифта
        *- загрузка иконки

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
from tkinter import filedialog, ttk, font, Tk, Menu,PhotoImage,Text, Label,SUNKEN, X,W
from tkinter.messagebox import showinfo,showwarning
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
    функции
    аргументы
    '''
    def __init__(self,title='',*args, **kwargs):
        super().__init__(*args, **kwargs)
        # -----------Объект работы с данными
        logger.info('Загрузка BACKEND')
        self.backEnd = BackEndWork()
        self.xfilepath=False
        self.dfilepath = False
        self.xtdirpath=False
        self.xddirpath = False
        # -----------Загрузим кастомный шрифт и иконку
        try:
            logger.info('Загрузка шрифта')
            custom_font_path = "lib/PT-Astra-Serif_Regular.ttf"
            custom_font = font.Font(family="AstraFont", size=12, name="custom_font")
            custom_font.configure(family=custom_font_path)
            self.option_add('*Font', custom_font)
            logger.info('Шрифт загружен')
        except BaseException as error:
            logger.error("Неудачная загрузка шрифта")
        try:
            logger.info('Загрузка иконки')
            icon=PhotoImage(file="lib/ico.png")
            self.iconphoto(True,icon)
            logger.info('Иконка загружена')
        except BaseException as error:
            logger.error("Неудачная иконки")

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
        self.sysmenu.add_command(label='Диагностическое окно',command=lambda : self.greetMessage(hide=False,refresh=True))
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

        # =============Сборка зоны просмотра и строки состояния
            # =============Сборка зоны просмотра
        self.xpsText=Text(height=13 )
        self.xpsText.place(relx=0,rely=0)
        self.xpsText.pack(fill=X)
            # =============Сборка строки состояния
        self.statusBar = Label(self, bd=1, relief=SUNKEN, anchor=W,height=2)
        self.statusBar.pack(fill=X)

        # =============Диагностическое окно приветствия
        self.greetMessage()

        # =============Проверка для пунктов меню, текстового поля и панели состояния
    def refreshMenu(self):
            '''Отключение пунктов меню по "показаниям"
            self.backend=BackEndWork()
            '''
            self.backEnd.refresh(xpsPath=self.xfilepath,dstPath=self.dfilepath,
                                 dirPath=self.xddirpath,dirTxtPath=self.xtdirpath)

    def refreshText(self):
        '''

        :return:
        '''
        pass

        # =============Окончание сборки главного окна
    # =============Процедура при запуске: 1.права, 2. випнет и ключ, 3. дст и xps
        # =============Выдача окна с сообщением, предложением установки
    def greetMessage(self,hide=True,refresh=False):
        '''Окно приветствия
        +Нацелиться на побновление в процессе работы программы
        !!!Параметры для обновления
                                ЕСТЬ            НЕТ
        Права
        Випнет                  устан
        установленный ключ      удал+устан      устан
        ключ на столе           устан
        пароль на столе         устан           устан+введите пароль
        can_install-отвечает на вопрос возможности установки
        refresh_key-необходимость заменять ключ
        #greetWin-окно сообщения
        '''
        if refresh:
            self.backEnd.refresh()
        message=''
        greetDict=self.backEnd.greetOptions()
        if greetDict['permis']:
            #can_instlall = True and can_instlall
            message += '-Привелегии исполнения есть.\n'
            if greetDict['xps_exists']:
                message += 'Файл пароля на рабочем столе: -есть\n'
                # can_instlall = True
            else:
                message += 'Файла пароля на рабочем столе: -нет\n'  # установка из программы
                # can_instlall = False
            if greetDict['dst_exists']:
                message += 'Файл ключа на рабочем столе: -есть\n'
                # can_instlall = True and can_instlall
            else:
                message += 'Файла ключа на рабочем столе: -нет\n'  # установка из программы
                # can_instlall = False and can_instlall
            if greetDict['client_exists']:
                if greetDict['refresh_key']:
                    # refresh_key = True
                    message += 'Имеется установленный ключ:\n'
                    message += '-! '+' '.join(self.backEnd.vipnet.sysKeyInfo['NAME']) #+ '\n'
                    # can_instlall = True and can_instlall
                else:
                    message += '-Установленного ключа нет\n-Клиент установлен'
                    # can_instlall = True and can_instlall
            else:
                message += '-! Клиент не установлен\n'
                # can_instlall = False and can_instlall
        else:
            message += '! Перезапустите программу с повышением привелегий.\n-Ограниченный функционал.'
            # can_instlall = False and can_instlall
        if self.backEnd.vipnet.error:
            message+='Рекомендую переустановить клиент.'
        logger.info(message)
        logger.info(f'Замена ключа-{greetDict["refresh_key"]}')
        logger.info(f'Установить сейчас-{greetDict["can_install"]}')
        if hide:
            self.withdraw()
        if greetDict["can_install"]:
            if greetDict['refresh_key']:
                showwarning(title="Предупреждение-установлен ключ", message=message)#+'!')
            else:
                showinfo(title="Информация",message=message)
        else:
            showwarning(title="Предупреждение",message=message)
        if hide:
            self.deiconify()





        # =============Открытие документа и каталога
    def openXPSFile(self,dirPath=False):
        logger.info('Открытие файла xps')
        fTypes = [('Файлы xps', '.xps')]#, ('Файлы txt', '.txt')]  # ,('Текстовые файлы','.txt')]
        if dirPath:
            self.xfilepath = filedialog.askopenfilename(filetypes=fTypes,initialdir=dirPath)
        else:
            self.xfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir='/home')
        self.refreshMenu()

    def openDSTFile(self,dirPath=False):
        fTypes = [('Файлы dst', '.dst')]  # , ('Файлы txt', '.txt')]  # ,('Текстовые файлы','.txt')]
        if dirPath:
            self.dfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir=dirPath)
        else:
            self.dfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir='/home')

    def openDirxps(self,dirPath=False):
        if dirPath:
            self.xdirpath = filedialog.askdirectory(initialdir=dirPath)
        else:
            self.xdirpath = filedialog.askdirectory(initialdir='/home')
        #Проверяем, есть ли xps в даннном каталоге, если есть - включаем пункт меню, -нет вывключаем

    def openDirxpsdst(self,dirPath=False):
        if dirPath:
            self.xddirpath = filedialog.askdirectory(initialdir=dirPath)
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
        self.vipnet=My_ViPNet(permis=self.permission)
        if self.vipnet.error:
            logger.error('Ошибка обращения к vipnetcient. Рекомендую переустановить.')
        #передача пароля с рабочего стола
        self.xpsFile=self.checkXPSfile(dirpath=self.permission.userDesktop.split()[0])
        self.dstFile=self.checkDSTfile(dirpath=self.permission.userDesktop.split()[0])
        pass

    # =============Обновление пременных, выдыча данных

    def refresh(self,xpsPath=False,dstPath=False,dirPath=False,dirTxtPath=False):
        '''Обновление данных
        !!!Получить входные параметры
        if xpsPath+dstPath+dirPath+dirTxtPath==False:
TypeError: can only concatenate str (not "bool") to str

        xpsPath=путь к xps
        dstPath=путь к dst
        dirPath=каталог xps+dst
        dirTxtPath=каталог xps для перехода в txt
        (по аналогии с __init__)'''
        logger.info("Обновление данных")
        self.permission.refresh()
        logger.info("Проверка ViPNet клиента")
        self.vipnet.refresh()
        if self.vipnet.error:
            logger.error('Ошибка обращения к vipnetcient. Рекомендую переустановить.')
        # передача файлов пароля и dst
        logger.info("Проверка файлов")
        if dirPath:
            #В приоретете
            logger.info('Смотрим переданный каталог xps+dst')
            pass
        else:
            #смотрим далее xps
            if xpsPath:
                logger.info('Смотрим переданный xps')
            # смотрим далее dst
            if dstPath:
                logger.info('Смотрим переданный dst')
            # смотрим далее каталог для преобразования в дст
            if dirTxtPath:
                logger.info('Смотрим переданный каталог xps в dst')
        #если ничего нет падаем по дефолту:
        if bool(xpsPath)+bool(dstPath)+bool(dirPath)+bool(dirTxtPath)==False:
            logger.info('Смотрим рабочий стол')
            self.xpsFile = self.checkXPSfile(dirpath=self.permission.userDesktop.split()[0])
            self.dstFile = self.checkDSTfile(dirpath=self.permission.userDesktop.split()[0])
        logger.info('Файлы проверены')

    def refreshText(self):
        '''
        Обновленние информации для текстового поля и панели состояния
        :return:
        '''


    def greetOptions(self,refresh=False):
        '''Функция для приветсвенного окна
        И НЕ ТОЛЬКО
        can_install=можно ставить
        permis=привилегии
        xps_exists=есть xps
        dst_exists=есть dst
        refresh_key=есть установленный ключ
        client_exists = клиент установлен
        ВОЗВРАЩАЕТ СЛОВАРЬ ЭТИХ ДАННЫХ'''
        if refresh:
            self.refresh()
        can_install=True
        permis=False
        xps_exists=False
        dst_exists=False
        refresh_key=False
        client_exists = True

        if self.permission.sudoCanRun:
            can_instlall = True and can_install
            permis=True
            if self.xpsFile:
                xps_exists=True
                can_install = True
            else:
                xps_exists=False
                can_install = False
            if self.dstFile:
                dst_exists=True
                can_install = True and can_install
            else:
                dst_exists=False
                can_install = False and can_install
            if self.vipnet.installed:
                if self.vipnet.error:
                    logger.error('Ошибка обращения к vipnetcient. Рекомендую переустановить.')
                if self.vipnet.installedKey:
                    refresh_key = True
                    can_install = True and can_install
                else:
                    refresh_key=False
                    can_install = True and can_install
            else:
                client_exists=False
                can_install = False and can_install
        else:
            permis=False
            can_install = False and can_install
        return {'permis':permis,'can_install':can_install,
                'xps_exists':xps_exists,'dst_exists':dst_exists,
                'refresh_key':refresh_key,'client_exists':client_exists}

    # =============Проверки по файлам и каталогам

    def checkXPSfile(self,filepath=False,dirpath=False):
        '''Наличие xps'''
        if dirpath:
            return self.searchBySuffix(dirname=dirpath,suff='.xps')
        elif filepath:
            pass
            #вернуть filepath, если всё в порядке
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
    # try:
    logger.info(f'GUI_module was loading like program.\nVersion: {VERSION}')
    testWindow=mainWin(title=TITLE)
    testWindow.mainloop()
    logger.info("Завершение и выход.")
    # except BaseException as error:
    #     logger.error(f"Аварийное завершение: {error}")
else:
    logger.info(f'GUI_module was loading like module.\nVersion: {VERSION}')

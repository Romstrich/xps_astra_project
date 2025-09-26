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
        - ведение логов (+наличие диагностического режима)
        - загрузка шрифта
        - загрузка иконки

    +Сейчас: Наладка главного окна, шрифта и т.д. (оформление)
    *Сейчас: Наладка обработки xps-документа, создание вспомогательных окон,
        проработка инструкции и помощи
    *Сейчас: -Запрет редактирования текстового поля
            -Реализация копирования из текстового поля
            -Вывод в текстовое поле каталога xps, реализация массового сохранения, отработка
            ситуации, когда документы не обнаружены.
    *Сейчас: -Отладка пунктов меню. Их показ и скрытие в зависимости от состояния выполнения

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
from tkinter import filedialog, ttk, font, Tk, Menu,PhotoImage,Text, Label,SUNKEN, X,W,END,LEFT
from tkinter.messagebox import showinfo,showwarning,showerror
from module_permissions import My_Permissions
from module_messenger import My_logger
from module_vipnet import My_ViPNet
from module_xps import ReaderXPS,Mass_ReaderXPS
from pathlib import Path
from module_xps import ReaderXPS
from module_sysinfo import My_System

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
        #self.xfilepath=False
        #self.dfilepath = False
        #self.xtdirpath=False
        #self.xddirpath = False
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
            logger.error("Неудачная загрузка иконки")

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
        # self.filemenu.add_command(label="Открыть каталог (xps+dst)",command=lambda: self.openDirxpsdst(self.backEnd.permission.userDesktop.split()[0]))
        self.filemenu.add_command(label="Открыть каталог (все xps)",command=lambda: self.openDirxps(self.backEnd.permission.userDesktop.split()[0]))
        # =============Сборка раздела экспорта в txt
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Сохранить как txt", state='disabled',command=lambda: self.saveAsTxt())  # , command=self.openfile)
        self.filemenu.add_command(label="Сохранить все как txt", state='disabled',command=lambda: self.saveDirxps())  # , command=self.openfile)
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
        self.helpmenu.add_command(label="О программе",command=self.softInfo)#, command=self.open_about)
        # =============Добавление разделов в главное меню
        self.mainmenu.add_cascade(label="Файл", menu=self.filemenu)
        self.mainmenu.add_cascade(label="ViPNet", menu=self.vipnetmenu)#, state='disabled')
        self.mainmenu.add_cascade(label='Система',menu=self.sysmenu)
        self.mainmenu.add_cascade(label="Справка", menu=self.helpmenu)

        self.config(menu=self.mainmenu)

        # =============Сборка зоны просмотра и строки состояния
        # =============Сборка копирования (правой кнопкой мыши)
        self.copyMenu = Menu(self, tearoff=0)
        self.copyMenu.add_command(label='Копировать', command=self.copySelected)

            # =============Сборка зоны просмотра
        self.xpsText=Text(height=13,state='disabled')
        self.xpsText.place(relx=0,rely=0)
        self.xpsText.bind("<Button-3>",self.showConMenu)
        self.xpsText.pack(fill=X)
            # =============Сборка строки состояния
        self.statusBar = Label(self, bd=1, relief=SUNKEN, anchor='nw',height=4,font=font.Font(size=6),justify='left')
        self.statusBar.pack(fill=X)


        # =============Диагностическое окно приветствия
        self.greetMessage()
        # self.refreshText()
        # self.refreshStatusBar()
        # self.refreshMenu()

        # =============Проверка для пунктов меню, текстового поля и панели состояния

    # =============Контекстное меню

    def showConMenu(self, event):
        self.copyMenu.post(event.x_root, event.y_root)
    def copySelected(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.xpsText.selection_get())
            logger.info('Выделенное скопировано.')
        except BaseException as error:
            logger.error(f'Ошибка копирования: {error}')

    # =============Доступ к пулнктам меню

    def refreshMenu(self):
            '''Отключение пунктов меню по "показаниям"
            self.backend=BackEndWork()
            '''
            if self.backEnd.xpsFile:
                self.filemenu.entryconfig("Сохранить как txt", state='normal')
            else:
                self.filemenu.entryconfig("Сохранить как txt", state='disable')
            if self.backEnd.dirTxtPath:
            #Сохранить каталог xps
                self.filemenu.entryconfig([5], state='normal')
            else:
                self.filemenu.entryconfig([5], state='disable')
    #       Закрытие пунктов меню изходя из прав доступа
            if self.backEnd.permission.sudoCanRun:
                #Закрыть пункты меню "Система" врежиме ограниченного функционала
                if not self.backEnd.vipnet.installed:
                    self.mainmenu.entryconfig("ViPNet", state='disable')
                    self.filemenu.entryconfig("Открыть dst", state='disable')
                if self.backEnd.vipnet.installed:
                    self.filemenu.entryconfig("Открыть dst", state='normal')
                # self.sysmenu.entryconfig("Информация для паспорта", state='normal')
                # self.sysmenu.entryconfig("Информация системная", state='normal')
                    self.mainmenu.entryconfig("ViPNet", state='normal')
                if self.backEnd.sysinfo.lshwInstalled:
                    self.sysmenu.entryconfig("Информация системная",state='normal')
                else:
                    self.sysmenu.entryconfig("Информация системная", state='disable')
            else:
                self.filemenu.entryconfig("Открыть dst", state='disable')
                self.sysmenu.entryconfig("Информация для паспорта", state='disable')
                self.sysmenu.entryconfig("Информация системная", state='disable')
                self.mainmenu.entryconfig("ViPNet", state='disable')
            # self.sysmenu.entryconfig([2],state='disable') блокирование под номером а не по лейблу


    def refreshText(self):
        '''
        :return:
        '''
        logger.info('Разблокирование текствого поля.')
        self.xpsText.config(state='normal')
        logger.info('Очистка текствого поля.')
        self.xpsText.delete("1.0", END)
        if self.backEnd.xpsFile:
            xps = ReaderXPS(self.backEnd.xpsFile)
            self.xpsText.insert("1.0", xps.readXPSFirstPage())
        else:
            logger.warning('Нет открытого xps-файла. Нет текста. Поле оставляю пустым.')
        logger.info('Блокирование текствого поля.')
        self.xpsText.config(state='disable')

    def refreshStatusBar(self):
        '''
        1.хпс-файл
        2.дст-файл
        *3.определённый пароль и его передача в буфер обмена
        *4.возможность установки ключа из текущего запуска программы
        :return:
        '''
        self.statusBar.config(text='')
        if self.backEnd.xpsFile:
            status="Открыт xps файл: "+str(self.backEnd.xpsFile)
            readXPS=ReaderXPS(self.backEnd.xpsFile).getPasswd()
            if self.backEnd.dirTxtPath:
                status += ' Открыт каталог xps-документов.'
            # print(readXPS.getPasswd())
            # Передать пароль в буфер обмена
            status += "\nОпределён пароль"
            try:
                self.clipboard_clear()
                self.clipboard_append(readXPS)
                status+= ' и передан в буфер обмена'
            except BaseException as error:
                logger.error(f'Возникла ошибка передачи в буфер обмена: {error}')
            status+=': '+readXPS
        else:
            status='Файл xps не открыт.'
            if self.backEnd.dirTxtPath:
                status += ' Открыт каталог xps-документов:'+self.backEnd.dirTxtPath+'.'
            status+='\nПароль отсутствует.'

        status += '\n'

        if self.backEnd.dstFile:
            status+="Открыт dst файл: "+str(self.backEnd.dstFile)
        else:
            status+='dst файл не открыт'
        status += '\n'
        # В зависимости от прав и наличия клиента выдать сообщение
        if self.backEnd.permission.sudoCanRun:
            #Выяснить судьбу випнет-клиента
            #status += "Проверка состояния клиента"
            if self.backEnd.vipnet.installed:
                    #status += "Удачное обращение к ViPNet"
                status += "ViPNet-клиент установлен. "
                if self.backEnd.vipnet.error:
                    status += "Ошибка при обращении к ViPNet. "
                else:
                    pass
                if self.backEnd.vipnet.installedKey:
                    status += "В системе имеется установленный ключ."
                else:
                    pass
            else:
                    status += "ViPNet-клиент не установлен. "

        else:
            status += "Текущие права исключают возможность системных запросов. Блокировка элементов меню."
        # else:
        #     status += 'dst файл не открыт'
        self.statusBar.config(text=status)


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
        #if self.backEnd.vipnet.error:
       #     message+='Рекомендую переустановить клиент.'
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
        self.refreshText()
        self.refreshStatusBar()
        self.refreshMenu()





        # =============Открытие документа и каталога
    def openXPSFile(self,dirPath=False):
        '''
        Реализовать преход на полную обработку с backEnd
        :param dirPath:
        :return:
        '''
        logger.info('Открытие файла xps')
        fTypes = [('Файлы xps', '.xps')]#, ('Файлы txt', '.txt')]  # ,('Текстовые файлы','.txt')]
        if dirPath:
            # self.xfilepath = filedialog.askopenfilename(filetypes=fTypes,initialdir=dirPath)
            self.backEnd.setXPS(filedialog.askopenfilename(filetypes=fTypes,initialdir=dirPath))
        else:
            # self.xfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir='/home')
            self.backEnd.setXPS(filedialog.askopenfilename(filetypes=fTypes, initialdir='/home'))
        self.backEnd.setDIR()
        # Передать файл Backend, проверить и обновить данные окна
        #self.backEnd.setXPS(self.xfilepath)
        self.refreshText()
        self.refreshStatusBar()
        # self.backEnd.refresh()
        # print(os.path.abspath(self.xfilepath))
        self.refreshMenu()

    def saveAsTxt(self):
        #Окно с информацией о сохранениии
        #Окно с предупреждением о перезаписи
        logger.info('Сохраним одноимённый txt')
        try:
            xps=ReaderXPS(self.backEnd.xpsFile)
            result=xps.saveAsTxt()
            self.filemenu.entryconfig("Сохранить как txt", state='disable')
        except BaseException as error:
            logger.error(f'При записи txt возникла ошибка: {error}')
            showerror(title='Ошибка',message='При сохранении возникла ошибка:\n'+str(error))
        finally:
            if result == False:
                showerror(title='Ошибка', message='При сохранении возникла ошибка.')
            else:
                showinfo(title='Информация', message='Файл сохранён.')

    def openDSTFile(self,dirPath=False):
        logger.info('Открытие файла dst')
        fTypes = [('Файлы dst', '.dst')]  # , ('Файлы txt', '.txt')]  # ,('Текстовые файлы','.txt')]
        if dirPath:
            # self.dfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir=dirPath)
            self.backEnd.setDST(filedialog.askopenfilename(filetypes=fTypes, initialdir=dirPath))
        else:
            # self.dfilepath = filedialog.askopenfilename(filetypes=fTypes, initialdir='/home')
            self.backEnd.setDST(filedialog.askopenfilename(filetypes=fTypes, initialdir='/home'))
        # self.backEnd.dstFile = self.dfilepath
        self.refreshText()
        self.refreshStatusBar()
        # self.backEnd.refresh()
        # print(os.path.abspath(self.xfilepath))
        self.refreshMenu()

    def openDirxps(self,dirPath=False):
        logger.info('Открытие каталога xps')
        if dirPath:
            # self.xdirpath = filedialog.askdirectory(initialdir=dirPath)
            self.backEnd.setDIR(filedialog.askdirectory(initialdir=dirPath),skipFiles=True)
        else:
            # self.xdirpath = filedialog.askdirectory(initialdir='/home')
            self.backEnd.setDIR(filedialog.askdirectory(initialdir='/home'),skipFiles=True)
        #Проверяем, есть ли xps в даннном каталоге, если есть - включаем пункт меню, -нет вывключаем
        #self.backEnd.setDIR(self.xdirpath)
        massXPS=self.backEnd.checkXPSdir(self.backEnd.dirTxtPath)
        if massXPS:
            self.backEnd.setDIR(dirPath=self.backEnd.dirTxtPath,skipFiles=False)
            showinfo(title='Открытие каталога',message='Найдено '+str(len(massXPS.fileList))+' файлов xps.')
            #Если файлы найдены - обнулить дст и хпс
        else:
            self.backEnd.setDIR()
            showwarning(title='Открытие каталога',message='Файлов xps в указанном каталоге не обнаружено.')
            # Если файлы не найдены - оставить дст и хпс
        self.refreshText()
        self.refreshStatusBar()
        self.refreshMenu()

    def saveDirxps(self):
        logger.info('Сохранение файлов xps каталога в txt')
        try:
            MassXps = Mass_ReaderXPS(self.backEnd.dirTxtPath)
            result = MassXps.writeDirToTXT()
            # self.filemenu.entryconfig([5], state='disable')
        except BaseException as error:
            logger.error(f'При записи  возникла ошибка: {error}')
            showerror(title='Ошибка', message='При сохранении возникла ошибка:\n' + str(error))
        else:
            #self.filemenu.entryconfig([5], state='disable')
            #Сброс каталога
            self.backEnd.setDIR()
        finally:
            if result == False:
                showerror(title='Ошибка', message='При сохранении возникла ошибка.')
            else:
                showinfo(title='Информация', message='Файлы сохранены.')
        self.refreshText()
        self.refreshStatusBar()
        self.refreshMenu()

        # =============Справка и информация
    def htmlHelp(self):
        '''
        выполнить команду открытия html-помощи в браузере
        :return:
        '''
        pass
    def shortHelp(self):
        pass
    def softInfo(self):
        #Реализуем через окно сообщения
        message=TITLE+'\nАвтор: Р.Д.Мотрич\nКонтакт: ascent.mrd@yandex.ru\nМосква, 2025 г.'
        showinfo(title="О программе", message=message)#,icon="lib/ico.png")

        # =============Окно(а) информации паспорт, система, випнет, инструкция

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
        self.xpsFile=self.checkXPSfile(dirPath=self.permission.userDesktop.split()[0])
        self.dstFile=self.checkDSTfile(dirPath=self.permission.userDesktop.split()[0])
        self.dirTxtPath=False
        self.sysinfo=My_System(permis=self.permission)

    # =============Обновление пременных, выдыча данных
    def setXPS(self,filePath=False):
        '''
        !!!Применить проверку
        :param filePath:
        :return:
        '''
        self.xpsFile=filePath

    def setDST(self,filePath=False):
        '''
                !!!Применить проверку
                :param filePath:
                :return:
                '''
        self.dstFile=filePath

    def setDIR(self,dirPath=False, skipFiles=False):
        '''

        :param dirPath: Если просто вызвать, без параметров - обнулит переменную каталога
        :param skipFiles: оставить переменные файлов - True, обнулить - False
        :return:
        '''
        if dirPath:
            self.dirTxtPath=dirPath
            if skipFiles:
                pass
            else:
                self.setXPS()
                self.setDST()
        else:
            self.dirTxtPath = False


    def refresh(self):#,xpsPath=False,dstPath=False,dirPath=False,dirTxtPath=False):
        '''Обновление данных
        #!!!Получить входные параметры
        #if xpsPath+dstPath+dirPath+dirTxtPath==False:
        #TypeError: can only concatenate str (not "bool") to str

        Необходимо обойтись без входных параметров
        задавать переменные методами set.
        а здесь уже разгребать

        xpsPath=путь к xps
        dstPath=путь к dst
        dirTxtPath=каталог xps для перехода в txt
        (по аналогии с __init__)'''
        logger.info("Обновление данных")
        self.permission.refresh()#!ТРЕБУЕТСЯ ЛИ?
        logger.info("Проверка ViPNet клиента")
        self.vipnet.refresh()
        if self.vipnet.error:
            logger.warning('Ошибка обращения к vipnetcient. Рекомендую переустановить.')
        self.sysinfo.updateInfo()
        # передача файлов пароля и dst
        logger.info("Проверка файлов")
        # if dirPath:
        #     #В приоретете
        #     logger.info('Смотрим переданный каталог xps+dst')
        #     pass
        # else:
        #     #смотрим далее xps
        #     if xpsPath:
        #         logger.info('Смотрим переданный xps')
        #     # смотрим далее dst
        #     if dstPath:
        #         logger.info('Смотрим переданный dst')
        #     # смотрим далее каталог для преобразования в дст
        #     if dirTxtPath:
        #         logger.info('Смотрим переданный каталог xps в dst')
        # #если ничего нет падаем по дефолту:
        # if bool(xpsPath)+bool(dstPath)+bool(dirPath)+bool(dirTxtPath)==False:
        #     logger.info('Смотрим рабочий стол')
        #     self.xpsFile = self.checkXPSfile(dirPath=self.permission.userDesktop.split()[0])
        #     self.dstFile = self.checkDSTfile(dirPath=self.permission.userDesktop.split()[0])
        # logger.info('Файлы проверены')

    def refreshText(self):
        '''
        Обновленние информации для текстового поля и панели состояния
        1)подобрать текст из xps
        :return:
        '''
        pass


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

    def checkXPSfile(self,filePath=False,dirPath=False):
        '''Наличие xps'''
        if dirPath:
            return self.searchBySuffix(dirname=dirPath,suff='.xps')
        elif filePath:
            #!!!вернуть filepath, если всё в порядке
            #Временное решение: просто возвращаю filePath
            return filePath
        else:
            return False

    def checkDSTfile(self,filePath=False,dirPath=False):
        '''наличие dst'''
        if dirPath:
            return self.searchBySuffix(dirname=dirPath, suff='.dst')
        elif filePath:
            return filePath
        else:
            return False

    def checkXPSdir(self,dirPath):
        '''Проверка предполагаемой дирректории с xps-сами
        либо возвращает объект Mass_ReaderXPS
        либо False'''
        logger.info(f'Проверка каталога {dirPath} xps')
        xpsToTxt=Mass_ReaderXPS(dirname=dirPath)
        if xpsToTxt.fileList:
            logger.info(f'Возвращаю список документов из каталога {dirPath}')
            xpsToTxt.printFileList()
            self.setDIR(dirPath)
            return xpsToTxt
        else:
            self.setDIR(False)
            logger.warning(f'Документов в каталоге {dirPath} не обнаружено!')
            return False

    # def checkXPSDSTdir(self):
    #     '''В каталоге должен быть и xps и дст
    #     !!!ЛИКВИДИРОВАНО'''
    #     return False

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
                        logger.info(f'Получили файл: {i}')
    #+!!! Получить склейку имени файла и каталога!!!
    #исправлено для раб стла получаем: /home/user/Desktops/Desktop1/xps3_project/temp.xps
                        return os.path.join(dirname,i)
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

'''
    ==============================Модуль режима GUI-интерфейса===========
    ---------------------------------------------------------------------
    Версия 0.3 для xps_astra 0.5

        Модуль реализации графического интерфейса, включаещего в себя:
        *- главное окно программы
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

import logging
# import tkinter
from tkinter import filedialog, ttk, font, Tk, Menu
from module_permissions import My_Permissions
from module_messenger import My_logger
from module_vipnet import My_ViPNet

VERSION = '0.3'
HELP = __doc__
TITLE='xps_astra v0.5'
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
        # -----------Загрузим кастомный шрифт
        try:
            logger.info('Загрузка шрифта')
            custom_font_path = "lib/PT-Astra-Serif_Regular.ttf"
            custom_font = font.Font(family="AstraFont", size=12, name="custom_font")
            custom_font.configure(family=custom_font_path)
            self.option_add('*Font', custom_font)
            logger.info('Шрифт загружен')
        except BaseException as error:
            logger.exception("Неудачная загрузка шрифта")

        # -----------Геометрия главного окна
        self.resizable(width=False, height=False)
        self.geometry("500x300")
        self.title(title)
        # -----------Определим состоянме вспомогательных окон
        # -----------Соберём главное меню
        self.mainmenu = Menu(self)


        # =============Сборка раздела "Файл"
        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Открыть xps")
        self.filemenu.add_command(label="Открыть dst")#, command=self.openDFile)  # ,command=openfile())
        self.filemenu.add_command(label="Открыть каталог (xps+dst)")#,
                                 # command=self.openPDDir)  # tkinter.filedialog.askdirectory())
        self.filemenu.add_command(label="Открыть каталог (все xps)")#, command=self.openTDir)  # ,command=openfile())
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
        self.vipnetmenu.add_command(label="Остановить ViPNet (система)")  # , command=self.openfile)
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

        self.startForMenu()

        # =============Проверка для пунктов меню
    def startForMenu(self):
            # Отключение пунктов меню по "показаниям"
            starter=BackEndWork()


        # =============Окончание сборки главного окна

class BackEndWork():
    '''Класс внутренней работы'''
    def __init__(self):
        logger.info("Проверка разрешений")
        self.permission=My_Permissions()
        logger.info("Проверка ViPNet клиента")
        self.vipnet=My_ViPNet()
        pass


if __name__ == '__main__':
    logger.info(f'GUI_module was loading like program.\nVersion: {VERSION}')
    testWindow=mainWin(title=TITLE)
    testWindow.mainloop()
else:
    logger.info(f'GUI_module was loading like module.\nVersion: {VERSION}')

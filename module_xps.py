'''
    ==============================Модуль распознания XPS==================
    ---------------------------------------------------------------------
    Версия 0.4 для xps_astra 0.4

        Модуль работы с одностраничными xps-файлами, содержащими
    информацию для випнет.
        -
    ---------------------------------------------------------------------
'''
import fitz, re, os.path
from pathlib import Path

class Read_XPS:
    '''
    Класс чтения xps - файла
    '''

    def __init__(self, file_name=''):
        '''
        :param file_name:
            переданный файл для чтения
        self.filePath   -   путь к обрабатываемому файлу
        '''
        self.error = []
        self.read_list = []
        self.filePath = self.checkFile(file_name)
        self.psw = None

    def checkFile(self, file_name):
        '''
        Отвечает за открытие файла, проверку и обработку ошибок
        :param file_name: путь к файлу
        :return:
        '''
        if os.path.isfile(file_name):
            self.show_message(f'Файл {file_name} существует')
            if Path(file_name).suffix=='.xps':
                self.show_message(f'Полный путь к указанному файлу: \n\t {os.path.abspath(file_name)}')
                return os.path.abspath(file_name)
            else:
                self.show_message(f'Файл {file_name} имеет неверное расширение')
                self.error.append('wrong_file_suffix')
                #return False
                return os.path.abspath(file_name)
        else:
            self.show_message(f'Файл {file_name} не существует')
            self.error.append('file_not_exists')
            return False

    def readFirstPage(self):  # , file_name):
        '''
        Читает первую страницу файла self.filePath
        :return:self.read_list
        Возвращает список вычитаных слов
        '''
        if len(self.error) == 0:
            try:
                document = fitz.open(self.filePath)
                self.show_message('Успешное открытие файла для чтения первой страницы')
            except BaseException as error:
                # Добавиь ошибку в self.error
                self.show_message(f'Возникла ошибка {error} на этапе открытия файла')
                self.error.append(error)
                return False
            else:
                pass
            try:
                page = document.load_page(0)
                text = page.get_text()
                self.show_message('Успешное чтение из файла')
                self.read_list = [i for i in text.split()]
                return self.read_list

            except BaseException as error:
                self.show_message(f'Возникла ошибка {error} на этапе чтения файла')
                self.error.append(error)
                return False
            else:
                self.show_message('Завершено чтение файла')
        else:
            self.show_message('Наличие ошибок')
            for i in self.error:
                self.show_message(i)
            self.show_message('Файл не может быть прочтён')
            return False

    def getPasswd(self):
        '''
        Возращает пароль
        Использует модуль re, который отвечает за парсинг
        edtrty[ktdfh
        :return: выявлен пароль
        '''
        # searching=re.compile(r'[\w\.\,\/]', re.S)
        if self.read_list:
            for i in self.read_list[::-1]:
                if re.search(r"[a-z\[\]\,\.\/\`]{12}", i):
                    self.psw = i
                    self.show_message(f'Выявлен пароль: {self.psw}')
                    # self.put_to_clip(i)
                    return i
                else:
                    pass
        else:
            self.show_message('Не предоставлены входные данные для выделения пароля')
            self.error.append('password_parce_error')
            return False

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

    def saveAsTxt(self):
        '''сохраняет в txt-вормате
        '''
        #Если у нас есть файл и нет ошибок
        if len(self.error)==0:
            try:
                #Переименуем
                txtPath,_ =os.path.splitext(self.filePath)
                txtPath=txtPath+'.txt'
                with open(txtPath,'w') as txt:
                    self.show_message('Открыли запись в txt')
                    txt.write(' '.join(self.read_list))
                    return txtPath
            except BaseException as e:
                self.show_message(f'{e}')
                self.error.append('wrong_write_txt')
                return False
            else:
                self.error.append('errors_write_txt')
                return False

    def readTxt(self):
        '''
        Почитаем из txt
        :return:
        '''
        #не кинуло ли нам, что файл не существует
        if 'file_not_exists' in self.error:
            #нет тела - нет дела
            self.error.append('txt_not_exists')
            return False
            # pass
        elif os.path.splitext(self.filePath)[-1]=='.txt':
            #если txt - выделим строку и вернём пароль
            self.show_message('Хотябы расширение норм')
            try:
                with open(self.filePath,'r') as txt:
                    self.read_list=txt.readline().split()
            except BaseException as e:
                self.show_message(f'{e}')
            else:
                pass
        else:
            #что может быть хуже?
            pass
    def __str__(self):
        return str(' '.join(self.read_list))


if __name__ == '__main__':
    print(__doc__)
    print('\n ОРГАНИЗОВАТЬ РАБОТУ С ФАЙЛАМИ TXT!!!')
    doctest = Read_XPS('xps.xps')
    #doctest = Read_XPS('/home/roma/Desktop/xps/xps_astra03.py')
    print(doctest.readFirstPage())
    doctest.getPasswd()
    #doctest.saveAsTxt()
    txtTest=Read_XPS('xps.txt')
    txtTest.readTxt()
    txtTest.getPasswd()
    #Проверить создание объекта, просто подсунуть ему парольную фразу + Всё и получить пароль

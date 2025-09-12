'''
    ==============================Модуль распознания XPS==================
    ---------------------------------------------------------------------
    Версия 0.4.1 для xps_astra 0.5

        Модуль работы с одностраничными xps и txt файлами, содержащими
    информацию для випнет.
        - выделяет пароль из известного типа (может не универсален)
        - сохраняет xps в txt (только первая страница)
        - обработка дирректории с фалами-паролями

    0.4.1
        - введение логирования
        - скрытие лишних показов

        Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г.
    ---------------------------------------------------------------------
'''

import fitz, re, os.path
from pathlib import Path
from module_messenger import My_logger

XPS = '.xps'
TXT = '.txt'
VERSION = '0.4.1'
HELP = __doc__
logger=My_logger


class ReaderXPS:
    '''
    Класс работы с файлами-паролями
    Атрибуты:
        filePath
        fileSufx
        readList
        psw
    Методы:
        __init__
        checkFile
        readFile
        readXPSFirstPage
        readTXT
        getPasswd
        saveAsTxt
    '''

    def __init__(self, file_name=False):
        '''
        :param file_name:
            переданный файл для чтения
        self.filePath   -   путь к обрабатываемому файлу
        '''
        if file_name:
            self.filePath = self.checkFile(file_name)
            if self.filePath:
                self.fileSufx = Path(self.filePath).suffix
            else:
                self.fileSufx = False
        else:
            self.filePath = False
            self.fileSufx = False
        if self.filePath:
            self.readList = self.readFile()
        else:
            self.readList = False
        self.psw = None

    def checkFile(self, file_name):
        '''
        Отвечает за проверку файла
        :param file_name: путь к файлу
        :return:
        '''
        if os.path.isfile(file_name):
            logger.info(f'Файл {file_name} существует')
            if Path(file_name).suffix == '.xps':
                logger.info(f'Полный путь к указанному файлу: \n\t {os.path.abspath(file_name)}')
                return os.path.abspath(file_name)
            elif Path(file_name).suffix == '.txt':
                logger.info(f'Полный путь к указанному файлу: \n\t {os.path.abspath(file_name)}')
                return os.path.abspath(file_name)
            else:
                logger.warning(f'Файл {file_name} имеет неверное расширение')
                # self.error.append('wrong_file_suffix')
                return False
                # return os.path.abspath(file_name)
        else:
            logger.warning(f'Файл {file_name} по указанному пути не существует.\n\tПроверьте путь и имя файла.')
            # self.error.append('file_not_exists')
            return False

    def readFile(self):
        '''Читает предоставленный файл, в зависимости от типа
         txt либо xps, для чего использует txtRead и xpsRead.
         :return Список слов из файла для дальнейшей обработки'''
        # Если файл есть и всё в порядке
        print('Начнем чтение файла')
        if self.filePath:
            # Проверка расширения
            if self.fileSufx == XPS:
                #print('Предоставлен формат XPS.')
                return self.readXPSFirstPage()
            elif self.fileSufx == TXT:
                #print('Предоставлен формат TXT.')
                return self.readTXT()
            else:
                logger.warning('Ошибка: Недопустимое расширение файла.')
                return False
        else:
            return False

    def readXPSFirstPage(self):  # , file_name):
        '''
        Читает первую страницу файла self.filePath
        :return:self.read_list
        Возвращает список вычитаных слов
        '''
        # if len(self.error) == 0:
        try:
            document = fitz.open(self.filePath)
            #print('Успешное открытие файла для чтения первой страницы')
        except BaseException as error:
            # Добавиь ошибку в self.error
            logger.error(f'Возникла ошибка {error} на этапе открытия файла')
            # self.error.append(error)
            return False
        else:
            pass
        try:
            page = document.load_page(0)
            text = page.get_text()
            # print('Успешное чтение из файла')
            # self.read_list = [i for i in text.split()]
            outList = [i for i in text.split()]
            if __name__ == '__main__':
                print(f'Прочитано: {outList}')
            if len(outList):
                return outList  # [i for i in text.split()]#self.read_list
            else:
                logger.warning('Файл пуст(нет текстовой информации).')
                return False
        except BaseException as error:
            logger.error(f'Возникла ошибка {error} на этапе чтения файла')
            # self.error.append(error)
            return False
        else:
            print('Завершено чтение файла')

    def readTXT(self):
        try:
            with open(self.filePath, 'r') as document:
                try:
                    text = document.read()
                    #print('Успешное чтение из файла')
                    outList = [i for i in text.split()]
                    if __name__=='__main__':
                        print(f'Прочитано: {outList}')
                    if len(outList):
                        return outList  # [i for i in text.split()]#self.read_list
                    else:
                        logger.warning('Файл пуст(нет текстовой информации).')
                        return False
                except BaseException as error:
                    logger.error(f'Возникла ошибка {error} на этапе чтения файла')
                    # self.error.append(error)
                    return False
                else:
                    logger.info('Завершено чтение файла')
        except BaseException as error:
            # Добавиь ошибку в self.error
            logger.error(f'Возникла ошибка {error} на этапе открытия файла')
            # self.error.append(error)
            return False
        else:
            pass

    def getPasswd(self):
        '''
        Возращает пароль
        Использует модуль re, который отвечает за парсинг
        edtrty[ktdfh
        :return: выявлен пароль
        '''
        # searching=re.compile(r'[\w\.\,\/]', re.S)
        if __name__=='__main__':
            print(f'СОДЕРЖИМОЕ:\n\t{" ".join(self.readList)}')
        if self.readList:
            for i in self.readList[::-1]:
                if re.search(r"[a-z\[\]\,\.\/\;\'\\`]{12}", i):
                    self.psw = i
                    if __name__=='__main__':
                        print(f'Выявлен пароль:\n\t{self.psw}')
                    # self.put_to_clip(i)
                    return str(i)
                else:
                    pass
        else:
            logger.warning('Не предоставлены входные данные для выделения пароля')
            # self.error.append('password_parce_error')
            return False

    def saveAsTxt(self):
        '''сохраняет в txt-вормате
        '''
        # Если у нас есть файл и нет ошибок
        # if len(self.error) == 0:
        logger.info(f'Начало записи txt из {self.filePath}')
        try:
            # Переименуем
            txtPath = self.filePath  # Path(self.filePath).name
            txtPath = Path(txtPath).with_suffix('.txt')
            logger.info(f'Новый путь: {txtPath}')
            if os.path.isfile(txtPath):
                print('ВНИМАНИЕ! ФАЙЛ СУЩЕСТВУЕТ! ФАЙЛ БУДЕТ ПЕРЕЗАПИСАН!')
            if self.filePath:
                with open(txtPath, 'w') as txt:
                    #print(f'Открыли запись в txt {txtPath}')
                    # strWrite=" ".join(self.read_list)
                    # print(f'ДЛЯ ЗАПИСИ: {strWrite}')
                    txt.write(' '.join(self.readList))
                    logger.info(f'Запись в txt {txtPath} завершена.')
                    return txtPath
            else:
                logger.warning('Нет данных для записи, файл не будет записан.')
                return False
        except BaseException as e:
            logger.error(f'Ошибка записи txt:\n\t{e}')
            # self.error.append('wrong_write_txt')
            return False
        else:
            # self.error.append('errors_write_txt')
            # return False
            pass


class Mass_ReaderXPS:
    '''
    Класс для поточного чтения в указанной папке
    Переменные:
        dirName
        fileList
        dataDict
    Методы:
        __init__
        checkDir
        getXpsFileList
        dataXPSdict
        printFileLis
        printDataList
        writeDirToTXT
    '''

    def __init__(self, dirname='', fulldada=False):
        '''
        :param dirname: Путь к обрабатываемому каталогу
        :param fulldada: Есть ли необходимость получать словарь данных
                            без него нельзя будет записать txt
        '''
        self.dirName = self.checkDir(dirname)
        #print(self.dirName)
        self.fileList = self.getXpsFileList()
        if fulldada:
            self.dataDict = self.dataXPSdict()
        else:
            self.dataDict = False

    def checkDir(self, dirname):
        '''
        Проверка дирректории
        Возврат абсолютного имени
        '''
        if os.path.isdir(dirname):
            print(f'Каталог {dirname} существует')
            return os.path.abspath(dirname)
        else:
            print(f'Каталог {dirname} по указанному пути не существует.\n\tПроверьте путь.')
            # self.error.append('file_not_exists')
            return False

    def getXpsFileList(self):
        '''
        Получим список xps файлов в каталоге
        '''
        out = []
        if self.dirName:
            print(f'Получим список файлов с расширением xps.\t{self.dirName}')
            filelist = os.listdir(self.dirName)
            # print(filelist)
            for i in filelist:
                if Path(i).suffix == XPS:
                    # print(os.path.join(self.dirName,i))
                    out.append(os.path.join(self.dirName,i))
            if len(out):
                print('Файлы xps обнаружены')
                return out
            else:
                print('Файлы xps не обнаружены')
                return False
        else:
            print(f'Не могу получить список файлов.\n\tСостояние каталога: {self.dirName}')
            return False

    def dataXPSdict(self):
        '''
        Получим словарь прочтённых данных
        :return:
        '''
        out = {}
        print('Построение словоря прочтённых данных')
        if self.fileList:
            for i in self.fileList:
                out.update({Path(i).name: [i, ReaderXPS(i).readXPSFirstPage(), ReaderXPS(i).getPasswd()]})
            # print(out)
            return out
        else:
            print(
                f'Не могу получить список файлов.\n\tСостояние каталога: {self.dirName}\n\tСостояние списка: {self.fileList}')
            return False

    def printFileList(self):  # ,filelist=[]):
        '''
        Печать списка файлов
        :return:
        '''
        if self.dirName:
            if self.fileList:
                for i in self.fileList:
                    print(i)

    def printDataList(self, showfull=False):
        '''
        Печать словаря данных (только пароль или  целиком)
        :param showfull:
        :return:
        '''
        if self.dataDict:
            for name, data in self.dataDict.items():
                if showfull:
                    print(f'{name}\tПароль: {data[2]}\n\t{data[1]}')
                else:
                    print(f'{name}\tПароль: {data[2]}')
            return True
        else:
            print('Нет словаря данных для вывода.')
            return False

    def writeDirToTXT(self):
        '''
        Запись полученного списка в txt
        :return:
        '''
        if self.fileList:
            try:
                for i in self.fileList:
                    ReaderXPS(i).saveAsTxt()
            except BaseException as error:
                print(f'При записи каталога возникла ошибка:\n\t{error}')
                return False
            print('Запись каталога завершена.')
            return True
        else:
            print(
                f'Не могу получить список файлов.\n\tСостояние каталога: {self.dirName}\n\tСостояние списка: {self.fileList}')
            return False


if __name__ == '__main__':
    logger.info(f'module_xps was loading like program.\nVersion: {VERSION}')
    print(__doc__)
    # print('\n ОРГАНИЗОВАТЬ РАБОТУ С ФАЙЛАМИ TXT!!!')
    # doctest = ReaderXPS('2586 Linux.xps')
    # doctest = ReaderXPS('2586 Linux2.xps')
    # doctest = ReaderXPS('2586 Linux2_Empty.xps')
    # doctest = ReaderXPS('/home/roma/Desktop/xps/xps_astra03.py')
    # doctest = ReaderXPS('2586 test 1.xps')
    # doctest = ReaderXPS('/home/user/Desktop/xps3_project/test_2.xps')
    # doctest = ReaderXPS('test3.xps')
    # doctest = ReaderXPS('test  4.xps')
    # doctest = ReaderXPS('test5.xps')
    # doctest = ReaderXPS('test6.xps')
    # doctest = ReaderXPS('test7.xps')
    # doctest = ReaderXPS('test8.xps')
    # # doctest = ReaderXPS('test9.xps')
    # doctest = ReaderXPS('/home/user/Desktop/xps3_project/test10.xps')
    # doctest.getPasswd()
    # # doctest.saveAsTxt()
    # txtTest=Read_XPS('xps.txt')
    # txtTest.readTxt()
    # txtTest.getPasswd()
    # Проверить создание объекта, просто подсунуть ему парольную фразу + Всё и получить пароль

    massDocTest=Mass_ReaderXPS('/home/user/Desktop',fulldada=True)
    # # massDocTest = Mass_ReaderXPS('/home/user/Desktop/xps3_projecd',fulldada=True)
    # # massDocTest = Mass_ReaderXPS('/home/user/Desktop/xps3_project/build',fulldada=True)
    # # massDocTest.printDataList(showfull=True)#dataXPSdict()

    # massDocTest.printDataList()
    # massDocTest.writeDirToTXT()

    # doctest = ReaderXPS('2586 Linux.txt')
    # doctest = ReaderXPS('2586 Linux2_Empty.txt')
    # doctest = ReaderXPS('/home/roma/Desktop/xps/xps_astra03.py')
    # doctest = ReaderXPS('/home/user/Desktop/xps3_project/2586 test 1.xps')
    #doctest = ReaderXPS('test_2.txt')
    # doctest = Read_XPS('test3.xps')
    # doctest = Read_XPS('test  4.xps')
    # doctest = Read_XPS('test5.xps')
    # doctest = Read_XPS('test6.xps')
    # doctest = Read_XPS('test7.xps')
    # doctest = Read_XPS('test8.xps')
    # # doctest = Read_XPS('test9.xps')
    doctest = ReaderXPS(massDocTest.fileList[0])
    doctest.getPasswd()
else:
    logger.info(f'module_xps was loading like module.\nVersion: {VERSION}')

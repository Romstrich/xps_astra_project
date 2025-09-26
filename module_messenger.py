'''
    ==============================Модуль вывода сообщений================
    ---------------------------------------------------------------------
        *Модуль вывода сообщений в соответствующее место назначения
        *Для каждого места ( панель, консоль, строка состояния и т.д.
    *будет применяться свой месенджер
        Обеспечение логирования программы
    ---------------------------------------------------------------------
'''
VERSION="0.1"
import logging

My_logger=logging.getLogger()
My_logger.setLevel(logging.INFO)
streamLog=logging.StreamHandler()
streamLog.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
My_logger.addHandler(streamLog)

class Messenger:
    '''
    принимает объект отправки (вывода сообщений)
    если объекта нет: в терминал.
    target: наш объект
    '''

    def __init__(self,target='tty'):
        '''
        :param target: объект для вывода текста
        '''
        self.target = target

    def __call__(self, *args, **kwargs):
        '''
        При вызове будет выводить сообщения в цель
        :param args:
        :param kwargs:
        :return:
        '''
        if args:
            for i in args:
                print(i)
        else:
            print('Сообщений не поступало')

if __name__ == '__main__':
    print('Идет проверка модуля messanger')
    message=Messenger()
    # message('Куку','ты это видишь?','Интересно, кака работает эта штука')
    message()
else:
    My_logger.info(f'module_messanger was loading like module.\nVersion: {VERSION}')
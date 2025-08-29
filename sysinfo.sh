#!/bin/bash
#проверка на административный запуск
if [ "$EUID" -ne 0 ]
  then echo "Запустите команду от имени root"

  else
#проверка наличия команд и утилит
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#В АСТРЕ НЕТ LSHW!!!
#ПРЕДЛОЖИ УСТАНОВИТЬ!!!!
if ! type "lshw" > /dev/null 2>&1; then
  echo -e "Нет утилиты lshw.\nПопытка установки..."
  apt update;
  apt install lshw
fi
#выполнение инструкций согласно списка


if ! type "lshw" > /dev/null 2>&1; then
#Производитель
 echo -e "Нет утилиты lshw.\nКраткая сводка по системе:"
else
echo "Информация о производителе:"
lshw  | head -n 8
#Процессор
echo "Информация о процессоре:"
lshw -class cpu
#Память
echo "Информация об оперативной памяти:"
lshw -short -class memory
#lshw -class memory
#Графика
echo "Информация о графических процессорах:"
lshw -short -class display
#Сеть
echo "Информация о сетевых интефейсах:"
lshw -short -class network
#Диски
echo "Информация о дисковых устройствах:"
lshw -class disk
fi
#Ядро операционной системы
echo "Информация о ядре операционной системы:"
echo "Версия ядра:"
uname -r
echo "Сборка:"
uname -v
echo "Ахитектура:"
uname -m
#Список пользователей и групп, в которые они входят
echo "Список пользователей:"
awk -F: '$3 >= 1000 {print $1}' /etc/passwd  | grep -v nobody
#информация об авторе

fi

echo  "Мотрич Р.Д. ascent.mrd@yandex.ru 2025 г."
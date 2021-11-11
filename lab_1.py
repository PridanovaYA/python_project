import zipfile
import os
import hashlib
import re
import requests


# 1
# Программно разархивировать архив в выбранную диркторию

test_zip = zipfile.ZipFile('D:\\test.zip')

test_zip_files = test_zip.namelist()

print(test_zip_files)

test_zip.extractall('D:\\LAB_1')

test_zip.close()

# 2
# Найти в директории все файлы формата txt,
# получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран (имя файла и хеш).

txt_files = []
for dirpath, dirnames, filenames in os.walk('.'):
    destination = 'D:\\LAB_1'
    for filename in filenames:  # перебор
        if filename.endswith('.txt'):
            txt_files.append(destination + (os.path.join(dirpath, filename))[1::])

for txt_file in txt_files:
    target_file_data = open(txt_file, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()
    print(txt_file)
    print(result)

# 3
# Найти файл, MD5 хеш которого равен следующему значению:
# 4636f9ae9fef12ebd56cd39586d33cfb. Прочитать из файла ссылку на веб-страницу.
# Нужный файл имеет расширение .sh
# Xэши считаем так:
# target_file_data = open(file,'rb').read()
# result = hashlib.md5(target_file_data).hexdigest()

for dirpath, dirnames, filenames in os.walk('.'):
    destination = 'D:\\LAB_1'
    for filename in filenames:
        p = destination + (os.path.join(dirpath, filename))
        target_file_data = open(p, 'rb').read()
        result = hashlib.md5(target_file_data).hexdigest()
        if result == '4636f9ae9fef12ebd56cd39586d33cfb':
            print('--------------------------------------------')
            print(p)
            print(filename)
            f = open(p, 'r')
            target_file = f.read()
            print(f.read(1000))


# 4
# Получить содержимое веб-страницы (по ссылке из задания 3).
# При помощи регулярных выражений и методов работы со строками распарсить содержимое HTML страницы
# и сохранить информацию из таблицы в словарь.

r = requests.get(target_file)
result_dct = {} # словарь для записи содержимого таблицы
counter = 0
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text) # Получение списка строк таблицы

for line in lines:
    if counter == 0: # извлечение заголовков таблицы
        headers = re.sub("<.*?>", " ", line) # Удаление тегов
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers) # Извлечение списка заголовков
    temp = re.sub("<.*?>", ';', line)
    temp = re.sub(r'\(.*?\)', '', temp)
    temp = re.sub(r'\xa0', '', temp)
    temp = re.sub(r'\s', ';', temp)
    temp = re.sub(r'\;;+', '!', temp)
    temp = re.sub(';', ' ', temp)
    temp = re.sub(r'^\!+|\s+$', '', temp)
    temp = re.sub(r'^\W+', '', temp)
    temp = re.sub(r'^\!', '', temp)
    temp = re.sub('_', '-1', temp)
    temp = re.sub(r'[*]', '', temp)
    tmp_split = re.split(r'\!', temp)

    if tmp_split != headers:
        country_name = tmp_split[0]
        result_dct[country_name] = [0, 0, 0, 0]
        for i in range(4):
            result_dct[country_name][i] = int(tmp_split[i+1])
    counter += 1


# 5
# Сохранить содержимое таблицы в новый файл, где каждая
# новая строка таблицы сохраняется с новой строки, а отдельные столбцы отделены символом ";".

with open('res.csv', 'w') as output:
    output.write(";")  # for office
    for i in headers:
        output.write(i)
        output.write(";")
    for key in result_dct.keys():
        output.write("\n")
        output.write(key + ';' + str(result_dct[key][0]) + ";" + str(result_dct[key][1]) + ";" + str(result_dct[key][2]) + ";" + str(result_dct[key][3]))

#output.close()

# 6
# Предоставить возможность пользователю при помощи метода input() получить информацию об отдельных элементах таблицы.

while True:
    print("Enter country name or 1 to exit")
    user_input = input()
    if user_input == "1":
        break
    print("Sick"+"\t\t"+"Died"+"\t\t"+"Cured"+"\t\t"+"Active cases")
    print(result_dct[user_input][0], "\t", result_dct[user_input][1], "\t", result_dct[user_input][2], "\t\t", result_dct[user_input][3])


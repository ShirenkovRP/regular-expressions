import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
#  1.поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
#  В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О
new_list = []
for i in contacts_list:
    interim_list = []
    for position in i[:3]:
        if position != "":
            for cell_str in position.split(" "):
                interim_list.append(cell_str)
    if len(interim_list) < 3:
        interim_list.append("")
    interim_list.extend(i[3:7])
    new_list.append(interim_list)

#  2.привести все телефоны в формат +7(999)999-99-99.
#  Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
for i in new_list:
    pattern = re.compile(r"(\+*7|8)\s*\-*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})\s*\(*(доб.)*\s*(\d+)*\)*")
    i[5] = pattern.sub(r'+7(\2)\3-\4-\5 \6\7', i[5]).rstrip()

#  3.объединить все дублирующиеся записи о человеке в одну
final_list = []
while len(new_list) != 0:
    position_list = new_list.pop(0)
    if position_list:
        for i in new_list:
            if position_list[0:2] == i[0:2]:
                interim_list = []
                while len(position_list) != 0 and len(i) != 0:
                    a = position_list.pop(0)
                    b = i.pop(0)
                    if a != b:
                        interim_list.append(a + b)
                    else:
                        interim_list.append(a)
                position_list = interim_list
        final_list.append(position_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',', lineterminator="\n")
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(final_list)

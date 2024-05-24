# Это скрипт "schedule_get" - парсер школьного расписания
import requests
import json
import datetime
import os
import time
file_json_name = 'schedule' # .json file name
file = open(f'{file_json_name}.txt', 'w', encoding='utf-8')
file.close()
file = None
def printC(*args):
    print("[Callback] (from ScheduleGet)", *args)

# js_get_link() - gets link to schedule JSON
def js_get_link():
    start = time.time()
    printC('Начат процесс парсинга.'.upper())
    site = requests.get('https://lyceum.nstu.ru/rasp/m.schedule.html').content # get site code in bytes
    file = open('site_code.html', 'wb') # open .html to write site code
    dir_path = os.path.abspath(__file__)
    dir_path = dir_path[0:len(dir_path) - 16]
    files_list = os.listdir(dir_path)
    if not('old_link.txt' in files_list):
        oldl = open(os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')+'/'+'old_link.txt','w')
        oldl.write('.')
        oldl.close()
    
    file.write(site) # write site code
    file.close() # close .html
    file = open('site_code.html', 'r', encoding='UTF-8') # open encoded to UTF-8 site code
    rd = file.readline() # test-read
    site_enco = '' # var that will keep .json list name
    for i in range(16):
        rd = file.readline() # skipping some lines
    site_enco += rd # adding necessary site code line
    js_name = site_enco[site_enco.find('c=')+3:site_enco.find('.js"')+3] # find .json name
    js_link = (f'https://lyceum.nstu.ru/rasp/{js_name}') # make link
    end = time.time()
    printC(f'Время получения ссылки: {end-start} секунд/ы/а')
    return js_link # return link

# js_download downloads JSON, save's it with name f'{file_json_name}.txt' and returns Python dict if return_dict = True 
def js_sure_download(filename = file_json_name):
    printC('Принудительная загрузка JSON начата.'.upper())
    start = time.time()
    get_js = requests.get(js_get_link()).text # get .json in bytes
    file = open(f'{filename}.txt', 'r+', encoding='utf-8') # open f'{filename}.txt' to save json
    file.truncate(0)
    if '\n'.join(list(file)) != get_js:
        file.write(get_js) # write JSON
        file.close() # close file
    file = open(f'{filename}.txt', 'r', encoding = 'UTF-8') # open f'{filename}.txt' to read encoded json
    js_list = list(file)[8] # adding necessary lines (schedule, teachers, etc)
    js_list = js_list[:len(js_list)-2] # delete non-necessary '];'
    js_list_dict = json.loads(js_list.replace("'F'", 'False').replace('чтениечтение', 'чтение').replace('спотзал', 'спортзал').replace('Инженерная графика', 'Инж. графика').replace('математической логики', 'мат. логики')) # convert string JSON to Python dict
    printC('Успешно загружен JSON'.upper())
    end = time.time()
    printC(f'Время загрузки JSON: {end-start} секунд/ы/а')
    return js_list_dict # return Python dict
js_download = js_sure_download
# get_everything - gives partitioned Python dict 
def get_everything():
    dictionary = js_download() # get Python dict
    schedule = dictionary['CLASS_SCHEDULE'] # get schedule info
    teachers = dictionary['TEACHERS'] # get teachers info
    classes = dictionary['CLASSES'] # get classes info
    cabinets = dictionary['ROOMS'] # get cabinets info
    subjects = dictionary['SUBJECTS'] # get subjects info
    return [dictionary, schedule, teachers, classes, cabinets, subjects] # return everything

# everything_class - all school class's info in a current week
def everything_class(class_name):
    dictionary = get_everything()
    schedule = dictionary[1]
    schedule = schedule[list(schedule.keys())[0]][class_name]
    keys = [[],[],[],[],[],[],[]]
    lesson_arrangement = [[],[],[],[],[],[],[]]
    for i in range(1, 7):
        for j in range(1, 14):
            key_gen = str((i * 100) + (j))
            if schedule.get(key_gen) != None:
                keys[i].append(key_gen)
                lesson_arrangement[i].append(j)
    keys.pop(0)
    lesson_arrangement.pop(0)
    return [dictionary, schedule, keys, lesson_arrangement]

# organize() organizes everything_class() output
def organize(class_name):
    printC('Начат процесс организации информации из JSON')
    start = time.time()
    inp = everything_class(class_name)
    dictionary = inp[0]
    schedule = inp[1]
    schedule_keys = inp[2]
    lesson_arr = inp[3]
    subjs_info = [[],[],[],[],[],[]]
    teach_info = [[],[],[],[],[],[]]
    cabnt_info = [[],[],[],[],[],[]]
    for i in range(len(schedule_keys)):
        for j in schedule_keys[i]:
            subjs_info[i].append(schedule[j]['s'])
            teach_info[i].append(schedule[j]['t'])
            cabnt_info[i].append(schedule[j]['r'])
    end = time.time()
    printC(f'Время организирования JSON: {end-start} секунд/ы/а')
    return [subjs_info, teach_info, cabnt_info, lesson_arr, inp, schedule_keys, dictionary]

# translate() translates organize() output into Russian
def translate(class_name):
    start = time.time()
    inp = organize(class_name)
    subjs_info = inp[0]
    teach_info = inp[1]
    cabnt_info = inp[2]
    lesson_arr = inp[3]
    dictionary = inp[-1][0]
    schedule_keys = inp[5]
    teach_dict = dictionary['TEACHERS']
    cabnt_dict = dictionary['ROOMS']
    subjs_dict = dictionary['SUBJECTS']
    text = [[],[],[],[],[],[]]
    for i in range(len(schedule_keys)):
        for j in range(len(schedule_keys[i])):
            try:
                for k in range(len(teach_info[i][j])):
                    subjs_info[i][j][k] = str(subjs_dict[subjs_info[i][j][k]]).replace('[', '').replace(']', '').replace("'", '"')
                    teach_info[i][j][k] = str(teach_dict[teach_info[i][j][k]]).replace('[', '').replace(']', '').replace("'", '"')
                    cabnt_info[i][j][k] = str(cabnt_dict[cabnt_info[i][j][k]]).replace('[', '').replace(']', '').replace("'", '"')
                text[i].append(f'        {lesson_arr[i][j]}й урок:\n предмет/ы {subjs_info[i][j]},\n учитель/я {teach_info[i][j]},\n кабинет – {cabnt_info[i][j]}. \n\n\n'.replace('[', '').replace(']', ''))
            except:
                text[i].append('Не удалось загрузить расписание.')
    if len(text[5]) == 0:
        del text[5]
    end = time.time()
    printC(f'Время перевода: {end-start} секунд/ы/а')
    return [subjs_info, teach_info, cabnt_info, text]
classes_list = js_download()['CLASSES']
def prepare_to_convert(class_name):
    inp = ''
    flag = True
    for i in range(len(class_name)):
        if not(class_name[i] in ['а', 'б', 'в', 'г', '-', '1','2','3','4','5','6','7', '8', '9', '0']):
            continue
        elif class_name[i] == '—':
            inp += '-'
        elif class_name.isdigit() == True and not('0') in class_name:
            if len(class_name) == 1:
                inp = '00' + class_name
                break
            elif len(class_name) == 2:
                inp = '0' + class_name
                break
            elif len(class_name) != 1 and len(class_name) != 2:
                flag = False
                break
        else:
            inp += class_name[i]
    if flag == True:
        return inp.lower()
    else:
        return '000'
def class_name_converter(class_name, db = True):
    dictionary = classes_list
    if db == True and class_name.isdigit() == True:
        return class_name
    elif db == False and class_name.isdigit() == True:
        return dictionary[class_name]
    elif db == False and class_name.isdigit() == False:
        return class_name
    else:
        dictionary = {v: k for k, v in dictionary.items()}
        return dictionary[class_name.lower()]

def cls_find(course):
    dicti = list(js_download()['CLASSES'].values())
    lst = []
    if course == '11':
        for i in range(len(dicti)):
            if course in dicti[i]:
                lst.append(dicti[i])        
        return lst
    else:
        for i in range(len(dicti)):
            if course in dicti[i] and not('-' in dicti[i]):
                lst.append(dicti[i])        
        return lst

def find_available_classes_by_course(course):
    dictionary = js_download()
    class_list = dictionary['CLASSES']
    class_list = {v: k for k, v in class_list.items()}
    val = list(class_list)
    av_cl = []
    for i in range(len(val)):
        if val[i].startswith(course) == True and course == '11':
            av_cl.append(val[i])
        elif val[i].startswith(course) == True and course == '1' and not('-' in val[i]):
            av_cl.append(val[i])
        elif val[i].startswith(course) == True and course.startswith('1') == False:
            av_cl.append(val[i])
        elif val[i].startswith(course) == True and course.startswith('10') == True:
            av_cl.append(val[i])
    return av_cl

def all_translated_exchanges():
    dictionary = js_download()
    teach_dict = dictionary['TEACHERS']
    cabnt_dict = dictionary['ROOMS']
    subjs_dict = dictionary['SUBJECTS']
    exchanges = dictionary['CLASS_EXCHANGE']
    cls_list = list(exchanges.keys())
    cls_with_exchanges = cls_list 
    s_temp = []
    txt = dict.fromkeys(cls_list)
    for i in range(len(cls_list)):
        for j in exchanges[cls_list[i]]:
            for k in exchanges[cls_list[i]][j]:
                if exchanges[cls_list[i]][j][k]['s'][0].isnumeric() == False:
                    c_n = class_name_converter(cls_list[i], db = False)
                    txt[cls_list[i]] = f'{j}: изменения на {k}-й урок: урок отменен'
                else:
                    #c_n = class_name_converter(cls_list[i], db = False)
                    sj = subjs_dict[exchanges[cls_list[i]][j][k]['s'][0]]
                    tch = teach_dict[exchanges[cls_list[i]][j][k]['t'][0]]
                    cb = cabnt_dict[exchanges[cls_list[i]][j][k]['r'][0]]
                    txt[cls_list[i]] = str(j)+' '+' класс: изменения на '+str(k)+'-й урок: предмет '+str(sj)+', учитель: '+str(tch)+', кабинет: '+ str(cb)
    return exchanges, txt, cls_with_exchanges 
def all_classes():
    clses = js_download()['CLASSES']
    return list(clses.values())

def check_lesson_time():
    current_time = datetime.datetime.now().strftime('%H:%M')
    curt = datetime.datetime.now().strftime('%H:%M:%S')
    #printC(current_time)
    current_datetime = datetime.datetime.now()
    weekday = current_datetime.weekday()
    if weekday==6:
            return "Сегодня воскресенье."  
    lessons_time = {
        "1": ["8:15", "9:00"],
        "2": ["9:10", "9:55"],
        "3": ["10:15", "11:00"],
        "4": ["11:15", "12:00"],
        "5": ["12:10", "12:55"],
        "6": ["13:05", "13:50"],
        "7": ["14:00", "14:40"],
        "8": ["14:55", "15:35"],
        "9": ["15:50", "16:30"],
        "10": ["16:40", "17:20"],
        "11": ["17:30", "18:10"],
        "12": ["18:20", "19:00"], 
        "перемена": ["9:00", "18:20"]
    }

    time_obj = datetime.datetime.strptime(current_time, '%H:%M').time()
    
    for key, value in lessons_time.items():
        lesson_start = datetime.datetime.strptime(value[0], '%H:%M').time()
        lesson_end = datetime.datetime.strptime(value[1], '%H:%M').time()
        if (lesson_start <= time_obj < lesson_end):
            if key.isnumeric():
                return f"Время: {curt}, сейчас {key}-й урок"
            else:
                return f"Время: {curt}, сейчас {key}."
    return "Уроки прошли."


result = check_lesson_time()
printC("ТЕСТ ВРЕМЕНИ:", result)
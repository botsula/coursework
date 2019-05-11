from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from emoji import emojize
import datetime
from abstract_method import myTask, myAddTask, myTaskCreate

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks', 'https://www.googleapis.com/auth/tasks.readonly']


# """Shows basic usage of the Tasks API.
# Prints the title and ID of the first 10 task lists.
# """
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '2json.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

SERVICE = build('tasks', 'v1', credentials=creds)


# Проверяет, есть ли список РЗ у пользователя. Если нет, то создаёт. Если есть - pass.
def find_list():
    tasklists = SERVICE.tasklists().list().execute()
    fin = False
    id = ''
    for i in tasklists['items']:
        if i['title'] == '🦖 Remindozaur':
            fin = True
            id = i['id']
    if fin is False:
        tasklist = {
            'title': '🦖 Remindozaur'
        }
        result = SERVICE.tasklists().insert(body=tasklist).execute()
        id = result['id']
    # print(id)
    return id

def task_creation():
    title = input('Title: ')
    notes = input('Notes: ')
    due = input('Due (yyyy-mm-dd): ')
    ttype = input('Now choose the type of task.\nM - money deadline | D - common deadline\n: ')

    today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')

    today_date = datetime.date(int(today[0]), int(today[1]), int(today[2]))
    temp_date = due.split('-')
    deadline_date = datetime.date(int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
    delta = deadline_date - today_date
    # print()
    delta = int(delta.days)

    fin_money, static_money = None, None
    if ttype == 'M':
        fin_money = int(input('Money goal: '))
        # print(delta, fin_money)
        if (fin_money / delta) == (fin_money // delta):
            static_money = int(fin_money / delta)

        else:
            static_money = int(round((fin_money / delta) + 1))

    task = myTaskCreate(title, notes, due, ttype, delta, fin_money, static_money)
    if task.ttype == 'M':
        fin_task = {
            'title': emojize(':money_with_wings:') + ' {}: keep {}$, {} day{} left!'.format(task.word_title,
                                                                                           task.static_money,
                                                                                           task.delta_days,
                                                                                            's' if task.delta_days > 1
                                                                                            else ''),
            'notes': task.notes + '\n\n'
                     'Money goals: 0/{}\n'
                     'I started: {}.{}.{}\n'
                     'Deadline: {}.{}.{}\n'
                     'Amount per day: {}$'.format(task.fin_money,
                                                  today[2], today[1], today[0],
                                                  task.due[8:10], task.due[5:7], task.due[:4],
                                                  task.static_money),
            'due': task.due + 'T12:00:00.000Z'
        }
    elif task.ttype == 'D':
        fin_task = {
            'title': emojize(':fire:') + ' {}: {} day{} left!'.format(task.word_title,
                                                                                           task.delta_days,
                                                                                            's' if task.delta_days > 1
                                                                                            else ''),
            'notes': task.notes + '\n\n'
                     'I started: {}.{}.{}\n'
                     'Deadline: {}.{}.{}\n'.format(today[2], today[1], today[0],
                                                  task.due[8:10], task.due[5:7], task.due[:4]),
            'due': task.due + 'T12:00:00.000Z'
        }
    # print(fin_task)
    return fin_task



my_first_task = {
        'title': emojize(':fire:') + ' Coursework: 3 days left!',
        'notes': 'That is a deadline of my programming coursework. Blah blah blah.\n'
                 'I started: 09.05.2019\n'
                 'Deadline: 12.05.2019',  # можно будет удалить !!!
        'due': '2019-05-12T12:00:00.000Z'
    }
my_first_task = myAddTask(my_first_task)
my_first_task.word_title = my_first_task.title[2:my_first_task.title.find(':')]

# my_second_task = {
#         'title': emojize(':fire:') + ' OMAGAD: 2 days left!',
#         'notes': 'Another cool task, nothing left to say.\n'
#                  'I started: 10.05.2019\n'
#                  'Deadline: 12.05.2019',  # можно будет удалить !!!
#         'due': '2019-05-12T12:00:00.000Z'
#     }
# my_second_task = myAddTask(my_first_task)


my_first_finance_task = {
        'title': emojize(':money_with_wings:') + ' I wanna money: keep 100$, 5 days left!',
        'notes': 'That is a deadline of my programming coursework. Blah blah blah.\n\n'
                 'Money goals: 0/500\n'
                 'I started: 10.05.2019\n'
                 'Deadline: 15.05.2019\n'
                 'Amount per day: 100$',
        'due': '2019-05-15T12:00:00.000Z'
    }
my_first_finance_task = myAddTask(my_first_finance_task)
my_first_finance_task.word_title = my_first_finance_task.title[2:my_first_finance_task.title.find(':')]



def add_task(add_task_adt, rz_list_id):
    check = SERVICE.tasks().list(tasklist=rz_list_id, showCompleted=True).execute()
    items = check.get('items', [])
    for i in items:
        temp = i['title']
        if temp.startswith('🦖') is False:
            a = temp.find(':')
            temp2 = temp[2:a]
            b = add_task_adt.title.find(':')
            temp3 = add_task_adt.title[2:b]
            if temp2 == temp3:
                print('Task with the same name is already existed.')
                return False
    result = SERVICE.tasks().insert(tasklist=rz_list_id, body=add_task_adt.real_task).execute()
    fall = myTask(result)
    # print(fall)
    # print(result)
    return True


def finish_task_upload(task_adt, rz_list_id):
    date = str(datetime.datetime.now())
    fin_date = date[0:10] + 'T12:00:00.000Z'

    temp = task_adt.title
    a = temp.find(':')
    task_adt.title = temp[2:a]

    task_adt.real_task['notes'].find('')

    if task_adt.type == 'money':
        task = {
            'title': '🦖 {}: {}'.format(task_adt.title, 'you did it!' if task_adt.success is True
                                                            else 'finish line!'),

            'notes': 'Remindozaur congratulates you! {}\n{}'.format('You successfully achieved your\n"💸 ' + task_adt.title
                                                                    + '" goal!' if task_adt.success is True
                                                                    else ' And hope you stayed alive till\n"💸 '
                                                                         + task_adt.title + '" deadline!',
                                                                    'Money goals: '
                                                                    + str(task_adt.money[0]) + '/' + task_adt.money[1]),
            'due': fin_date,
            'id': task_adt.id
        }

    else:
        task = {
            'title': '🦖 {}: {}'.format(task_adt.title, 'you did it!' if task_adt.success is True
                                                            else 'finish line!'),
            'notes': 'Remindozaur congratulates you!\n{}'.format('You successfully achieved your\n"🔥 ' + task_adt.title
                                                                + '" goal!' if task_adt.success is True
                                                                else ' And hope you stayed alive till\n"🔥 '
                                                                     + task_adt.title + '" deadline!'),
            'due': fin_date,
            'id': task_adt.id
        }
    # print('- Finish task uploading...')
    if task_adt.success:
        add_task(myAddTask(task), rz_list_id)
    else:
        result = SERVICE.tasks().update(tasklist=rz_list_id, task=task['id'],
                                        body=task).execute()
        # print(result)


def money_task_up(task, rz_list_id, a, b, c, d, new_num):
    task_uploaded = SERVICE.tasks().get(tasklist=rz_list_id, task=task.id).execute()
    task_uploaded['status'] = 'needsAction'
    task_uploaded['title'] = task_uploaded['title'][:c] + str(task.money_today) + \
                             task_uploaded['title'][d:a] + str(new_num) + task_uploaded['title'][b:]
    task_uploaded['notes'] = task_uploaded['notes'][:task_uploaded['notes'].find('Money goals: ') + 13] + \
                             str(int(task.money[0])) + '/' + str(task.money[1]) + \
                             task_uploaded['notes'][task_uploaded['notes'].find('I started') - 1:]

    result = SERVICE.tasks().update(tasklist=rz_list_id, task=task_uploaded['id'],
                                    body=task_uploaded).execute()
    # print(result)


def fire_task_up(task, rz_list_id, a, b, new_num):
    # First retrieve the task to update.
    task_uploaded = SERVICE.tasks().get(tasklist=rz_list_id, task=task.id).execute()
    task_uploaded['status'] = 'needsAction'
    task_uploaded['title'] = task_uploaded['title'][:a] + str(new_num) + task_uploaded['title'][b:]

    result = SERVICE.tasks().update(tasklist=rz_list_id, task=task_uploaded['id'],
                                    body=task_uploaded).execute()
    # Print the completed date.
    # print(result)

def update_task(one_word_name, rz_list_id):
    check = SERVICE.tasks().list(tasklist=rz_list_id, showCompleted=True, showHidden=True).execute()
    items = check.get('items', [])
    flag = False #таск не виконано, потрібно буде додавати
    task = False
    for i in items:
        if i['title'].startswith('🦖') is False:
            temp = i['title']
            do_dvokrapka = temp[2:temp.find(':')]
            # print(do_dvokrapka, one_word_name)
            if do_dvokrapka == one_word_name:
                # print('I found task')
                task = myTask(i)
            # else:
            #     print('There is no "{}" task to update.'.format(one_word_name))
            #     return False
        else:
            print('Task is finished.')
    # print('task: ', task)
    if task:
        if task.status == 'completed':
            flag = True #все по плану, таск виконано
        if task.title.startswith(emojize(':fire:')):
            task.type = 'fire'
        else:
            task.type = 'money'

        if task.type == 'fire':
            a = task.title.find(':') + 2
            b = task.title.find('days left') - 1
        else:
            a = task.title.find('$,') + 3
            b = task.title.find('days left') - 1
            c = task.title.find(': keep') + 7
            d = task.title.find('$,')
            task.static_money = int(task.notes[task.notes.find('per day:') + 9:-1])  # сколько должно добавлять каждый день
            task.money_today = int(task.title[c:d])  # сколько нужно отложить сегодня
            task.money = task.notes[task.notes.find('Money goals: ')+13 : task.notes.find('I started')-1].split('/')  # накопленые деньги

        num = int(task.title[a:b])
        new_num = num - 1

        if flag is True:
            task.success = True

        if new_num == 0:
            if (task.type == 'money') & (task.success is True):
                task.money[0] = int(task.money[0]) + task.money_today
            finish_task_upload(task, rz_list_id)
        else:
            if task.type == 'fire':
                fire_task_up(task, rz_list_id, a, b, new_num)

            if task.type == 'money':
                if task.success is True:
                    task.money[0] = int(task.money[0]) + int(task.money_today)
                    task.money_today = task.static_money
                    # print(task.money_today)
                    money_task_up(task, rz_list_id, a, b, c, d, new_num)
                else:
                    task.money_today += task.static_money
                    money_task_up(task, rz_list_id, a, b, c, d, new_num)

def main():
    id = find_list()
    choice = input('Welcome to the "Remindozaur" - reminding app.\n'
                   '                    ----\n'
                   'To use it you need an active Google Account\n'
                   'and downloaded app "Google Tasks" on your cell. '
                   'You also can use it on whatever platform.\n'
                   '                    ----\n'
                   'Choose from list:\n'
                   '1 - Create a new task and add it.\n'
                   '2 - Update tasks on your account (once a day auto-update will be available on a web-version).\n'
                   '3 - Quite the program.'
                   '! To delete any task you just need to DELETE (not complete) it from your task list.\n: ')
    if choice == '1':
        a = task_creation()
        add_task(myAddTask(a), id)
        main()
    elif choice == '2':
        temp = input('Name of the task: ')
        update_task(temp, id)
        main()
    elif choice == '3':
        return None



if __name__ == '__main__':
    main()

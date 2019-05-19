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

creds = None

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '2json.json', SCOPES)
        creds = flow.run_local_server()

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

SERVICE = build('tasks', 'v1', credentials=creds)


def find_list():
    '''
    Find list 'Remindozaur' in user`s account and returns its ID. If list is missing, than function creates it.
    :return: str, ID of 'Remindozaur' list
    '''
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
    return id


def task_creation_web(title, notes, due, money):
    '''
    Create new task from web-app user`s input and return the task dictionary of Google Tasks format.
    :param title: the name of task, str
    :param notes: some information about task, str
    :param due: due date in format yyyy-mm-dd, str
    :param money: money amount (e.q. '1000') or '0', str
    :return: dictionary of Google Tasks format for task
    '''
    today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')

    today_date = datetime.date(int(today[0]), int(today[1]), int(today[2]))
    temp_date = due.split('-')
    deadline_date = datetime.date(int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
    delta = deadline_date - today_date
    delta = int(delta.days)

    fin_money, static_money = None, None
    if money != '0':
        fin_money = int(money)
        if (fin_money / delta) == (fin_money // delta):
            static_money = int(fin_money / delta)

        else:
            static_money = int(round((fin_money / delta) + 1))
        money = 'M'

    task = myTaskCreate(title, notes, due, money, delta, fin_money, static_money)
    if money == 'M':
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
    else:
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
    return fin_task


def task_creation():
    '''
    Function for console program usage.
    Create new task from user`s input and return the task dictionary of Google Tasks format.
    :param title: the name of task, str
    :param notes: some information about task, str
    :param due: due date in format yyyy-mm-dd, str
    :param money: money amount (e.q. '1000') or '0', str
    :return: dictionary of Google Tasks format for task
    '''
    title = input('Title: ')
    notes = input('Notes: ')
    due = input('Due (yyyy-mm-dd): ')
    ttype = input('Now choose the type of task.\nM - money deadline | D - common deadline\n: ')

    today = datetime.datetime.today().strftime('%Y-%m-%d').split('-')

    today_date = datetime.date(int(today[0]), int(today[1]), int(today[2]))
    temp_date = due.split('-')
    deadline_date = datetime.date(int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
    delta = deadline_date - today_date
    delta = int(delta.days)

    fin_money, static_money = None, None
    if ttype == 'M':
        fin_money = int(input('Money goal: '))
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
    return fin_task


def add_task(add_task_adt, rz_list_id):
    '''
    Add task to user`s Google Account.
    :param add_task_adt: task of myAddTask() type
    :param rz_list_id: ID of 'Remindozaur' list in user`s account
    :return: bool
    '''
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
    return True


def finish_task_upload(task_adt, rz_list_id):
    '''
    When task was updated after 1 day left, this function uploads the final greetings task with congratulations.
    :param task_adt: task of myTask() type
    :param rz_list_id: ID of 'Remindozaur' list in user`s account
    :return: None
    '''
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

            'notes': 'Remindozaur congratulates you! {}\n{}'.format(
                'You successfully achieved your\n"💸 ' + task_adt.title
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
    if task_adt.success:
        add_task(myAddTask(task), rz_list_id)
    else:
        result = SERVICE.tasks().update(tasklist=rz_list_id, task=task['id'],
                                        body=task).execute()


def money_task_up(task, rz_list_id, a, b, c, d, new_num):
    '''
    Update 'money' type deadline/task and upload it to user`s account.
    :param task: task of myTask() type
    :param rz_list_id: ID of 'Remindozaur' list in user`s account
    :param a: first flag for parsing title, int
    :param b: second flag for parsing title, int
    :param c: first flag for parsing money, int
    :param d: second flag for parsing money, int
    :param new_num: updated number of days till deadline
    :return: None
    '''
    task_uploaded = SERVICE.tasks().get(tasklist=rz_list_id, task=task.id).execute()
    task_uploaded['status'] = 'needsAction'
    task_uploaded['title'] = task_uploaded['title'][:c] + str(task.money_today) + \
                             task_uploaded['title'][d:a] + str(new_num) + task_uploaded['title'][b:]
    task_uploaded['notes'] = task_uploaded['notes'][:task_uploaded['notes'].find('Money goals: ') + 13] + \
                             str(int(task.money[0])) + '/' + str(task.money[1]) + \
                             task_uploaded['notes'][task_uploaded['notes'].find('I started') - 1:]

    result = SERVICE.tasks().update(tasklist=rz_list_id, task=task_uploaded['id'],
                                    body=task_uploaded).execute()


def fire_task_up(task, rz_list_id, a, b, new_num):
    '''
    Update 'usual' type deadline/task and upload it to user`s account.
    :param task: task of myTask() type
    :param rz_list_id: ID of 'Remindozaur' list in user`s account
    :param a: first flag for parsing title, int
    :param b: second flag for parsing title, int
    :param new_num: updated number of days till deadline
    :return: None
    '''
    # First retrieve the task to update.
    task_uploaded = SERVICE.tasks().get(tasklist=rz_list_id, task=task.id).execute()
    task_uploaded['status'] = 'needsAction'
    task_uploaded['title'] = task_uploaded['title'][:a] + str(new_num) + task_uploaded['title'][b:]

    result = SERVICE.tasks().update(tasklist=rz_list_id, task=task_uploaded['id'],
                                    body=task_uploaded).execute()


def find_all_tasks(rz_list_id):
    '''
    Return list of [title, notes] all user`s active and completed tasks from Google Tasks.
    :param rz_list_id: ID of 'Remindozaur' list in user`s account, str
    :return: list of [title, notes], lst(str, str)
    '''
    check = SERVICE.tasks().list(tasklist=rz_list_id, showCompleted=True, showHidden=True).execute()
    items = check.get('items', [])
    fin = []
    for i in items:
        if i['title'].startswith('🦖') is False:
            temp = i['title']
            temp_2 = i['notes']
            do_dvokrapka = temp[2:temp.find(':')]
            fin.append([do_dvokrapka, temp_2])
    return fin


def update_task(one_word_name, rz_list_id):
    '''
    Update all 'Remindozaur' tasks:
    - check if deadline was completed or not, and based on it process its parameters
    - change the days till deadline
    - change the amount per day for money deadlines
    - update information in notes for user to see which amount is already gathered
    - if 0 days till deadline, raise finish_task_upload() function
    :param one_word_name: task title made by user, str
    :param rz_list_id: ID of 'Remindozaur' list in user`s account
    :return: None
    '''
    check = SERVICE.tasks().list(tasklist=rz_list_id, showCompleted=True, showHidden=True).execute()
    items = check.get('items', [])
    flag = False  # shows that task is not completed
    task = False
    for i in items:
        if i['title'].startswith('🦖') is False:
            temp = i['title']
            do_dvokrapka = temp[2:temp.find(':')]
            if do_dvokrapka == one_word_name:  # task is found
                task = myTask(i)
        else:
            print('Task is finished.')
    if task:
        if task.status == 'completed':
            flag = True  # task is completed
        if task.title.startswith(emojize(':fire:')):
            task.type = 'fire'
        else:
            task.type = 'money'

        if task.type == 'fire':
            a = task.title.find(':') + 2
            if 'days left' in task.title:
                b = task.title.find('days left') - 1
            else:
                b = task.title.find('day left') - 1
        else:
            a = task.title.find('$,') + 3
            if 'days left' in task.title:
                b = task.title.find('days left') - 1
            else:
                b = task.title.find('day left') - 1
            c = task.title.find(': keep') + 7
            d = task.title.find('$,')
            task.static_money = int(
                task.notes[task.notes.find('per day:') + 9:-1])  # static money keep amount per day
            task.money_today = int(task.title[c:d])  # money to keep at current day
            task.money = task.notes[task.notes.find('Money goals: ') + 13: task.notes.find('I started') - 1].split(
                '/')  # already gathered money

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
                    money_task_up(task, rz_list_id, a, b, c, d, new_num)
                else:
                    task.money_today += task.static_money
                    money_task_up(task, rz_list_id, a, b, c, d, new_num)


def main():
    '''
    The main function built for using Remindozaur app with console.
    :return: None
    '''
    id = find_list()
    choice = input('Welcome to the "Remindozaur" - reminding app.\n'
                   '                    ----\n'
                   'To use it you need an active Google Account\n'
                   'and downloaded app "Google Tasks" on your cell. '
                   'You also can use it on whatever platform.\n'
                   '                    ----\n'
                   'Choose from list:\n'
                   '1 - Create a new task and add it.\n'
                   '2 - Update task on your account (once a day auto-update will be available on a web-version).\n'
                   '3 - Update all "Remindozaur" tasks.\n'
                   '4 - Quite the program.'
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
        for task_title in find_all_tasks(id):
            update_task(task_title[0], id)
        main()
    elif choice == '4':
        return None


if __name__ == '__main__':
    main()

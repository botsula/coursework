class myTaskCreate:
    '''Initialize the creating task'''
    def __init__(self, word_title, notes, due, ttype, delta_days, fin_money, static_money, ):
        self.word_title = word_title
        self.notes = notes
        self.due = due
        self.ttype = ttype
        self.fin_money = fin_money
        self.static_money = static_money
        self.delta_days = delta_days

class myAddTask:
    '''Initialize the adding task.'''
    def __init__(self, task_dict):
        self.real_task = task_dict
        self.title = task_dict['title']
        self.notes = task_dict['notes']
        self.due = task_dict['due']
        self.word_title = None

class myTask:
    '''Initialise usual task.'''
    def __init__(self, task_dict):
        self.real_task = task_dict
        self.title = task_dict['title']
        self.updated = task_dict['updated']
        self.status = task_dict['status']
        self.notes = task_dict['notes']
        self.due = task_dict['due']
        self.id = task_dict['id']
        self.type = None
        self.success = None
        self.static_money = None
        self.money = None # [now/need]
        self.money_today = None

    def __str__(self):
        return 'Title: {}\n'.format(self.title) + \
               'Notes: {}\n'.format(self.notes) + \
               'Due: {}\n'.format(self.due) + \
               'Status: {}\n'.format(self.status) + \
               'Updated: {}\n'.format(self.updated) + \
               'ID: {}'.format(self.id)


class myTaskList:
    '''Creating my abstract method.'''

    def __init__(self, lst):
        '''Initialize my data type.'''
        self.data = lst

    def get_task(self, index):
        '''Return task dictionary with defined index.'''
        return self.data[index]

    def __getitem__(self, item):
        '''Return item with defined index'''
        return self.get_task(item)

    def get_title(self, index):
        '''Return title of task with defined index.'''
        return self.__getitem__(index)['title']

    def get_due(self, index):
        '''Return due of task with defined index.'''
        return self.__getitem__(index)['due']

    def get_note(self, index):
        '''Return notes from task of defined index.'''
        return self.__getitem__(index)['notes']

    def get_all_titles(self):
        '''Return list of whole titles in tasks'''
        titles = []
        for i in self.data:
            titles.append(i['title'])
        return titles

    def get_all_notes(self):
        '''Return the list of all notes'''
        notes = []
        for i in self.data:
            notes.append(i['notes'])
        return notes

    def __len__(self):
        '''Return the amount of elements in my data type'''
        return len(self.data)

    def __repr__(self):
        '''Representation of my data type'''
        return list(self.data)

    def __str__(self):
        '''String representation of my data type.'''
        res = ''
        for i in range(len(self)):
            res += str(self.get_task(i)) + '\n'
        return res

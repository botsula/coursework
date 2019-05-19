class myTaskCreate:
    '''Class made for creating tasks function.'''

    def __init__(self, word_title, notes, due, ttype, delta_days, fin_money, static_money):
        '''
        Initialize the creating task.
        :param word_title: the task name made by user, str
        :param notes: notes made by user, str
        :param due: the date in format yyyy-mm-dd, task deadline
        :param ttype: money or usual, str
        :param delta_days: the days before deadline, str
        :param fin_money: the amount user wants to reach before deadline, str (if deadline type is 'money')
        :param static_money: the amount user needs to keep for a day before deadline (if deadline type is money)
        '''
        self.word_title = word_title
        self.notes = notes
        self.due = due
        self.ttype = ttype
        self.fin_money = fin_money
        self.static_money = static_money
        self.delta_days = delta_days


class myAddTask:
    '''Class made for adding tasks function.'''

    def __init__(self, task_dict):
        '''
        Initialise the adding task.
        :param task_dict: the task data dictionary in Google Tasks format
        '''
        self.real_task = task_dict
        self.title = task_dict['title']
        self.notes = task_dict['notes']
        self.due = task_dict['due']
        self.word_title = None


class myTask:
    '''Create usual task for main data processing'''

    def __init__(self, task_dict):
        '''
        Initialize the usual task.
        :param task_dict: the task data dictionary in Google Tasks format

        '''
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
        self.money = None  # [now/need]
        self.money_today = None

    def __str__(self):
        '''
        String representation of task.
        :return:
        '''
        return 'Title: {}\n'.format(self.title) + \
               'Notes: {}\n'.format(self.notes) + \
               'Due: {}\n'.format(self.due) + \
               'Status: {}\n'.format(self.status) + \
               'Updated: {}\n'.format(self.updated) + \
               'ID: {}'.format(self.id)

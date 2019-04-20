
class myDataType:
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

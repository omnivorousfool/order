import tkinter as tk
from tkinter.constants import UNDERLINE, W
from widgets import generate_font, dialog, records_board, button
import tkinter.font

def trans(matrix):
    result = []
    for n in range(0, len(matrix[0])):
        col = []
        for row in matrix:
            col += [row[n]]
        result += [col]
    return result

def load_records():
    try:
        with open('records.numrcds', 'r') as numrcds:
            meta = numrcds.read()
    except:
        with open('records.numrcds', 'w') as numrcds:
            meta = ''
    if meta == '':
        return [['You', 'have', 'not', 'played', 'NUMSKI', 'yet.']]
    records = meta.split('\n')
    record_list = []
    for i in records:
        record_list.append(i.split(','))
    record_list.remove([''])
    return record_list

class records(dialog):
    def __init__(self, master):
##        self.attributes('-alpha', 0)
        super().__init__(master)
        self.font = generate_font(size=48)
        self.title('NUMSKI Records')
##        self.align()
##        self.bind('<ButtonPress>', test)
        self.title = tk.Label(self, text='Records', font=self.font, bg='white', fg='black')
        self.title.pack()
        self.display_records()
        self.sort_index = [0, False] # first indicates the sorting dependent, second represents reverse(True) or not
        self.set_headings_funcs()
        
    def display_records(self):
        font = generate_font(size=10, weight=tkinter.font.NORMAL)
        
        self.record_list = records_board(master=self, font=font, colwidth=[20, 5, 10, 7, 12, 12],
                                         order=True)
        self.records = load_records()
        self.record_list.insert(self.records)
        self.record_list.set_headings()
        
        self.record_list.scroll_frame.frame.adjust_size(None)
        self.record_list.pack(fill=tk.BOTH, expand=True)

                

    def set_headings_funcs(self):
        headings = ['No.', 'Date', 'Level', 'Time', 'Move', 'Shuffle times', 'Gamemode']
        
        def set_arrow(widget, origin, down=False):
            if down:  
                widget['text'] = '%s▲' % origin
            else:
                widget['text'] = '%s▼' % origin
                
        def sort_date():
            reverse = not self.sort_index[1]
            data = sorted(self.records, key=lambda x: x[0], reverse=reverse)
            self.record_list.cfg_values(data)
            self.sort_index[1] = reverse
            set_arrow(self.record_list.headings[1], 'Date', down=reverse)
            self.record_list.cfg_headings(headers=['No.', None, 'Level', 'Time', 'Move', 'Shuffle times', 'Gamemode'])

        def sort_level():
            reverse = not self.sort_index[1]
            data = sorted(self.records, key=lambda x: float(x[1].replace('x','.')), reverse=reverse)
            self.record_list.cfg_values(data)
            self.sort_index[1] = reverse
            set_arrow(self.record_list.headings[2], 'Level', down=reverse)
            self.record_list.cfg_headings(headers=['No.', 'Date', None, 'Time', 'Move', 'Shuffle times', 'Gamemode'])

        def sort_time():
            reverse = not self.sort_index[1]
            data = sorted(self.records, key=lambda x: float(x[2].replace('s','')), reverse=reverse)
            self.record_list.cfg_values(data)
            self.sort_index[1] = reverse
            set_arrow(self.record_list.headings[3], 'Time', down=reverse)
            self.record_list.cfg_headings(headers=['No.', 'Date', 'Level', None, 'Move', 'Shuffle times', 'Gamemode'])

        def sort_move():
            reverse = not self.sort_index[1]
            data = sorted(self.records, key=lambda x: int(x[3]), reverse=reverse)
            self.record_list.cfg_values(data)
            self.sort_index[1] = reverse
            set_arrow(self.record_list.headings[4], 'Move', down=reverse)
            self.record_list.cfg_headings(headers=['No.', 'Date', 'Level', 'Time', None, 'Shuffle times', 'Gamemode'])

        def sort_shuffle():
            reverse = not self.sort_index[1]
            data = sorted(self.records, key=lambda x: int(x[4]), reverse=reverse)
            self.record_list.cfg_values(data)
            self.sort_index[1] = reverse
            set_arrow(self.record_list.headings[5], 'Shuffle times', down=reverse)
            self.record_list.cfg_headings(headers=['No.', 'Date', 'Level', 'Time', 'Move', None, 'Gamemode'])

        def sort_gm():
            reverse = not self.sort_index[1]
            data = sorted(self.records, key=lambda x: x[5], reverse=reverse)
            self.record_list.cfg_values(data)
            self.sort_index[1] = reverse
            set_arrow(self.record_list.headings[6], 'Gamemode', down=reverse)
            self.record_list.cfg_headings(headers=['No.', 'Date', 'Level', 'Time', 'Move', 'Shuffle times', None])

        def no_heading():
            data = sorted(self.records, key=lambda x: x[0])
            self.record_list.cfg_headings(headers=['No.', 'Date', 'Level', 'Time', 'Move', 'Shuffle times', 'Gamemode'])
            self.record_list.cfg_values(data)

        cmds = [no_heading, sort_date, sort_level, sort_time, sort_move, sort_shuffle, sort_gm]
##        for i in range(0,6):
##            cmd = lambda :sort_(i)
##            cmds.append(cmd)
##        cmds = [lambda :sort_(n) for n in range(0,7)]
##        print(cmds)
        self.record_list.cfg_headings(headers=headings, cmds=cmds)

##        for heading in self.record_list.headings:
##            heading.bind('<ButtonRelease-1>', self.set_arrow, '+')
            
##        self.record_list.cfg_headings(headers=headings,)

    def sort_data(self, *args):
        print('test')
        data = sorted(self.records, key=lambda x:x[1])
        self.record_list.cfg_values(data)

img = None

from os import system, popen

class about(dialog):
    def __init__(self, master=None):
        global img
        super().__init__(master)
        self.msg_font = generate_font(size=15, weight=tkinter.font.NORMAL)
        self.title_font = generate_font(size=40)
        self.link_font = generate_font(size=10, weight=tkinter.font.NORMAL, underline=True)
        img = tk.PhotoImage(file='GUI\pythonlogo.png')
        self.link_cmd = lambda : system('start https://github.com/omnivorousfool/order')
        self.about_msg = \
'\
This is a game compiled by Python with GUI made by tkinter.\n\
Version: 0.1\n\
Author: omnivorousfool\n\
Wechat: kuroko656045229\n\
Thanks for playing.\
'
        tk.Label(self, bg='white').pack(side='top')
        tk.Label(self, text='About NUMSKI', font=self.title_font, fg='black', bg='white').pack(side='top', padx=10)
        # tk.Label(self, image=img, bg='white').pack(side='top')
        tk.Label(self, text=self.about_msg, font=self.msg_font, image=img, fg='black', bg='white', justify='left', compound=tk.CENTER).pack(side='top', pady=20, padx=40)
        button(self, text='source code: https://github.com/omnivorousfool/order', font=self.link_font, command=self.link_cmd, changebg=False).pack(side='top', pady=5)
        

import numski
from widgets import suspend_dialog

class play(dialog):
    def __init__(self, master=None, board_size=None, shuffle_times=None, mode='Normal'):
        super().__init__(master)
        self.master = master
        self.attributes('-alpha', 0)
        self.size = None
        self.board_size = board_size
        self.shuffle_times = shuffle_times
        self.mode = mode
        self.start_play()
        self.unbind('<Escape>')
        self.bind('<KeyRelease-Escape>', lambda event:self.create_suspend_dialog())

    def start_play(self):
        self.numski = numski.numski(size=self.board_size, shuffle_times=self.shuffle_times, mode=self.mode, master=self)
        self.numski.pack(side='left',
                         anchor='w',
                         expand=True,
                         fill=tk.BOTH
                         )
        font = generate_font(size=25)
        frame = tk.Frame(self, bg='white', bd=0)
        frame_ = tk.Frame(self, bg='white', bd=0)
        tk.Label(frame, text='Time:', font=font, bg='white', fg='black', bd=5, justify='left').pack(side='left', anchor='n', fill=tk.X)
        self.time_label = tk.Label(frame, textvariable=self.numski.time_used, fg='black', font=font, bg='white', bd=2, justify='left')
        self.time_label.pack(side='left', anchor='n', fill=tk.X)
        tk.Label(frame_, text='Move:', font=font, bg='white', fg='black', bd=5, justify='left').pack(side='left', anchor='s', fill=tk.X)
        self.move_count = tk.Label(frame_, textvariable=self.numski.count_var, font=font, fg='black', bg='white', bd=2, justify='left')
        self.move_count.pack(side='left', anchor='s', fill=tk.X)
        frame.pack()
        frame_.pack()
        
        self.align()
##        self.attributes('-alpha', 0.6)
        self.numski.shuffle_thread.start()

    def create_suspend_dialog(self):
        self.suspend_menu = suspend_dialog(self)
##        self.suspend_menu.align()
        
if __name__ == '__main__':
    root = tk.Tk()
    a = about(master=root)
    root.mainloop()
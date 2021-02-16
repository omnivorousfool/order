import tkinter as tk
import tkinter.font
import re
from time import sleep
from threading import Thread
import datetime

def generate_font(size=22, weight=tkinter.font.BOLD, *arg, **kw):
    '''
    font size 25 33 40 48
    '''
    return tkinter.font.Font(family='Century Gothic', size=size, weight=weight, *arg, **kw)

def get_date():
    date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    ms = datetime.datetime.now().microsecond
    now = '%s.%d' % (date, ms // 100000)
    return now

class main_window(tk.Tk):
    def __init__(self, size=None):
        super().__init__()
        self.title('NUMSKI')
        self.wm_overrideredirect(True)
        self.attributes('-alpha', 0)
        self.configure(bg='white')
        self.bind('<FocusIn>', lambda event: self.alpha_(False))
        self.bind('<FocusOut>', lambda event: self.alpha_(True))
        self.size = size

    def align(self):
        if self.size == None:
            self.update()
            alignstr = '+%d+%d' % ((self.winfo_screenwidth()-self.winfo_width())/2, (self.winfo_screenheight()-self.winfo_height())/2)
            self.geometry(alignstr)
            self.attributes('-alpha', 1)
        else:
            self.size_x, self.size_y = self.size[0], self.size[1]
            alignstr = '%dx%d+%d+%d' % (self.size_x, self.size_y, (self.winfo_screenwidth()-self.size_x)/2, (self.winfo_screenheight()-self.size_y)/2)
            self.geometry(alignstr)
            self.attributes('-alpha', 1)

    def move_window(self, event):
        action = str(event.type)
        if action == 'ButtonPress':
            self.x = event.x
            self.y = event.y
        elif action == 'ButtonRelease':
            self.x = 0
            self.y = 0
        elif action == 'Motion':
            delta_x = event.x - self.x
            delta_y = event.y - self.y
            pos_x = self.winfo_x()
            pos_y = self.winfo_y()
            x = delta_x + pos_x
            y = delta_y + pos_y
            self.geometry('+%d+%d'%(x, y))
            
    def alpha_(self, out):
        if out:
            self.attributes('-alpha', 0.7)
        else:
            self.attributes('-alpha', 1)
            
    def close(self, widget):
        widget.destroy()
        

class dialog(tk.Toplevel):
    def __init__(self, master=None, size=None):
        super().__init__(master)
        self.attributes('-alpha', 0)
        self.master = master
        master.title('NUMSKI')
##        self.geometry(None)
        self.wm_overrideredirect(True)
##        self.dialog.transient(self.window)
##        self.dialog.attributes('-toolwindow', 1)
        self.focus()
        self.grab_set()
        self.configure(relief='solid', bd=12, bg='white'
##                       takefocus=True
                       )
        self.bind('<KeyRelease-Escape>', lambda event: self.back())
        self.bind('<FocusIn>', lambda event: self.alpha_(False))
        self.bind('<FocusOut>', lambda event: self.alpha_(True))
        self.size = size
        
    def align(self):  ## the size of the dialog must be larger than the size of the main window
        self.master.update()
        self.win_width, self.win_height = self.master.winfo_width(), self.master.winfo_height()
        self.win_x, self.win_y = self.master.winfo_x(), self.master.winfo_y()
        if self.size != None:
            self.width, self.height = self.size[0], self.size[1]
            alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.win_width-self.width)/2+self.win_x, (self.win_height-self.height)/2+self.win_y)
            self.geometry(alignstr)
            self.attributes('-alpha', 1)
        else:
            self.update()
            self.width, self.height = self.winfo_width(), self.winfo_height()
            alignstr = '+%d+%d' % ((self.win_width-self.width)/2+self.win_x, (self.win_height-self.height)/2+self.win_y)
            self.geometry(alignstr)
            self.attributes('-alpha', 1)
            
    def alpha_(self, out):
        if out:
            self.attributes('-alpha', 0.6)
        else:
            self.attributes('-alpha', 1)

    def close(self):
        self.destroy()

    def back(self):
        self.master.focus()
        self.master.grab_set()
        self.destroy()

class button(tk.Label):
    def __init__(self, master=None, command=None, changebg=True, **kw):
        super().__init__(master, bg='white', fg='black', takefocus=True, **kw)
        self.bind('<ButtonPress-1>', lambda event:self.press(changebg))
        self.bind('<ButtonRelease-1>', self.release)
        self.bind('<FocusIn>', self.focusIn)
        self.bind('<FocusOut>', self.focusOut)
        self.bind('<Enter>', self.focusIn)
        self.bind('<Leave>', self.focusOut)
        self.bind('<KeyPress-Return>',lambda event:self.press(changebg))
        self.bind('<KeyRelease-Return>', self.release)
        if command == None:
            self.command = lambda : print('clicked')
        else:
            self.command = command
            
    def press(self, changebg, *args):
        self.bg, self.fg = self.cget('bg'), self.cget('fg')
        if changebg:
            self.configure(bg='black', fg='white',
##                           underline=0
                           )
##        else:
##            self.configure(underline=0)
        
    def release(self, *args):
        self.configure(bg=self.bg, fg=self.fg,
##                       underline=-1
                       )
        self.command()

    def focusIn(self, *args):
        self.configure(
##            underline=0,
            fg='gray50')

    def focusOut(self, *args):
        self.configure(
##            underline=-1,
            fg='black')

    def cfg_cmd(self, cmd=lambda : print('clicked')):
        self.command = cmd


class switch(tk.Label):
    img_set = None
    def __init__(self, master=None, cmds=None, status=False, *args, **kw):
        global img_set
        super().__init__(master, takefocus=True, *args, **kw)
        self.status = status
        self.cmds = cmds   ## a tuptle that contains two functions and the first one is called when the switch is and the second is called when off
        self.img_set = (
                   tk.PhotoImage(file='GUI/GUI_switch_on.png'),     #0
                   tk.PhotoImage(file='GUI/GUI_switch_on_a.png'),   #1
                   tk.PhotoImage(file='GUI/GUI_switch_on_c.png'),   #2
                   tk.PhotoImage(file='GUI/GUI_switch_off.png'),    #3
                   tk.PhotoImage(file='GUI/GUI_switch_off_a.png'),  #4
                   tk.PhotoImage(file='GUI/GUI_switch_off_c.png')   #5
                   )
        self.init()

    def focusIn(self, event):
        if self.status:
            self['image'] = self.img_set[1]
        else:
            self['image'] = self.img_set[4]

    def focusOut(self, event):
        if self.status:
            self['image'] = self.img_set[0]
        else:
            self['image'] = self.img_set[3]

    def press(self, event):
        if self.status:
            self['image'] = self.img_set[2]
        else:
            self['image'] = self.img_set[5]
            
    def release(self, event):
        if self.status:
            self['image'] = self.img_set[4]
            self.status = False
            self.cmds[1]()
        else:
            self['image'] = self.img_set[1]
            self.status = True
            self.cmds[0]()

    def init(self):
        if self.status:
            self['image'] = self.img_set[0]
            self.bind_funcs()
        else:
            self['image'] = self.img_set[3]
            self.bind_funcs()

    def bind_funcs(self):
        self.bind('<FocusIn>', self.focusIn)
        self.bind('<FocusOut>', self.focusOut)
        self.bind('<Enter>', self.focusIn)
        self.bind('<Leave>', self.focusOut)
        self.bind('<ButtonPress-1>', self.press)
        self.bind('<ButtonRelease-1>', self.release)
        self.bind('<KeyPress-space>', self.press)
        self.bind('<KeyRelease-space>', self.release)
        
    def unbind_funcs(self):
        self.unbind('<FocusIn>')
        self.unbind('<FocusOut>')
        self.unbind('<Enter>')
        self.unbind('<Leave>')
        self.unbind('<ButtonPress-1>')
        self.unbind('<ButtonRelease-1>')
        self.unbind('<KeyPress-space>')
        self.unbind('<KeyRelease-space>')
        
    def set_disabled(self):
        self.disabled_img = (tk.PhotoImage(file='GUI/GUI_switch_on_disabled.png'), tk.PhotoImage(file='GUI/GUI_switch_off_disabled.png'))
        if self.status:
            self['image'] = self.disabled_img[0]
            self.unbind_funcs()
        else:
            self['image'] = self.disabled_img[1]
            self.unbind_funcs()
            
    def set_enabled(self):
        self.init()

def convt_index(index):
    pos = [0,0]
    pos[0], pos[1] = map(int, index.split('.'))
    return pos

def convt_pos(pos):
    return '%d.%d' % (pos[0], pos[1])
        
class entry(tk.Text):
    def __init__(self, master=None, max=2, *args, **kw):
        super().__init__(master,  *args, **kw)
        self.master = master
        self.font = generate_font(size=33, weight=tk.font.NORMAL)
        self.max_len = max
        self.insert('insert', 'test')
        self.configure(font=self.font,
                       wrap=tk.NONE,
                       height=1,
                       width=max,
                       bg='white',
                       fg='black',
                       insertbackground='black',
                       highlightcolor='black',
                       highlightbackground='white',
                       selectbackground='black',
                       selectforeground='white',
                       bd=0
                       )
        self.bind('<Key>', lambda event: self.verify_len())
        self.bind('<KeyPress>', lambda event: self.verify_char(), '+')
        self.bind('<KeyRelease>', lambda event: self.verify_char(), '+')
        self.bind('<FocusOut>', lambda event: self.verify_char(delete=True))
        

    def verify_len(self):
        insert = self.get(1.0, convt_pos([1, self.max_len-1]))
        content = self.get(1.0, tk.END)
                    
        if len(content) > self.max_len:
            print(len(content))
            self.delete(1.0, tk.END)
            self.insert('insert', insert)
            print('insert', insert)
            
    def verify_char(self, delete=False):
        content = self.get(1.0, tk.END)
        num = r'[^\d\n]'
        num_find = re.search(num, content)
        print(num_find)
        if num_find != None:
            print(self.index(tk.INSERT))
            insert = self.index(tk.INSERT)
            if delete:
                self.delete(1.0, tk.END)
            else:
                pos = convt_index(insert)
                pos[1] -= 1
                # f = round(float(insert)-0.1, 1)
                print(pos)
                self.delete(convt_pos(pos), insert)
            return True
        else:
            return False

    def get_value(self):
        return self.get(1.0, tk.END)

class progressbar(tk.Label):
    def __init__(self, master=None, maximum=None, length=10):
        super().__init__(master)
        self.master = master
        self.maximum = maximum
        self.length = length
        font = generate_font()
        self.tick = '■'
        self.tick_ = '□'
        self.configure(bg='white', fg='black', font=font)

    def set_value(self, value):
        if self.maximum == 0:
            self['text'] = self.tick * self.length
            return None
        self.tick_num = int(round((value / self.maximum) * self.length, 0))
##        print(self.tick_num)
        self.progress = self.tick * self.tick_num + (self.length - self.tick_num) * self.tick_
        self['text'] = self.progress

class list_box(tk.Listbox):
    def __init__(self, master=None, font=None):
        super().__init__(master)
        self.master = master
##        font = generate_font(weight=tkinter.font.NORMAL)
        self.configure(bg='white',
                       font=font,
                       fg='black',
                       selectmode='extended',
##                       insertbackground='black',
                       highlightcolor='black',
                       highlightbackground='white',
                       selectbackground='black',
                       selectforeground='white',
                       relief='flat'
                       )
##        self.bind('<MouseWheel>', test)
        self.bind('<Button-1>', self.test)
        
    def scroll(self, event):
        self.yview('scroll', event.delta//120, 'units')
        pass
        
    def view_details(self, item):
        
        pass
    def test(self, *args):
        self.yview_scroll(1, 'units')

class scrolledable(tk.Canvas):
    def __init__(self, master=None, **kw):
        super().__init__(master, bg='white', bd=0, highlightthickness=0, **kw)
        self.container = tk.Frame(self, bd=0, bg='black')
        self.container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.container_ = self.create_window(0, 0, window=self.container, anchor=tk.NW)
        self.xview_moveto(0)
        self.yview_moveto(0)
        
    def adjust_size(self, event):
        self.update()
        size = (self.container.winfo_reqwidth(), self.container.winfo_reqheight())
        self.config(scrollregion='0 0 %s %s' % size, width=self.container.winfo_reqwidth())
        print(size)
        if self.container.winfo_reqwidth() != self.winfo_reqwidth():
            self.itemconfigure(self.container_, width=self.container.winfo_reqwidth())
        
        def scroll(event):
            self.yview_scroll(-1*int((event.delta / 120)), "units")
##            print(event.delta)
            
        self.container.bind_all('<MouseWheel>', scroll)
##        self.container.bind('<Configure>',adjust_size)
##        self.master.master.bind('<Button-1>', test)
        
    def set_scrollbar(self, master=None):
        self.scrollbar = tk.Scrollbar(master,
                                      bg='white',
                                      bd=0,
                                      relief='flat',
                                      troughcolor='white',
                                      highlightcolor='black',
                                      highlightbackground='white'
                                      )
        self.scrollbar.config(command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)

class scroll_frame_with_bar(tk.Frame):
    def __init__(self, master=None, *args, **kw):
        super().__init__(master, bg='white', bd=0, *args, **kw)
        self.frame = scrolledable(master=self, **kw)
        self.frame.pack(side='left', fill=tk.BOTH, expand=True)
        self.container = self.frame.container
        self.frame.set_scrollbar(master=self)
        self.frame.scrollbar.pack(side='left', fill=tk.BOTH, expand=True)

class records_board(tk.Frame):
    def __init__(self, master=None, font=None, colwidth=None, order=False,  **kw):
        super().__init__(master, bg='white', bd=0, **kw)
        self.scroll_frame = scroll_frame_with_bar(master=self, height=368)
        self.scroll_frame.pack(side='bottom')
        self.font = font
        self.rows = []
        self.headings = []
        self.width = colwidth
        self.order = order
        
    def set_headings(self):
        if self.order:
            headers_no = len(self.values[0]) + 1
        else:
            headers_no = len(self.values[0])

        print(headers_no)
        for n in range(0, headers_no):
            heading = button(master=self,
                             font=self.font, width=self.width[n])
            heading.pack(side='left', anchor='w')
##            heading.bind('<ButtonRelease-1>', )
            self.headings.append(heading)
            
    def cfg_headings(self, headers=None, cmds=None):
        if cmds == None:
            for n, heading in enumerate(self.headings):
                if n == None:
                    pass
                else:
                    heading.configure(text=headers[n])
        else:
            for n, heading in enumerate(self.headings):
                heading.configure(text=headers[n])
                heading.cfg_cmd(cmds[n])
            
    def insert(self, values):
        self.values = values
        def select_row(event):
            widget = event.widget
            action = event.type
            self.fg, self.bg = widget.cget('fg'), widget.cget('bg')
            row = widget.grid_info()['row']
            for cell in self.rows[row]:
                cell.configure(fg='white', bg='black')       
        def select_row_(event):
            widget = event.widget
            action = event.type
            row = widget.grid_info()['row']
            for cell in self.rows[row]:
                cell.configure(fg=self.fg, bg=self.bg)
        if self.order:
            ordered_values = self.add_order(values)
            del values
        else:
            ordered_values = values
        for n, row in enumerate(ordered_values):
            cells = []
            for m, i in enumerate(row):
                cell = button(master=self.scroll_frame.container, text=i, font=self.font, bd=2, width=self.width[m])
                cell.configure(takefocus=0)
                if n % 2 == 0:
                    cell.configure(bg='grey80')
                cell.grid(column=m, row=n, sticky='ESWN')
                cells.append(cell)
                cell.unbind('<Enter>')
                cell.unbind('<Leave>')
                cell.bind('<Enter>', select_row)
                cell.bind('<Leave>', select_row_)
            self.rows.append(cells)
            
    def add_order(self, values):
        values_ = []
        for n, row in enumerate(values):
            new_row = [str(n+1)] + row
            values_.append(new_row)
        print('order inserted')
        self.width.insert(0, 5)
        return values_
    
    def cfg_values(self, values):
        for n, row_values in enumerate(values):
            row_cells = self.rows[n]
            for m, cell in enumerate(row_cells[1:]):
                cell.configure(text=row_values[m])

        
class custom_dialog(dialog):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        font = generate_font(size=33, weight=tk.font.NORMAL)
        font_ = generate_font(size=25)
        tk.Label(self, text='Custom settings', bg='white', fg='black', bd=4, font=('Century Gothic Bold', 40)).grid(column=0, row=0, columnspan=4, sticky='WE')
        self.col_num = tk.Label(self, text='Columns:', bg='white',  fg='black', font=font, justify=tk.LEFT)
        self.col_num.grid(column=0, row=1, sticky='NSWE')
        self.col_entry = entry(self)
        self.col_entry.grid(column=1, row=1, sticky='NSWE')
        self.row_num = tk.Label(self, text='Rows:', bg='white', fg='black', font=font, justify=tk.LEFT)
        self.row_num.grid(column=2, row=1, sticky='NSWE')
        self.row_entry = entry(self)
        self.row_entry.grid(column=3, row=1, sticky='NSWE')
        self.shuffle_times = tk.Label(self, text='Shuffle times:', bg='white', fg='black', font=font, justify='left')
        self.shuffle_times.grid(column=0, row=2, columnspan=2, sticky='WE')
        self.shuffle_times_entry = entry(self, max=5)
        self.shuffle_times_entry.grid(column=2, row=2, columnspan=2, sticky='NSWE')
        self.start_btn = button(self, text='Start', bd=0, font=font_, command=self.master.master.custom_play)
        self.start_btn.grid(column=0, row=3, columnspan=2 ,sticky='NSWE')
        self.cancel_btn = button(self, text='Cancel', bd=0, font=font_, command=self.back)
        self.cancel_btn.grid(column=1, row=3, columnspan=3, sticky='NSWE')
        self.align()

    def get_settings(self):
        if self.col_entry.verify_char() or self.row_entry.verify_char() or self.shuffle_times_entry.verify_char():
            return False
        else:
            try:
                col = int(self.col_entry.get_value())
                row = int(self.row_entry.get_value())
            except:
                col,row= 1,1
            try:
                shuffle_times = int(self.shuffle_times_entry.get_value())
            except:
                shuffle_times = None
            return col, row, shuffle_times


class winner_dialog(dialog):
    def __init__(self, master=None, time=0, move=0, level=0, shuffle_times=0, mode='Normal'):
        super().__init__(master)
        font = generate_font(size=25)
        font_ = generate_font(size=48)
        font__ = generate_font(size=20, weight=tkinter.font.NORMAL)
        date = get_date()
        tk.Label(self, text='Congratulations!', font=font_, bg='white', fg='black', bd=18).grid(column=0, row=0, columnspan=2, sticky='EW')
        tk.Label(self, text='You have completed NUMSKI !!!', font=font, bg='white', fg='black', bd=5).grid(column=0, row=1, columnspan=2, sticky='EW')
        win_info = "Time:%.5fs  Move:%d\nLevel:%s  Shuffle times:%d\nGamemode:%s\nDate:%s"%(time, move, level, shuffle_times, mode, date)        
        tk.Label(self, text=win_info, font=font__, bg='white', fg='black', bd=5).grid(column=0, row=2, columnspan=2, sticky='EW')
        self.exit_btn = button(self, text='Home', bd=5, font=font, command=self.master.destroy)

        self.new_game = button(self, text='New game', bd=5, font=font)
        self.exit_btn.grid(column=0, row=3, sticky=tk.EW)
        self.new_game.grid(column=1, row=3, sticky=tk.EW)
        self.align()
##        exit_btn.bind('<Button-1>', lambda event: self.close())
##        self.cancel.bind('<Button-1>', lambda event: self.close())

class suspend_dialog(dialog):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        font = generate_font(size=40)
        font_ = generate_font(size=33, weight=tkinter.font.NORMAL)
        tk.Label(self, text='Menu', bg='white', fg='black', font=font, bd=12).grid(column=0, row=0, sticky='EW')
        self.home = button(self, text='Home', font=font_, bd=5)
        self.home.grid(column=0, row=1, sticky='EW')
        self.exit = button(self, text='Exit', font=font_, bd=5, command=self.master_exit)
        self.exit.grid(column=0, row=2, sticky='EW')
        self.resume = button(self, text='Resume', font=font_, bd=5, command=self.back)
        self.resume.grid(column=0, row=3, sticky='EW')
        self.settings = button(self, text='Settings', font=font_, bd=5)
        self.settings.grid(column=0, row=4, sticky='EW')
        self.align()
        self.unbind('<Escape>')
##        self.bind('<Escape>', lambda event: self.back())
        
    def master_exit(self):
        self.master.destroy()

class shuffling_dialog(dialog):
    def __init__(self, master=None):
        super().__init__(master)
        self.unbind('<KeyRelease-Escape>')
        self.master = master
        self.master.attributes('-alpha', 0.6)
        font = generate_font(size=33)
        font_ = generate_font(weight=tkinter.font.NORMAL)
        self.title = tk.Label(self, text='Shuffling...', fg='black', font=font, bg='white', bd=6)
        self.title.grid(column=0, row=0, columnspan=7, sticky='NSEW')
        tk.Label(self, bg='white', bd=6).grid(column=0, row=1, sticky='NSEW')
        self.time_label = tk.Label(self, text='Time used:', font=font_, bg='white', fg='black')
        self.time_label.grid(column=1, row=1, sticky='NSEW')
        self.time = tk.Label(self, textvariable=self.master.numski.time_used, font=font_, bg='white', fg='black')
        self.time.grid(column=2, row=1, sticky='NSEW')
        self.shuffle_label = tk.Label(self, text='Shuffle times:', font=font_, fg='black', bg='white')
        self.shuffle_label.grid(column=3, row=1, sticky='NSEW')
        self.shuffle_times = tk.Label(self, textvariable=self.master.numski.count_var, font=font_, bg='white', fg='black', bd=0)
        self.shuffle_times.grid(column=4, row=1, sticky='NSEW')
        self.total_times = tk.Label(self, text='/%d'%self.master.numski.shuffle_times,font=font_, bg='white', fg='black', bd=0)
        self.total_times.grid(column=5, row=1, sticky='NSEW')
        tk.Label(self, bg='white', bd=6).grid(column=6, row=1, sticky='NSEW')
        self.progress_bar = progressbar(master=self, maximum=self.master.numski.shuffle_times, length=25)
        self.progress_bar.grid(column=0, row=2, columnspan=7, sticky='NSEW')
        self.pro_bar_thread = Thread(target=self.set_progressbar)
##        thread.start()

    def done(self):
        self.title['text'] = 'Done!'
        self.progress_bar.set_value(self.master.numski.shuffle_times)

    def set_progressbar(self):
        while self.master.numski.status:
            self.progress_bar.set_value(self.master.numski.count)
            sleep(0.01)

def trans(matrix):
    result = []
    for n in range(0, len(matrix[0])):
        col = []
        for row in matrix:
            col += [row[n]]
        result += [col]
    return result

def test(event):
    print(event.char, event.widget, event.type, event.keycode, event.num, event.delta)

##class settings_dialog():
##    def __init__(self, window, size=None):


if __name__ == '__main__':
    window = tk.Tk()
    window.wm_overrideredirect(0)
    font = generate_font()
##    probar = progressbar(master=window, maximum=100, length=15)
##    probar.set_value(50)
##    probar.pack()
##    s = custom_dialog(window)
##    print(get_date())
##    winner = winner_dialog(window)
##    suspend = shuffling_dialog(window)
    b = button(master=window, text='test', font=font, command=get_date)
    b.pack()
    button(master=window, text='test', font=font, command=lambda : print('test')).pack()
    
    s_ = switch(master=window, status=True, cmds=[lambda:print(), lambda:print()])
    s = switch(master=window, cmds=[lambda:s_.set_disabled(), lambda:s_.set_enabled()])
    s__ = switch(master=window, cmds=[lambda:s.set_enabled(), lambda:s.set_disabled()])
    s.pack()
    s_.pack()
    s__.pack()
    e = entry(window, max=5)
    e.pack()
    e_ = entry(window, max=15)
    e_.pack()
    window.mainloop()

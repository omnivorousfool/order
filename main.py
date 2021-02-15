import tkinter as tk
import numski
import datetime
from widgets import generate_font, dialog, custom_dialog, main_window, button
from windows import about, play, records

img_set = None

class main_menu(main_window):
    def __init__(self, size=(1380, 860)):
        super().__init__(size)
        global img_set
        
        img_set = (
            tk.PhotoImage(file='GUI\GUI_frame.png'),    #0
            tk.PhotoImage(file='GUI\GUI_bar.png'),      #1
            tk.PhotoImage(file='GUI\GUI_min.png'),      #2
            tk.PhotoImage(file='GUI\GUI_close.png'),    #3
            tk.PhotoImage(file='GUI\GUI_numski.png'),   #4
            tk.PhotoImage(file='GUI\GUI_play.png'),     #5
            tk.PhotoImage(file='GUI\GUI_play_a.png'),      #6
            tk.PhotoImage(file='GUI\GUI_records.png'),     #7
            tk.PhotoImage(file='GUI\GUI_settings.png'),    #8
            tk.PhotoImage(file='GUI\GUI_about.png'),       #9
            tk.PhotoImage(file='GUI\GUI_hide.png'),        #10
            tk.PhotoImage(file='GUI\GUI_records_a.png'),   #11
            tk.PhotoImage(file='GUI\GUI_settings_a.png'),  #12
            tk.PhotoImage(file='GUI\GUI_about_a.png'),     #13
            tk.PhotoImage(file='GUI\GUI_numski_a.png'),    #14
            )
        
        # GUI layout
        tk.Label(self, image=img_set[0], bd=0).place(x=0, y=0)   #frame

        self.GUI_bar = tk.Label(self, image=img_set[1], bd=0)
        self.GUI_bar.pack(side='left', anchor='n')
        self.GUI_bar.bind('<Enter>', self.move_window)
        self.GUI_bar.bind('<Leave>', self.move_window)
        self.GUI_bar.bind('<ButtonPress-1>', self.move_window)
        self.GUI_bar.bind('<ButtonRelease-1>', self.move_window)
        self.GUI_bar.bind('<B1-Motion>', self.move_window)
        self.GUI_bar.focus_set()

        self.GUI_numski = tk.Label(self, image=img_set[4], bd=0, takefocus=True)
        self.GUI_numski.place(x=71, y=70)
        self.basic_bind(self.GUI_numski, self.numski_bind)
        
        self.GUI_play = tk.Label(self, image=img_set[5], bd=0, takefocus=True)
        self.GUI_play.place(x=82, y=240)
        self.basic_bind(self.GUI_play, self.play_bind)

        self.GUI_records = tk.Label(self, image=img_set[7], bd=0, takefocus=True)
        self.GUI_records.place(x=670, y=94)
        self.basic_bind(self.GUI_records, self.records_bind)
        
        self.GUI_settings = tk.Label(self, image=img_set[8], bd=0, takefocus=True)
        self.GUI_settings.place(x=671, y=630)
        self.basic_bind(self.GUI_settings, self.settings_bind)
        
        self.GUI_about = tk.Label(self, image=img_set[9], bd=0, takefocus=True)
        self.GUI_about.place(x=1144, y=94)
        self.basic_bind(self.GUI_about, self.about_bind)
        
        self.GUI_min = tk.Label(self, image=img_set[10], bd=0)
        self.GUI_min.place(x=1294, y=22)
        self.GUI_min.bind('<Enter>', self.ctrl_bind)
        self.GUI_min.bind('<Leave>', self.ctrl_bind)
        self.GUI_min.bind('<Button-1>', self.minimize)
                
        self.GUI_close = tk.Label(self, image=img_set[10], bd=0)
        self.GUI_close.place(x=1334, y=22)
        self.GUI_close.bind('<Enter>', self.ctrl_bind)
        self.GUI_close.bind('<Leave>', self.ctrl_bind)
        self.GUI_close.bind('<Button-1>', lambda event: self.create_on_close_dialog())

        # key bindings
        self.bind('<KeyRelease-Escape>', lambda event: self.create_on_close_dialog())

        self.align()


    def minimize(self, event):
        
        pass

    def basic_bind(self, widget, func):
        widget.bind('<Enter>', func)
        widget.bind('<Leave>', func)
        widget.bind('<FocusIn>', func)
        widget.bind('<FocusOut>', func)  
        widget.bind('<Button-1>', func)

    def swap_Label_img(self, label, action, img_a, img):
        print(label, action)
        if action == 'Enter' or action == 'FocusIn':
            label['image'] = img_a
        elif action == 'Leave' or action == 'FocusOut':
            label['image'] = img


    def numski_bind(self, event):
        global img_set
        action = str(event.type)
        self.swap_Label_img(self.GUI_numski, action, img_set[14], img_set[4])

    def play_bind(self, event):
        global img_set
        action = str(event.type)
        self.swap_Label_img(self.GUI_play, action, img_set[6], img_set[5])
        if action == 'ButtonPress':
            self.create_select_menu()

    def records_bind(self, event):
        global img_set
        action = str(event.type)
        self.swap_Label_img(self.GUI_records, action, img_set[11], img_set[7])
        if action == 'ButtonPress':
            self.create_records_window()

    def settings_bind(self, event):
        global img_set
        action = str(event.type)
        self.swap_Label_img(self.GUI_settings, action, img_set[12], img_set[8])

    def about_bind(self, event):
        global img_set
        action = str(event.type)
        self.swap_Label_img(self.GUI_about, action, img_set[13], img_set[9])
        if action == 'ButtonPress':
            a = about(master=self)
            a.align()
        
    def ctrl_bind(self, event):
        global img_set
        action = str(event.type)
        self.swap_Label_img(self.GUI_min, action, img_set[2], img_set[10])
        self.swap_Label_img(self.GUI_close, action, img_set[3], img_set[10])

    def create_on_close_dialog(self):
        on_close = dialog(master=self)
        on_close.unbind('<Escape>')
        on_close.bind('<KeyRelease-Escape>', lambda event: on_close.close())
        font = generate_font(size=25)
        tk.Label(on_close, text='Do you want to exit Numski?', font=font, bg='white', fg='black', bd=12).grid(column=0, row=0, columnspan=2)
        button(on_close, text='Exit', bd=5, font=font, command=lambda: self.close(self)).grid(column=0, row=1, sticky=tk.EW)
        button(on_close, text='Cancel', bd=5, font=font, command=on_close.close).grid(column=1, row=1, sticky=tk.EW)
        on_close.align()

    def start_default_play(self, size):
        self.create_play_window(self, size, None)
        self.select.close()

    def custom_play(self, *args):
        try:
            col, row, shuffle_times = self.custom.get_settings()
            print(self.custom.get_settings(), 'test')
        except:
            return None
        self.create_play_window(self, (col, row), shuffle_times, mode='Custom')
        self.custom.close()
        self.select.close()

    def create_custom(self):
        self.custom = custom_dialog(master=self.select)

    def create_select_menu(self):
        self.select = dialog(master=self)
        font = generate_font(size=33, weight=tk.font.NORMAL)
        tk.Label(self.select, text='Select level', bg='white', fg='black', bd=4, font=('Century Gothic Bold', 40)).pack(fill=tk.BOTH, expand=1)
        easy_3x3 = button(self.select, text='Easy: 3x3', bd=10, font=font, command=lambda : self.start_default_play((3,3)))
        easy_3x3.pack(fill=tk.BOTH, expand=1)
        medium_5x5 = button(self.select, text='Medium: 5x5', bd=10, font=font, command=lambda : self.start_default_play((5,5)))
        medium_5x5.pack(fill=tk.BOTH, expand=1)
        hard_7x7 = button(self.select, text='Hard: 7x7', bd=10, font=font, command=lambda : self.start_default_play((7,7)))
        hard_7x7.pack(fill=tk.BOTH, expand=1)
        custom = button(self.select, text='Custom', bd=10, font=font, command=self.create_custom)
        custom.pack(fill=tk.BOTH, expand=1)
        self.select.align()

    def create_play_window(self, master, board_size, shuffle_times, mode='Normal'):
        play(master=self, board_size=board_size, shuffle_times=shuffle_times, mode=mode)


    def create_records_window(self):
        self.records_win = records(master=self)
        self.records_win.attributes('-alpha', 0)
        self.records_win.align()
        
if __name__ == '__main__':
    app = main_menu()
    app.mainloop()

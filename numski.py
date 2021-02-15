import tkinter as tk
from tkinter.constants import SEL_FIRST
import tkinter.font
from tkinter import messagebox
from random import choice
from time import perf_counter, sleep
from threading import Barrier, Thread
from widgets import generate_font, get_date, button, winner_dialog, shuffling_dialog

tileImg = None
tileImg_a = None
spaceImg = None
barrierImg = None


class numski(tk.Frame):
    def __init__(self, size=(5,5), shuffle_times=None, mode='Normal', master=None, gamerule=0):
        '''
        gamerule: 0 == classical,  1 == barrier
        '''
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        self.master.grab_set()
        self.size_x, self.size_y = size[0], size[1]
        self.length = self.size_x*self.size_y
        if shuffle_times == None:            
            self.shuffle_times = self.length**2
        else:
            self.shuffle_times = shuffle_times
        self.mode = mode
        self.gamerule = gamerule
        self.list_finish = [i for i in range(1,self.length)]
        self.list_finish.append(0)
        self.list_play = [i for i in range(1,self.length)]
        self.font = generate_font()
        self.create_tiles()
        self.arrange_tiles()
        self.status = 0
        self.last_dest = 0
        self.space_pos = self.length - 1
        self.time_thread = Thread(target=self.timer)
        self.shuffle_thread = Thread(target=self.shuffle_tiles, args=(self.shuffle_times,None))
        self.count = 0
        self.count_var = tk.StringVar(self)
        self.count_var.set("0")
        self.time_used = tk.StringVar(self)
        self.time_used.set("0")
##        self.shuffle_thread.start()
        self.count_font = generate_font(size=12)

    def barrier_rule_init(self):
        global barrierImg
        self.gamerule = 1
        barrierImg = tk.PhotoImage(file='GUI/GUI_barrier.png')
        self.barriers = [0 for i in range(0, self.length)]
        self.master.bind('<Button-1>', self.set_barrier)

    def set_barrier(self, event):
        global barrierImg
        tile = event.widget
        tile_pos = self.get_tile_pos(tile)
        if tile_pos != self.space_pos:
            self.barriers[tile_pos] = 0
            tile.configure(text='', image=barrierImg)
            tile.unbind('<Enter>')
            tile.unbind('<Leave>')
            tile.unbind('<FocusIn>')
            tile.unbind('<FocusOut>')
            print('%d set barrier' % tile_pos)
        else:
            print('%d cannot set barrier as it is space' % tile_pos)
            return None
        


    def bind_keys(self):
        self.master.bind('<Key-Up>', lambda event: self.key_move(1))
        self.master.bind('<Key-Down>', lambda event: self.key_move(3))
        self.master.bind('<Key-Left>', lambda event: self.key_move(0))
        self.master.bind('<Key-Right>', lambda event: self.key_move(2))
        self.master.bind('<Key-a>', lambda event: self.key_move(0))
        self.master.bind('<Key-w>', lambda event: self.key_move(1))
        self.master.bind('<Key-d>', lambda event: self.key_move(2))
        self.master.bind('<Key-s>', lambda event: self.key_move(3))
        
        
    def create_tiles(self):
        global tileImg, spaceImg, tileImg_a
        self.tiles = []
        tileImg = tk.PhotoImage(file='GUI/GUI_tile.png')
        spaceImg = tk.PhotoImage(file='GUI/GUI_space.png')
        tileImg_a = tk.PhotoImage(file='GUI/GUI_tile_a.png')
        for i in self.list_play:
            tile = button(self,
                            text='%s'%i,
                            image=tileImg,
                            font=self.font,
                            compound=tk.CENTER,
                            bd=0,
                            changebg=False
                            )
            tile.bind('<Enter>', self.tile_bind)
            tile.bind('<Leave>', self.tile_bind)
            tile.bind('<FocusIn>', self.tile_bind, '+')
            tile.bind('<FocusOut>', self.tile_bind, '+')
            tile.unbind('<ButtonPress-1>')
            tile.unbind('<ButtonRelease-1>')
            self.tiles.append(tile)
        self.space = tk.Label(self,
                              image=spaceImg,
                              bd=0,
                              fg='black',
                              bg='white'
                              )
        self.tiles.append(self.space)
        self.list_play.append(0)
            
    def arrange_tiles(self):
        for i in range(0, self.length):
            self.tiles[i].grid(column=i%self.size_x, row=i//self.size_x, padx=0, pady=0)
        
    def generate_pos(self, current_pos):
        dests = list(filter(self.check_dest, [current_pos+1, current_pos-1, current_pos+self.size_x, current_pos-self.size_x]))
        print('?->%d:' % current_pos, dests)
        if len(dests) == 0:
            return self.last_dest
        else:
            dest = choice(dests)
            return dest

    def move_to(self, dest, check=True, **kw):
        if check:
            if self.check_dest(dest, **kw):
                self.move_to(dest, check=False)
                return True
            else:
                print('%d!->%d' % (self.space_pos, dest))
                return False
        else:
            print('%d->%d' % (self.space_pos, dest))
            self.last_dest = self.space_pos
            dest_num = self.list_play[dest]
            dest_tile = self.tiles[dest]
            self.space_pos = dest
            self.swap_tiles(self.space, dest_tile)
            self.swap_list(0, dest_num, self.list_play)
            self.swap_list(self.space, dest_tile, self.tiles)


    def check_dest(self, dest, from_space=True, dest_col=None, dest_row=None):  ## check the destination of tile or space
        space_col, space_row = self.pos_to_col_row(self.space_pos)
        if self.gamerule == 0:
            verify_statment_1 = lambda dest, dest_col, dest_row, space_col, space_row:\
                 dest < self.length and dest >= 0 and (dest_col == space_col or dest_row == space_row) and dest != self.last_dest
            verify_statment_2 = lambda dest, dest_col, dest_row, space_col, space_row:\
                dest < self.length and dest >= 0 and delta in [-1,1,-self.size_x,self.size_x] and (dest_col == space_col or dest_row == space_row)
        elif self.gamerule == 1:
            verify_statment_1 = lambda dest, dest_col, dest_row, space_col, space_row:\
                 dest < self.length and dest >= 0 and (dest_col == space_col or dest_row == space_row) and dest != self.last_dest and (not self.barriers[dest])
            verify_statment_2 = lambda dest, dest_col, dest_row, space_col, space_row:\
                dest < self.length and dest >= 0 and delta in [-1,1,-self.size_x,self.size_x] and (dest_col == space_col or dest_row == space_row) and (not self.barriers[dest])      
        if from_space:
            dest_col, dest_row = self.pos_to_col_row(dest)
##            last_dest = self.last_direct
##            print('last:%d' % self.last_dest)
            # if dest < self.length and dest >= 0 and (dest_col == space_col or dest_row == space_row) and dest != self.last_dest:
            if verify_statment_1(dest, dest_col, dest_row, space_col, space_row):
                return True
            else:
                return False
        else:
            if dest_col == None and dest_row == None:
                dest_col, dest_row = self.pos_to_col_row(dest)
            delta = dest - self.space_pos
            # if dest < self.length and dest >= 0 and delta in [-1,1,-self.size_x,self.size_x] and (dest_col == space_col or dest_row == space_row):
            if verify_statment_2(dest, dest_col, dest_row, space_col, space_row):
                return True
            else:
                return False

    def key_move(self, key):
        print('key move')
        if self.count == 0:
            self.status = 1
            thread = Thread(target=self.timer)
            thread.start()
        if key == 0:  # Key: A Left
            dest = self.space_pos - 1
            self.key_move_(dest)
        elif key == 1: # Key: W Up
            dest = self.space_pos - self.size_x
            self.key_move_(dest)
        elif key == 2: # Key: D Right
            dest = self.space_pos + 1
            self.key_move_(dest)
        elif key == 3: # Key: S Down
            dest = self.space_pos + self.size_x
            self.key_move_(dest)

    def key_move_(self, dest):
        if self.check_dest(dest, from_space=False):
            self.move_to(dest, check=False)
            self.count += 1
            self.count_var.set("%d" % self.count)
            self.check_win()

    def shuffle_tiles(self, times=None, *args):
        self.status = 1
        self.shuffling = shuffling_dialog(self.master)
        self.shuffling.align()
        self.shuffling.pro_bar_thread.start()
        self.time_thread.start()
        while self.count != self.shuffle_times:
            dest = self.generate_pos(self.space_pos)
            self.move_to(dest, check=False)
            self.count += 1
            self.count_var.set("%d" % self.count)
        self.status = False
        self.master.bind('<Button-1>', func=self.click_to_move)
        self.bind_keys()
        self.shuffling.done()
        sleep(0.7)
        self.shuffling.back()
        self.count = 0
        self.count_var.set('0')

    def get_tile_pos(self, tile):
        return self.co_ords_to_pos([tile.grid_info()['column'], tile.grid_info()['row']])

    def click_to_move(self, event):
        tile = event.widget
        tile_pos = self.get_tile_pos(tile)
        if self.move_to(tile_pos, from_space=False):
            self.count += 1
            self.count_var.set("%d" % self.count)
        if self.count == 1:
            self.status = 1
            thread = Thread(target=self.timer)
            thread.start()
        self.check_win()
    
    def swap_tiles(self, a, b):
        column_b = a.grid_info()['column']
        row_b = a.grid_info()['row']
        column_a = b.grid_info()['column']
        row_a = b.grid_info()['row']
        b.grid_configure(column=column_b, row=row_b)
        a.grid_configure(column=column_a, row=row_a)

    def swap_list(self, a, b, target):
        temp = a
        index_a = target.index(a)
        index_b = target.index(b)
        target[index_a] = b
        target[index_b] = temp

    def pos_to_col_row(self, pos):
        return pos % self.size_x, pos // self.size_x  # col & row

    def co_ords_to_pos(self, coords):
        return coords[0] + coords[1] * self.size_x
    
    def vector_to_pos(self, vector):
        
        col, row = self.pos_to_col_row(self.space_pos)
        new_coords = (col+vector[0], row+vector[1])
        return self.co_ords_to_pos(new_coords)
    
    def tile_bind(self, event):
        global tileImg, tileImg_a
        action = str(event.type)
        tile = event.widget
        if action == 'Enter' or action == 'FocusIn':
            tile['image'] = tileImg_a
        elif action == 'Leave' or action == 'FocusOut':
            tile['image'] = tileImg
            
    def timer(self):
        time = perf_counter()
        while self.status:
            self.time_lapsed = perf_counter() - time
            self.time_used.set("%.5fs" % self.time_lapsed)
            sleep(0.000005)

    def disable_tiles(self):
        self.master.unbind('<Button-1>')
        for i in range(0,8):
            key_bindings = ['a', 'w', 'd', 's', 'Left', 'Up', 'Right', 'Down']
            self.master.unbind('<Key-%s>' % key_bindings[i])

    def write_records(self):
        date = get_date()
        record = '%s,%s,%.5fs,%d,%d,%s' % (date, self.level, self.time_lapsed, self.count, self.shuffle_times, self.mode)
        with open("records.numrcds", 'a') as records:
            records.write(record+'\n')
            
    def check_win(self):
        if self.list_play == self.list_finish:
            self.status = False
            self.level = '%dx%d' % (self.size_x, self.size_y)
            winner = winner_dialog(self.master, time=self.time_lapsed, move=self.count, level=self.level, shuffle_times=self.shuffle_times, mode=self.mode)
            winner.bind('<Escape>', lambda event: self.master.destroy())
##            winner.exit_btn.bind('<Button-1>', lambda event: self.master.destroy())
##            winner.new_game.bind('<Button-1>', lambda event: self.master.destroy())
            self.disable_tiles()
            self.write_records()

    def move_space_to_any_dest(self, vector, method=0, *args):  ## method = 0 col first
        delta_col, delta_row = vector[0], vector[1]             ## method = 1 row first
##        space_col, space_row = self.pos_to_col_row(self.space_pos)
##        delta_col, delta_row = dest_col - space_col, dest_row - space_row
        col_move, row_move = 0, 0
        dest = self.vector_to_pos(vector)
        print('%d=>[%d, %d].%d:%d'%(self.space_pos, delta_col, delta_row, dest, method))
        if method:
            while row_move != delta_row:
                if delta_row < 0:
                    self.move_to(self.space_pos-self.size_x)
                    row_move -= 1
                else:
                    self.move_to(self.space_pos+self.size_x, from_space=False)
                    row_move += 1
##                sleep(0.5)
            while col_move != delta_col:
                if delta_col < 0:
                    self.move_to(self.space_pos-1, from_space=False)
                    col_move -= 1
                else:
                    self.move_to(self.space_pos+1, from_space=False)
                    col_move += 1
##                sleep(0.5)
        else:
            while col_move != delta_col:
                if delta_col < 0:
                    self.move_to(self.space_pos-1, from_space=False)
                    col_move -= 1
                else:
                    self.move_to(self.space_pos+1, from_space=False)
                    col_move += 1
##                sleep(0.5)
            while row_move != delta_row:
                if delta_row < 0:
                    self.move_to(self.space_pos-self.size_x, from_space=False)
                    row_move -= 1
                else:
                    self.move_to(self.space_pos+self.size_x, from_space=False)
                    row_move += 1
##                sleep(0.5)
##        else:
##            print('%d!=>[%d, %d].%d:%d'%(self.space_pos, delta_col, delta_row, dest, method))
##        
        
        

##    def chose_method(self, delta_row):
##        if delta_row < 0:
##            return 0
##        else:
##            return 1

##    def chose_orient(self, delta_col, delta_row):
##        if delta_col < 0 and delta_row < 0:
##            return ''
##        elif delta_col 
            
        
    def move_near_dest(self, orient, delta_pos):
        '''
        move space to the one of the positions that is close to the dest
        four orientations: 'up', 'down', 'right' and 'left'
        '''
##        method = self.chose_method(delta_pos[1])
##        if delta_pos
                
##        if orient == 'up':
##            if delta_pos[0] == 0:
##                pos = self.space_pos
####                index = choice([0,1])
##                new_pos_list = list(filter(self.check_dest, [pos+1, pos-1]))
##                new_pos = choice(new_pos_list)
##                print('%d:%s'%(new_pos, str(new_pos_list)))
####                new_pos = new_pos_list[index]
##                self.move_to(new_pos)
##                delta_pos[0] += pos - new_pos
##            delta_pos[1] -= 1
##            self.move_space_to_any_dest(delta_pos, method=1)
##        elif orient == 'down':
##            delta_pos[1] += 1
##            self.move_space_to_any_dest(delta_pos, method=1)
##        elif orient == 'right':
##            delta_pos[0] += 1
##            self.move_space_to_any_dest(delta_pos, method=0)
##        elif orient == 'left':
##            delta_pos[0] -= 1
##            self.move_space_to_any_dest(delta_pos, method=0)

        signs = [-1,1]
        directs = [self.size_x, 1]
        up = orient == 'up'
        down = orient == 'down'
        right = orient == 'right'
        sign = down or right
        condi = (up or down)
##        if up or down:
        print(orient)
        if delta_pos[not condi] == 0:
            pos = self.space_pos
##                index = choice([0,1])
            new_pos_list = list(filter(self.check_dest, [pos+directs[condi], pos-directs[condi]]))
            new_pos = choice(new_pos_list)
            print('%d:%s'%(new_pos, str(new_pos_list)))
##                new_pos = new_pos_list[index]
            self.move_to(new_pos, check=False)
            delta_pos[not condi] += (pos - new_pos) / directs[condi]
        delta_pos[condi] += signs[sign]
        dest = self.vector_to_pos(delta_pos)
        self.move_space_to_any_dest(delta_pos, method=condi)
##        else:
##            if delta_pos[1] == 0:

    def move_tile_vertically(self, up=True):
        if up:
            self.move_to(self.space_pos+self.size_x)
            self.move_to(self.space_pos+1)
            self.move_to(self.space_pos-self.size_x)
            self.move_to(self.space_pos-self.size_x)
            self.move_to(self.space_pos-1)
        else:
            self.move_to(self.space_pos-self.size_x)
            self.move_to(self.space_pos+1)
            self.move_to(self.space_pos+self.size_x)
            self.move_to(self.space_pos+self.size_x)
            self.move_to(self.space_pos-1)

    def move_tile_horizontally(self, right=True):
        if right:
            self.move_to(self.space_pos-1)
            self.move_to(self.space_pos-self.size_x)
            self.move_to(self.space_pos+1)
            self.move_to(self.space_pos+1)
            self.move_to(self.space_pos+self.size_x)
        else:
            self.move_to(self.space_pos+1)
            self.move_to(self.space_pos-self.size_x)
            self.move_to(self.space_pos-1)
            self.move_to(self.space_pos-1)
            self.move_to(self.space_pos+self.size_x)

    def move_tile_to_any_pos(self, tile_num, dest, *args):
        dest_col, dest_row = self.pos_to_col_row(dest)
        tile = self.tiles[tile_num]
        tile_col, tile_row = tile.grid_info()['column'], tile.grid_info()['row']
        delta_col, delta_row = dest_col - tile_col, dest_row - tile_row
        col_move, row_move = 0, 0


def create_numski(master, size, shuffle_times):
    app = numski(size=size, shuffle_times=shuffle_times, master=master)
    app.pack()
    
def test(event):
    print('Press', event.keycode)

def create_thread(target, args):
    t = Thread(target=target, args=args)
    t.start()

if __name__ == '__main__':
    root = tk.Tk()
    app = numski(master=root, size=(8,7), mode='Test', shuffle_times=20)
    app.pack()
##    thread = Thread(target=app.move_space_to_any_dest, args=(5,1))
##    thread.start()
##    app.move_space_to_any_dest(5)
##    app.move_tile_to_any_pos(1, 1)
    app.move_space_to_any_dest([-4, 0], method=1)
##    sleep(2)
    app.move_near_dest('down', [0,-5])
    app.move_tile_vertically(up=False)
    app.move_tile_vertically(up=False)
    app.move_tile_vertically(up=False)
    app.move_tile_vertically(up=False)
    app.move_near_dest('right', [0,-1])
    app.move_tile_horizontally()
    app.barrier_rule_init()
    app.barriers[54] = 1
    app.barriers[55] = 1
    app.barriers[20] = 1
    # app.master.bind('<Button-1>', func=app.click_to_move)
    # app.shuffle_thread.start()
    
    root.mainloop()
    

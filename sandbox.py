"""Testing area."""

from collections.abc import Sequence
import typing
import json
import os
import os.path
from tkinter import Tk, ttk, Canvas
from tkinter import TOP, BOTTOM, LEFT, RIGHT, VERTICAL, HORIZONTAL, N, S, W, E, NW, SE, SW
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import sv_ttk
import ttkthemes

IMG_SIDE = 200

def read_card(fname:os.PathLike) -> dict:
    with open(fname, "r") as fd:
        return json.load(fd)


def write_card(data:dict, fname:os.PathLike) -> None:
    with open(fname, "w") as fd:
        json.dump(data, fd)

def test_tk():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()

def test_ttk():
    root = Tk()
    s = ttk.Style()
    theme_list = s.theme_names()
    root.destroy()
    print(theme_list)
    for theme in theme_list:
        print(theme)
        root = Tk()
        s = ttk.Style()
        s.theme_use(theme)
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
        ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
        root.mainloop()

def test_diag_box():
    filename = filedialog.askopenfilename(title='pen')
    print(filename)


def rotate_config(config:typing.Tuple[int], n:int):
    up, down, left, right = config[0], config[1], config[2], config[3]
    for i in range(n % 4):
        up, down, left, right = right, left, up, down
    return up, down, left, right


class Card:
    def __init__(self, config:typing.Tuple[int], name:typing.Union[str, None], img:typing.Union[Image.Image,None]):
        self.up = config[0]
        self.down = config[1]
        self.left = config[2]
        self.right = config[3]
        self.name = name
        if img is not None:
            self.img = img.copy()
        else:
            self.img = None
    
    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return ""
    
    @classmethod
    def from_dict(cls, d:dict):
        im_filename = d.get('im_filename', '')
        if im_filename != '':
            norm_fname = os.path.normpath(im_filename)
            with Image.open(norm_fname) as im:
                return Card(d['config'], d.get('name', None), im.resize((IMG_SIDE, IMG_SIDE)))
        else:
            return Card(d['config'], d.get('name', None), None)
    
    @classmethod
    def from_filename(cls, fname:os.PathLike):
        with open(fname, 'r') as fd:
            return Card.from_dict(json.load(fd))
    
    def get_tk_img(self):
        return ImageTk.PhotoImage(self.img)
    
    def copy(self):
        return Card((self.up, self.down, self.left, self.right), self.name, self.img)
    
    def rotate(self, trigo:int=1):
        nb_trig_rotations = trigo % 4
        new_conf = rotate_config((self.up, self.down, self.left, self.right), nb_trig_rotations)
        return Card(new_conf, self.name, self.img.rotate(nb_trig_rotations*90))




class ImageButton(ttk.Button):
    def __init__(self, master, text, im, comp):
        super().__init__(master, text=text, image=im, compound=comp)
        self.state(('!selected',))
        self.state(('!focus',))
    
    def switch_select(self):
        if self.instate(('!selected',)):
            self.state(('selected', 'pressed'))
        elif self.instate(('selected',)):
            self.state(('!selected',))
        self.state(('!focus',))


class CardButton(ttk.Button):
    def __init__(self, master, card, img, comp=TOP):
        if card.name is not None and card.img is not None:
            super().__init__(master, text=card.name, image=img, compound=comp)
        elif card.name is not None and card.img is None:
            super().__init__(master, text=card.name)
        elif card.name is None and card.img is not None:
            super().__init__(master, image=card.get_tk_img())
        else:
            raise TypeError("Too few defined attributes in object of class Card to make a CardButton out of it.")
        self.card = card
    
    @classmethod
    def on_SelectionFrame(cls, master, card, comp=TOP):
        res = CardButton(master, card, comp)
        res.grid(column=master.nb_widgets % master.columns, row=master.nb_widgets // master.columns)
        master.nb_widgets += 1
        return res
    
    def switch_select(self):
        if self.instate(('!selected',)):
            self.state(('selected', 'pressed'))
        elif self.instate(('selected',)):
            self.state(('!selected',))
        self.state(('!focus',))


class SelectionFrame(ttk.Frame):
    def __init__(self, master, columns=5, padding=0):
        super().__init__(master, padding=padding)
        self.columns = columns
        self.nb_widgets = 0
        self.grid()
    
    def get_selection_list(self):
        return [e.card for  e in self.winfo_children() if e.instate(('selected',))]



def test_image():
    img_fname = os.path.join("img", "awesomeQuote.jpg")
    root = Tk()
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    with Image.open(img_fname) as im:
        img_tk = ImageTk.PhotoImage(im.resize((200,200)).rotate(90))
        test_button = ImageButton(frm, "test", img_tk, comp=TOP)
        test_button.grid(column=1, row=1)
    test_button['command'] = test_button.switch_select
    root.mainloop()


def test_super_frame():
    root = Tk()
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    select = SelectionFrame(frm, columns=3, padding=30)
    select.grid(column=0, row=0)
    l = []
    def endSelection():
        for e in select.get_selection_list():
            l.append(e)
        root.destroy()
    ttk.Button(frm, text="Ok", command=endSelection).grid(column=0, row=1)
    card1 = Card.from_filename(os.path.join("cards", "card1.json"))
    card_list = [card1]
    for i in range(3):
        card_list.append(card_list[-1].rotate())
    i = 0
    trick_garbage_collector = []
    for c in card_list:
        trick_garbage_collector.append(c.get_tk_img())
        new_button = CardButton.on_SelectionFrame(select, c, trick_garbage_collector[-1])
        new_button['command'] = new_button.switch_select
    root.mainloop()


def test_canvas():
    path_to_scid = os.path.abspath(os.path.join("themes", "scidthemes.0.9.3"))
    path_to_scid_themes = os.path.abspath(os.path.join("themes", "scidthemes.0.9.3", "scidthemes.tcl"))
    # print(path_to_scid)
    path_to_aw = os.path.abspath(os.path.join("themes", "awthemes-10.4.0"))
    root = Tk()
    # root.tk.call('lappend', 'auto_path', path_to_scid)
    # root.tk.call('source', path_to_scid_themes)
    # root.tk.call('package', 'require', 'scidsand')
    # root.tk.call('lappend', 'auto_path', path_to_aw)
    # root.tk.call('package', 'require', 'awdark')
    # sv_ttk.set_theme('dark')
    ttkthemes.ThemedStyle(root, theme="adapta")
    # s = ttk.Style()
    # s.theme_use('awdark')
    # s.theme_use('scidsand')
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    can = Canvas(frm, height=int(1.5*IMG_SIDE), confine=True, background='#000000')
    can.grid(column=0, row=0)
    sbar = ttk.Scrollbar(frm, orient=VERTICAL, command=can.yview)
    sbar.grid(column=1, row=0, sticky=N+S)
    can['yscrollcommand'] = sbar.set
    pad_select = 30
    select = SelectionFrame(can, columns=3, padding=pad_select)
    can.create_window(0, 0, anchor=NW, window=select)
    l = []
    def endSelection():
        for e in select.get_selection_list():
            l.append(e)
        root.destroy()
    sep = ttk.Separator(frm, orient=HORIZONTAL)
    sep.grid(column=0, row=1, sticky=E+W)
    ttk.Button(frm, text="Ok", command=endSelection).grid(column=0, row=2)
    card1 = Card.from_filename(os.path.join("cards", "card1.json"))
    card_list = [card1]
    for i in range(3):
        card_list.append(card_list[-1].rotate())
    i = 0
    trick_garbage_collector = []
    for c in card_list:
        trick_garbage_collector.append(c.get_tk_img())
        new_button = CardButton.on_SelectionFrame(select, c, trick_garbage_collector[-1])
        new_button['command'] = new_button.switch_select
    button_width = new_button.winfo_reqwidth()
    button_height = new_button.winfo_reqheight()
    total_width = button_width * min(select.nb_widgets, select.columns) + 2 * pad_select
    total_height = button_height * (select.nb_widgets // select.columns + 1) + 2 * pad_select
    can['width'] = total_width
    can['scrollregion'] = (0, 0, total_width, total_height)
    root.mainloop()

    


# test_diag_box()
# test_ttk()
# test_image()
# test_super_frame()
test_canvas()
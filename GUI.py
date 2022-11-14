import typing
from tkinter import Tk, ttk, Canvas
from tkinter import TOP, BOTTOM, LEFT, RIGHT, VERTICAL, HORIZONTAL, N, S, W, E, NW, SE, SW, CENTER
from tkinter import PhotoImage
from PIL import Image, ImageTk
import ttkthemes
import sv_ttk
from data_structures import Card, IMG_SIDE
from math_utils import opti_factors
from utils import var_names_to_tuples


class CardButton(ttk.Button):
    def __init__(self, master, card:Card, img:ImageTk.PhotoImage, comp=TOP):
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
    def on_SelectionFrame(cls, master, card:Card, img:ImageTk.PhotoImage, comp=TOP):
        res = CardButton(master, card, img, comp)
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
        return [e.card for e in self.winfo_children() if e.instate(('selected',))]


class NbCardsFrame(ttk.Frame):
    def __init__(self, master, columns=5, padding=0):
        super().__init__(master, padding=padding)
        self.columns = columns
        self.nb_widgets = 0
        self.grid()
    
    def get_cards_nb_list(self):
        return [(e.card, e.get_field_value()) for e in self.winfo_children()]



class SelNbCard(ttk.Frame):
    def __init__(self, master, c:Card, img:ImageTk.PhotoImage, padding:int=30):
        super().__init__(master, padding=padding)
        self.grid()
        self.card = c
        self.picture = ttk.Label(self, image=img)
        self.picture.grid(row=0, column=0)
        field_values = list(map(str, range(1, 11)))
        self.field = ttk.Combobox(self, values=field_values)
        self.field.grid(row=1, column=0)
        self.field.set("1")
    
    def get_field_value(self):
        return int(self.field.get())
    
    @classmethod
    def on_NbCardsFrame(self, master, c:Card, img:ImageTk.PhotoImage, padding:int=30):
        res = SelNbCard(master, c, img, padding)
        res.grid(column=master.nb_widgets % master.columns, row=master.nb_widgets // master.columns)
        master.nb_widgets += 1
        return res



def card_selection(full_list):
    root = Tk()
    root.title("Vous n'imaginez pas tout ce que tkinter peut faire pour vous")
    ttkthemes.ThemedStyle(root, theme="adapta")
    # sv_ttk.set_theme("dark")
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    can = Canvas(frm, confine=True, background='#000000')
    can.grid(column=0, row=0)
    sbar = ttk.Scrollbar(frm, orient=VERTICAL, command=can.yview)
    sbar.grid(column=1, row=0, sticky=N+S)
    can['yscrollcommand'] = sbar.set
    pad_select = 30
    select = SelectionFrame(can, columns=3, padding=pad_select)
    can.create_window(0, 0, anchor=NW, window=select)
    subset = []
    def endSelection():
        for e in select.get_selection_list():
            subset.append(e)
        root.destroy()
    sep = ttk.Separator(frm, orient=HORIZONTAL)
    sep.grid(column=0, row=1, sticky=E+W)
    ttk.Button(frm, text="Ok", command=endSelection).grid(column=0, row=2)
    trick_garbage_collector = []
    for c in full_list:
        trick_garbage_collector.append(c.get_tk_img())
        new_button = CardButton.on_SelectionFrame(select, c, trick_garbage_collector[-1])
        new_button['command'] = new_button.switch_select
    root.update_idletasks()
    can['width'] = select.winfo_reqwidth()
    can['height'] = min(2 * IMG_SIDE, select.winfo_reqheight())
    can['scrollregion'] = (0, 0, select.winfo_reqwidth(), select.winfo_reqheight())
    root.mainloop()
    return subset


def select_nb_cards(subset:typing.List[Card]):
    root = Tk()
    root.title("Vous n'imaginez pas tout ce que tkinter peut faire pour vous")
    ttkthemes.ThemedStyle(root, theme="adapta")
    # sv_ttk.set_theme("dark")
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    can = Canvas(frm, confine=True, background='#000000')
    can.grid(column=0, row=0)
    sbar = ttk.Scrollbar(frm, orient=VERTICAL, command=can.yview)
    sbar.grid(column=1, row=0, sticky=N+S)
    can['yscrollcommand'] = sbar.set
    pad_select = 30

    nb_cards_frm = NbCardsFrame(can, columns=3, padding=pad_select)
    can.create_window(0, 0, anchor=NW, window=nb_cards_frm)
    tuning_list = []
    def endTuning():
        for e in nb_cards_frm.get_cards_nb_list():
            tuning_list.append(e)
        root.destroy()
    sep = ttk.Separator(frm, orient=HORIZONTAL)
    sep.grid(column=0, row=1, sticky=E+W)
    ttk.Button(frm, text="Ok", command=endTuning).grid(column=0, row=2)
    trick_garbage_collector = []
    for c in subset:
        trick_garbage_collector.append(c.get_tk_img())
        new_tuning_frm = SelNbCard.on_NbCardsFrame(nb_cards_frm, c, trick_garbage_collector[-1])
    root.update_idletasks()
    can['width'] = nb_cards_frm.winfo_reqwidth()
    can['height'] = min(2 * IMG_SIDE, nb_cards_frm.winfo_reqheight())
    can['scrollregion'] = (0, 0, nb_cards_frm.winfo_reqwidth(), nb_cards_frm.winfo_reqheight())
    root.mainloop()
    return tuning_list


def select_solve_mode(nb_cards:int):
    p, q = opti_factors(nb_cards)
    root = Tk()
    root.title("Definition du motif a remplir")
    ttkthemes.ThemedStyle(root, theme="adapta")
    frm = ttk.Frame(root, padding=30)
    frm.grid()
    info_str = ("Selection du motif a remplir :\n"
        "Motif automatique (rectangle au plus proche du carre)\n"
        "ou motif personnalise")
    info_lab = ttk.Label(frm, anchor=CENTER, justify=CENTER, padding=30, text=info_str)
    info_lab.grid(row=0, column=0)
    snd_frm = ttk.Frame(frm, padding=30)
    snd_frm.grid(row=1, column=0)
    snd_frm.grid()
    auto_str = "Automatique :\nGrille " + str(p) + "x" + str(q)
    auto_lab = ttk.Label(snd_frm, anchor=CENTER, justify=CENTER, padding=30, text=auto_str)
    auto_lab.grid(row=0, column=0)
    custom_str = "Motif personnalise :\nSelection case par case"
    custom_lab = ttk.Label(snd_frm, anchor=CENTER, justify=CENTER, padding=30, text=custom_str)
    custom_lab.grid(row=0, column=1)
    decide_list = []
    def auto_set():
        decide_list.append('auto')
        root.destroy()
    def custom_set():
        decide_list.append('custom')
        root.destroy()
    auto_button = ttk.Button(snd_frm, text="Go", command=auto_set)
    auto_button.grid(row=1, column=0)
    custom_button = ttk.Button(snd_frm, text="Go", command=custom_set)
    custom_button.grid(row=1, column=1)
    root.mainloop()
    pattern = {}
    if decide_list[0] == 'auto':
        for y in range(p):
            for x in range(q):
                pattern[(x, y)] = True
    else:
        print("Not handled case")
    return pattern


def final_pattern(var_name_list, var_dict, max_side:int=900):
    card_key_tuples = var_names_to_tuples(var_name_list)
    # print(card_key_tuples)
    mx = min(card_key_tuples, key=(lambda x: x[1][0]))[1][0]
    Mx = max(card_key_tuples, key=(lambda x: x[1][0]))[1][0]
    my = min(card_key_tuples, key=(lambda x: x[1][1]))[1][1]
    My = max(card_key_tuples, key=(lambda x: x[1][1]))[1][1]
    Dx = Mx - mx + 1
    Dy = My - my + 1
    side = max_side // max(Dx, Dy)
    pic = Image.new('RGB', (Dx * side, Dy * side))
    for v_name, key in card_key_tuples:
        pos = (side * (key[0] - mx), side * (My - key[1]))
        pic.paste(var_dict[v_name].get_img().resize((side, side)), pos)
    return pic
from collections.abc import Sequence
import typing
import json
import os
import os.path
from PIL import Image, ImageTk
from math_utils import rotate_config, keep_configs

IMG_SIDE = 300

class Card:
    def __init__(self, config:typing.Tuple[int], name:str="", img:typing.Union[Image.Image,None]=None):
        self.up = config[0]
        self.left = config[1]
        self.down = config[2]
        self.right = config[3]
        self.name = name
        if img is not None:
            self.img = img
        else:
            self.img = None
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
    @classmethod
    def from_dict(cls, d:dict):
        im_filename = d.get('im_filename', '')
        if im_filename != '':
            norm_fname = os.path.normpath(im_filename)
            with Image.open(norm_fname) as im:
                return Card(d['config'], d.get('name', ""), im.copy())
        else:
            return Card(d['config'], d.get('name', ""))
    
    @classmethod
    def from_file(cls, fname:os.PathLike):
        with open(fname, 'r') as fd:
            return Card.from_dict(json.load(fd))
    
    def to_dict(self, im_fname:typing.Union[os.PathLike, None]=None):
        d = {'config':(self.up, self.left, self.down, self.right)}
        if self.name != "":
            d['name'] = self.name
        if im_fname is not None:
            d['im_filename'] = im_fname
        return d
    
    def to_file(self, fname:os.PathLike, im_fname:typing.Union[os.PathLike, None]=None):
        if im_fname is not None and self.img is not None:
            self.img.save(im_fname)
        with open(fname, 'w') as fd:
            json.dump(self.to_dict(im_fname), fd)
    
    def get_tk_img(self, size=(IMG_SIDE, IMG_SIDE)):
        return ImageTk.PhotoImage(self.img.resize(size))
    
    def copy(self):
        return Card(self.get_config(), self.name, self.img.copy())
    
    def get_config(self):
        return (self.up, self.left, self.down, self.right)
    
    def rotate(self, turns:int=1):
        new_conf = rotate_config(self.get_config(), turns % 4)
        return Card(new_conf, self.name, self.img.rotate((turns % 4) * 90))


class CardPool:
    nb_cp = 0
    def __init__(self, c:Card, n:int=1):
        CardPool.nb_cp += 1
        self.id = CardPool.nb_cp
        self.number = n
        self.parent = c
        config = c.get_config()
        self.sym_ind = keep_configs(config)
        self.name = "CP" + str(self.id) + "(" + str(self.parent) + ")"
        self.v_card_list = []
        for i in range(self.sym_ind):
            self.v_card_list.append( vCard(parent=self, config=config, idx=i) )
            config = rotate_config(config)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def rotate_card(self, idx:int, turns:int=1):
        return self.v_card_list[(idx+turns) % self.sym_ind]
    
    def __iter__(self):
        return self.v_card_list.__iter__()


class vCard:
    nb_c = 0
    def __init__(self, parent:CardPool, config:typing.Tuple[int], idx:int):
        vCard.nb_c += 1
        self.id = vCard.nb_c
        self.parent = parent
        self.idx = idx
        self.name = "c" + str(self.id) + "(" + str(self.parent) + "," + str(self.idx) + ")"
        self.config = config
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
    def __getitem__(self, key):
        assert key == (1,0) or key == (0,1) or key == (-1,0) or key == (0,-1)
        return self.config[2 * ((1 + key[0] - key[1]) // 2) + abs(key[0]) ]
    
    def rotate(self, turns:int=1):
        return self.parent.rotate_card(idx=self.idx, turns=turns)
    
    def get_img(self):
        return self.parent.parent.img.rotate((self.idx) * 90)


class ExtMap:
    def __init__(self, d:dict):
        self.data = d
        self.mx = min(d, key=(lambda x: x[0]))[0]
        self.Mx = max(d, key=(lambda x: x[0]))[0]
        self.my = min(d, key=(lambda x: x[1]))[1]
        self.My = min(d, key=(lambda x: x[1]))[1]
        self.ind_sym = 4
        dil_map = {}
        for key in d:
            dil_map[(2 * key[0] - self.mx - self.Mx, 2 * key[1] - self.my - self.My)] = True
        for key in dil_map:
            if not dil_map.get((-key[1], key[0]), False):
                self.ind_sym = 1
                break
        if self.ind_sym > 2:
            for key in dil_map:
                if not dil_map.get((-key[0], -key[1]), False):
                    self.ind_sym = 2
                    break


    def __iter__(self):
        return self.data.__iter__()
    
    def neighb(self, key:typing.Tuple[int]):
        dx = 1
        dy = 0
        potential_neighb = []
        for i in range(4):
            if self.data.get((key[0]+dx, key[1]+dy), False):
                potential_neighb.append((key[0]+dx, key[1]+dy))
            dx, dy = -dy, dx
        return potential_neighb
    
    def rotate(self, key:typing.Tuple[int], turns:int=1):
        if turns % self.ind_sym != 0:
            raise ValueError(("Not enough symmetries in the "
                "map to rotate a cell this way : "
                "ind_sym = " + str(self.ind_sym) + ", turns = " + str(turns)))
        tx = 2 * key[0] - self.mx - self.Mx
        ty = 2 * key[1] - self.my - self.My
        for i in range(turns % 4):
            tx, ty = -ty, tx
        return (self.mx + self.Mx + tx) // 2, (self.my + self.My + ty) // 2
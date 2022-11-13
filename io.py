import json
import os
import typing


def read_card(fname:os.PathLike) -> dict:
    with open(fname, "r") as fd:
        return json.load(fd)


def write_card(data:dict, fname:os.PathLike) -> None:
    with open(fname, "w") as fd:
        json.dump(data, fd)


def cardQSave(
        fname:os.PathLike, config:typing.Tuple[int],
        name:typing.Union[str, None]=None, 
        imfile:typing.Union[os.PathLike, None]=None
    ) -> None:
    dir = 'cards'
    filename = os.path.join(dir, fname + '.json')
    d = {}
    d['config'] = config
    if name is not None:
        d['name'] = name
    if imfile is not None:
        d['im_filename'] = os.path.join('img', imfile)
    with open(filename, "w") as fd:
        json.dump(d, fd)
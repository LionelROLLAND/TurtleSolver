import typing

def isqrt_sup(n:int, borne_inf:int=0, borne_sup:typing.Union[int, None]=None) -> int:
    if borne_sup is None:
        borne_sup = n
    elif borne_inf == borne_sup:
        return borne_inf
    c = (borne_inf + borne_sup) // 2
    if c ** 2 < n:
        return isqrt_sup(n, c+1, borne_sup)
    return isqrt_sup(n, borne_inf, c)


def isqrt_inf(n:int, borne_inf:int=0, borne_sup:typing.Union[int, None]=None) -> int:
    if borne_sup is None:
        borne_sup = n
    if borne_inf == borne_sup:
        return borne_inf
    c = (borne_inf + borne_sup + 1) // 2
    if c ** 2 > n:
        return isqrt_inf(n, borne_inf, c-1)
    return isqrt_inf(n, c, borne_sup)


def prime_factors(n:int, start:int=2, acc:list=[]) -> typing.List[typing.Tuple[int]]:
    if n == 1:
        return acc
    stop = isqrt_inf(n)
    while start <= stop:
        if n % start == 0:
            exp = 1
            n //= start
            while n % start == 0:
                exp += 1
                n //= start
            return prime_factors(n, start+1, acc + [(start, exp)])
        start += 1
    return [(n, 1)]


def opti_factors(n:int):
    rt = isqrt_inf(n)
    while n % rt != 0:
        rt -= 1
    return rt, n // rt


def rotate_config(config:typing.Tuple[int], n:int=1):
    up, left, down, right = config
    for i in range(n % 4):
        up, left, down, right = right, up, left, down
    return up, left, down, right


def keep_configs(init_config) -> int:
    config = rotate_config(init_config)
    i = 1
    while config != init_config:
        i += 1
        config = rotate_config(config)
    return i
from . import padrao, ce, pi

def calcular_difal(uf_empresa, *args, **kwargs):
    if uf_empresa == "CE":
        return ce.calcular(*args, **kwargs)
    elif uf_empresa == "PI":
        return pi.calcular(*args, **kwargs)
    else:
        return padrao.calcular(*args, **kwargs)

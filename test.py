def test(a, b, c, **kargs): print(f"a = {a}\nb = {b}\nc = {c}")

dict = {"b": 2,
        "c": 3}

test(a = 1, **dict)
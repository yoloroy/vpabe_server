def sum_dicts(a: dict, b: dict):
    for key in b.keys():
        a[key] = b[key]

    return a

d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 3, 'c': 3}

#d3 = **d1

*dd, b = d1

print(dd, type(dd))
d3 = {*d2, *d1}

print(dd)
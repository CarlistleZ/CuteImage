#!/usr/bin/python

FILTERS = {
    0: [(lambda r: r + 180), (lambda g: g + 40), (lambda b: b - 20)],
    1: [(lambda r: r + 50), (lambda g: g + 50), (lambda b: b + 150)],
    2: [(lambda r: r + 10), (lambda g: g + 10), (lambda b: b + 180)],
    3: [(lambda r: r + 10), (lambda g: g + 80), (lambda b: b + 20)],
    4: [(lambda r: r - 20), (lambda g: g - 10), (lambda b: b - 50)],
    5: [(lambda r: r - 50), (lambda g: g - 25), (lambda b: b - 10)],
    6: [(lambda r: r + 35), (lambda g: g + 30), (lambda b: b + 40)],
    7: [(lambda r: r - 20), (lambda g: g + 1), (lambda b: b + 120)],
    8: [(lambda r: r - 50), (lambda g: g - 30), (lambda b: b - 40)],
    9: [(lambda r: r + 50), (lambda g: g + 50), (lambda b: b + 90)],
    10: [(lambda r: r + 30), (lambda g: g + 30), (lambda b: b + 45)],
    11: [(lambda r: r - 20), (lambda g: g - 45), (lambda b: b - 50)]
}
def sum_dresses_price(dresses):
    # dresses: ((size, details, name, price))
    total = 0
    for dress in dresses:
        total += dress[-1]
    return total

def sum_dresses_price(dress_details, dresses):
    # dress_details: ((name, price),...)
    # dresses: ((size, index))
    total = 0
    for dress in dresses:
        deets = dress_details[dress[1]]
        total += deets[1]
    return total

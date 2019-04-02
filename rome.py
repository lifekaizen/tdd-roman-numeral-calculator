ROMAN_NUMERALS = ['I', 'V', 'X']
def add(augend, addend):
    if not isinstance(augend, str) or not isinstance(addend, str):
        raise ValueError

    simple_augend = augend.replace('IX', 'IIIIIIIII').replace('IV', 'IIII')
    simple_addend = addend.replace('IX', 'IIIIIIIII').replace('IV', 'IIII')
    simple_sum = simple_augend + simple_addend

    for char in simple_sum:
        if char not in ROMAN_NUMERALS:
            raise ValueError

    ordered_sum = ''.join(sorted(simple_sum, reverse=True))

    canonicalised_sum = ordered_sum.replace('IIIIIIIIII', 'X').replace('IIIIIIIII', 'IX').replace('IIIII', 'V').replace('VV', 'X').replace('IIII', 'IV').replace('VIV', 'IX')
    if canonicalised_sum == 'VX':
        canonicalised_sum = 'XV'
    if canonicalised_sum == 'VIX':
        canonicalised_sum = 'XIV'
    return canonicalised_sum
__author__ = 'Karl Tiirik'
import datetime


class EstPerson(object):
    def __init__(self, gender, birth_date, nth_baby):
        self.gender = gender
        self.birth_date = birth_date
        self.code = calc_code(gender, birth_date, nth_baby)

    def __str__(self):
        return "%s, %s, %s" % (self.code, self.gender, self.birth_date)


def calc_code(gender, birth_date, nth_baby):
    """ Generates EST ID code """
    century_digit = get_century_digit(birth_date, gender)
    birth_date = format_date(birth_date)
    nth_baby = str(nth_baby).zfill(3)
    id_code = century_digit + birth_date + nth_baby
    id_code += calc_checksum(id_code)
    return id_code


def get_century_digit(date, gender):
    """ Returns gender/century digit according to date and gender """
    year = date.year
    century = []

    if 1800 <= year <= 1899:
        century = ['1', '2']
    elif 1900 <= year <= 1999:
        century = ['3', '4']
    elif 2000 <= year <= 2099:
        century = ['5', '6']

    if gender == 'M':
        return century[0]
    else:
        return century[1]


def format_date(date):
    """ Format date """
    f_date = str(date.year)[2:] + str(date.month).zfill(2) + str(date.day).zfill(2)
    return f_date


def calc_checksum(number):
    """ Calculates checksum using Modulo 11 and weights """
    lvl_1_weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    lvl_2_weights = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    cs = 0

    remainder = modulo_11(number, lvl_1_weights)
    if remainder != 10:
        cs = remainder
    else:
        remainder = modulo_11(number, lvl_2_weights)
        if remainder != 10:
            cs = remainder
    return str(cs)


def modulo_11(number, weights):
    """ Modulo 11 method with weights """
    code = [int(i) for i in number]
    total = sum([x * y for x, y in zip(code, weights)])
    return total % 11


def id_generator(n):
    """ Generates a list with n EstPerson-s with unique codes """
    start_date = datetime.date(1800, 1, 1)
    end_date = datetime.date.today()
    delta = end_date - start_date
    count = 0

    for nth in range(1, 1000):
        for d in range(delta.days + 1):
            if count >= n:
                break
            yield EstPerson('M', start_date + datetime.timedelta(days=d), nth)
            count += 1
            if count >= n:
                break
            yield EstPerson('F', start_date + datetime.timedelta(days=d), nth)
            count += 1


if __name__ == "__main__":
    import cProfile

    cProfile.run('id_generator(1000000)', sort='tottime')

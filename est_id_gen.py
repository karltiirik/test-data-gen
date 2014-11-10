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
    f_date = date.strftime('%Y%m%d')[2:]
    return f_date


def calc_checksum(number):
    """ Calculates checksum using Modulo 11 and weights """
    LVL_1_WEIGHTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    LVL_2_WEIGHTS = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    cs = 0

    remainder = modulo_11(number, LVL_1_WEIGHTS)
    if remainder != 10:
        cs = remainder
    else:
        remainder = modulo_11(number, LVL_2_WEIGHTS)
        if remainder != 10:
            cs = remainder
    return str(cs)


def modulo_11(number, weights):
    """ Modulo 11 method with weights """
    sum = 0

    for i in range(len(number)):
        sum += int(number[i]) * weights[i]
    return sum % 11


def gen_n_persons(n):  # needs optimization
    """ Generates a list with n EstPerson-s with unique codes"""
    start_date = datetime.date(1800, 1, 1)
    end_date = datetime.date.today()
    delta = end_date - start_date
    list_of_persons = []

    for nth in range(1, 1000):
        for d in range(delta.days + 1):
            for g in ['M', 'F']:
                person = EstPerson(g, start_date + datetime.timedelta(days=d), nth)
                list_of_persons.append(person)
                if len(list_of_persons) >= n:
                    break
            if len(list_of_persons) >= n:
                break
        if len(list_of_persons) >= n:
            break
    return list_of_persons

if __name__ == "__main__":
    import cProfile
    cProfile.run('gen_n_persons(1000000)', sort='tottime')

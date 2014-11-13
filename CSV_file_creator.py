__author__ = 'Karl Tiirik'

import csv
import random

from est_id import est_id_gen


def generate_csv_with_n_users(n):
    """ Generates a CSV file with n test persons' data """
    surnames, forenames = read_names('IO files\\names.txt')

    with open('IO files\\test_persons_data.csv', 'w', encoding="utf8") as test_persons:
        wr = csv.writer(test_persons, delimiter=',', lineterminator='\n')
        wr.writerow(['SOCIAL_SECURITY_NUMBER', 'FORENAME', 'SURNAME', 'GENDER', 'DATE_OF_BIRTH'])

        for id_code in est_id_gen.id_generator(n):
            b_date = '%s.%s.%s' % (str(id_code.birth_date.day).zfill(2), str(id_code.birth_date.month).zfill(2),
                                   str(id_code.birth_date.year))
            persons_data = [id_code.code, random.choice(forenames), random.choice(surnames), id_code.gender, b_date]
            wr.writerow(persons_data)


def read_names(file_name):
    """ Read files from csv format, save as list. Removes problematic lines """
    with open(file_name, 'r', encoding='utf8') as names_file:
        raw_list_of_names = names_file.read().splitlines()

    surnames, forenames = [], []
    for i in range(len(raw_list_of_names)):
        try:
            surname, forename = raw_list_of_names[i].split(', ')
            surnames.append(surname)
            forenames.append(forename)
        except ValueError:  # If there is only 1 name
            forenames.append(raw_list_of_names[i])
    return surnames, forenames


if __name__ == '__main__':
    import cProfile

    cProfile.run('generate_csv_with_n_users(1000000)', sort='tottime')  # ~30 seconds, 5.5 MB of RAM
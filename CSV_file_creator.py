__author__ = 'Karl Tiirik'
import est_id_gen
import csv


def generate_csv_with_n_users(n):
    """Generates a CSV file with n test persons' data"""
    list_of_names = read_names("names.txt")
    list_of_est_ids = est_id_gen.gen_n_persons(n)

    with open('test_persons_data.csv', 'w', encoding="utf8") as test_persons:
        wr = csv.writer(test_persons, delimiter=',', lineterminator='\n')
        wr.writerow(["SOCIAL_SECURITY_NUMBER", "FORENAME", "SURNAME", "GENDER", "DATE_OF_BIRTH"])
        for i in range(n):
            forename = list_of_names[i % len(list_of_names)][1]
            surname = list_of_names[i % len(list_of_names)][0]
            persons_data = [list_of_est_ids[i].code, forename, surname,
                            list_of_est_ids[i].gender, list_of_est_ids[i].birth_date.strftime('%d.%m.%Y')]
            wr.writerow(persons_data)


def read_names(file_name):
    """ Read files from csv format, save as list. Removes problematic lines"""
    with open(file_name, "r", encoding="utf8") as names_file:
        raw_list_of_names = names_file.read().splitlines()

    list_of_names = []
    for i in range(len(raw_list_of_names)):
        try:
            surname, forename = raw_list_of_names[i].split(", ")
            list_of_names.append([surname, forename])
        except ValueError:  # If there is only 1 name
            pass
    return list_of_names

if __name__ == "__main__":
    import cProfile
    cProfile.run('generate_csv_with_n_users(1000000)', sort='tottime')  # ~37 seconds
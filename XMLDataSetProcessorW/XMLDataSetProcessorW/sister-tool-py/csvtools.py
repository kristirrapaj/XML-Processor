import csv


class InvalidGroupError(Exception):
    @staticmethod
    def mth_raise_error():
        print(f"The group passed is invalid. \n")


def read_errors_file():
    with open(".\\output\\error.txt", "r") as errorFile:
        with open("output/errorFields.csv", "w+") as fieldFile:
            csv_file = csv.reader(errorFile, delimiter=",")
            unique = []
            for line in csv_file:
                print(line[1])
                if not line[1] in unique:
                    unique.append(line[1])
            for line in unique:
                fieldFile.write(f"{line}\n")


def process_file(file, fields):
    if file is None:
        raise ValueError("file cannot be None")
    if fields is None:
        raise ValueError("fields cannot be None")
    return fn_process_file(file, fields)


def get_field_to_hide(_filepath):
    """
    :param _filepath: Path to file containing fields to hide
    :return fields_to_hide: List of fields to hide
    """
    if _filepath is None:
        raise ValueError("filepath cannot be None")
    return fn_get_field_to_hide(_filepath)


def get_category(_filepath, _group):
    """
    :param _filepath: Path to file containing group/category pairs
    :param _group: Group to get category for
    :return category: Associated category for given group
    :raises InvalidGroupError: If group is not found in file
    """
    if _filepath is None:
        raise ValueError("filepath cannot be None")
    if _group is None:
        raise ValueError("group cannot be None")
    return fn_get_category(_filepath, _group)


def get_fields_groups(_filepath):
    """
    :param _filepath: Path to file containing fields/groups pairs
    :return tuple: Associated category for given group
    :raises ValueError: If filepath is None
    """
    if _filepath is None:
        raise ValueError("filepath cannot be None")
    return fn_get_fields_groups(_filepath)


def fn_get_category(_filepath, _group):
    _groups_list = []

    # Generate list of tuples from csv file
    with open(_filepath, "r", newline='') as file_to_read:
        csv_file = csv.reader(file_to_read, delimiter=',')
        for line in csv_file:
            _groups_list.append((line[0], line[1]))
        file_to_read.close()
    # Search for group in list of tuples
    for item in _groups_list:  # GROUP,CATEGORY
        if _group == item[0]:  # group == "GROUP"
            return item[1]  # CATEGORY
    # If group is not found, raise InvalidGroupError

    raise InvalidGroupError()


def fn_get_field_to_hide(_filepath):
    """
    :param _filepath: Path to file containing fields to hide
    :return fields_to_hide: List of fields to hide
    """
    fields_to_hide = []
    index = 0
    try:
        with open(_filepath, 'r') as _file_to_csv_parse:
            csv_file = csv.reader(_file_to_csv_parse, delimiter=',')
            for line in csv_file:
                if index % 2 == 0:
                    fields_to_hide.append(line)
                index += 1
            _file_to_csv_parse.close()
    except FileNotFoundError:
        return fields_to_hide
    return fields_to_hide


def fn_get_fields_groups(_filepath):
    _result = []
    # Generate list of tuples from csv file
    with open(_filepath, "r", newline='') as file_to_read:
        csv_file = csv.reader(file_to_read, delimiter=',')
        for line in csv_file:
            _result.append((line[0], line[1]))
        file_to_read.close()
    return _result


def fn_process_file(file, fields):
    """
    Process a CSV file and extract data based on specified fields.

    Args:
        file (str): The path to the CSV file.
        fields (list): A list of field names to extract from each row.

    Returns:
        list: A list of extracted data based on the specified fields.
    """
    result = []
    with open(file, "r") as file_to_read:
        csvfile = csv.reader(file_to_read, delimiter=",")
        index = 0
        for row in csvfile:
            if index % 2 == 0:
                fn_process_row(row, fields, file, result)
            index += 1
    return result


def fn_process_row(row, fields, file, result):
    for field in fields:
        if row[0] == field:
            group_name = fn_get_group_name(file)
            field_name = field
            result.append((field_name, group_name))


def fn_get_group_name(file):
    return file.split("\\")[3].split(".")[0]

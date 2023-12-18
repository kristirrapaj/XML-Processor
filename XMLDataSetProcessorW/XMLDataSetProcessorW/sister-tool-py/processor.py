import glob
import xml
from typing import List, Tuple
from xml.dom import minidom
from xml.dom.minidom import parseString

import csvtools

global current_column
global child_list


def set_column_child_node_list(_column):
    global child_list
    child_list = [child for child in current_column]


def add_found_fields():
    """
    This function reads error fields from a file, processes multiple files, and writes the unique results to another file.

    Returns:
        None
    """
    _fields = []
    with open(".\\output\\errorFields.csv", "r") as fieldFile:
        for lineField in fieldFile:
            _fields.append(lineField.split("\n")[0])
        fieldFile.close()
    with open(".\\src\\DATA_FIELDS_NAMES.csv", "a") as dataFieldFile:
        _result = []
        file_list = get_files_visible_editable_nullable()
        for file in file_list:
            _result += csvtools.process_file(file, _fields)
        _unique_result = set(_result)
        for _unique in _unique_result:
            dataFieldFile.write(f"{_unique[0]},{_unique[1]}\n")


def field_empty_in_file(file, field):
    with open(".\\output\\error.txt", "a") as errorFile:
        errorFile.write(f"{file},{field}\n")


class NoFieldFound(Exception):

    def __init__(self, file, field_text):
        field_empty_in_file(file, field_text)


class NoVarError(Exception):
    def __init__(self, file, field):
        field_empty_in_file(file, field)


def change_element_value(_column, _element_name, _new_value, _filepath_to_fields):
    """
    Change the value of an element in a column based on certain conditions.

    Args:
        _column (Element): The column element to modify.
        _element_name (str): The name of the element to modify.
        _new_value (str): The new value to assign to the element.
        _filepath_to_fields (str): The filepath to the fields.

    Returns:
        Element: The modified column element.
    """
    fields_to_hide = csvtools.get_field_to_hide(_filepath_to_fields)
    _assigned_value = ""
    for _field in fields_to_hide:
        if _field[0].startswith(_new_value):
            match _element_name:
                case "EDITABLE":
                    _assigned_value = _field[1]
                case "VISIBLE":
                    _assigned_value = _field[2]
                case "NULLABLE":
                    _assigned_value = _field[3]
    # if the column matches the field to hide, then hide it
    if _assigned_value == "":
        raise ValueError
    for field in child_list:
        if field.nodeName == "DATA_FIELD_NAME" and field.firstChild.data in fields_to_hide:
            field.parentNode.getElementsByTagName(_element_name)[0].firstChild.data = _assigned_value.lower()
    return _column


def get_files_visible_editable_nullable():
    """
    Retrieves a list of files that are visible, editable, and nullable.

    Returns:
        list: A list of file paths.
    """
    directory_files_altro = glob.glob(f".\\src\\Altro\\*.csv")
    directory_files_cfisiche = glob.glob(f".\\src\\Caratteristiche Fisiche\\*.csv")
    directory_files_dettagli = glob.glob(f".\\src\\Dettagli\\*.csv")
    files = []
    for file in directory_files_altro:
        files.append(file)
    for file in directory_files_cfisiche:
        files.append(file)
    for file in directory_files_dettagli:
        files.append(file)
    return files


def get_list_of_elements(_parsed_file, _list_of_elements):
    """

    :param _parsed_file: xml file parsed with minidom.
    :param _list_of_elements: list of elements to search for.
    :return: list of elements with the given tagname.

    Args:
        _list_of_elements:
    """
    if _parsed_file is None or _list_of_elements is None:
        raise ValueError("parsedfile or element_list cannot be None")

    elements = {}
    for element in _list_of_elements:
        elements[element] = [element for element in _parsed_file.getElementsByTagName(_list_of_elements[element])]

    return elements


def assign_group(_matching_file):
    """

    :param _matching_file:  csv file containing the fields and groups.
    :return: list of tuples (DATA_FIELD_NAME, GROUP).
    """
    # Generates a list of tuples from the csv file that matches the data field names with the groups
    # field_group = ("FIELD_NAME", "GROUP")
    test = [field_group for field_group in csvtools.get_fields_groups(_matching_file)]
    return test


def generate_final_list(_filepath, _fields_groups):
    """

    :param _filepath: Filepath containing the groups and categories.
    :param _fields_groups:  List of tuples (DATA_FIELD_NAME, GROUP) to be matched with the categories.
    :return: list of tuples (DATA_FIELD_NAME, GROUP, CATEGORY).
    """
    _result = []
    for group in _fields_groups:
        try:
            category = csvtools.get_category(_filepath, group[1].lower().capitalize())
            _result.append(group + (category,))
        except ValueError:
            pass
        except csvtools.InvalidGroupError:
            csvtools.InvalidGroupError.mth_raise_error()
            return
    return _result


def attach_text_node(_node, _node_text, _file):
    _text_node = _file.createTextNode(_node_text)
    _node.appendChild(_text_node)


def update_column_setting(_groups_fields_categories, _column, _file):
    """
    Update the column setting based on the provided groups, fields, and categories.

    Args:
        _groups_fields_categories (List[Tuple[str, str, str]]): A list of tuples containing the data field name, group, and category.
        _column (Any): The column to be updated.
        _file (Any): The file associated with the column.

    Returns:
        Any: The updated column.
    """
    _group_text, _category_text, _dfn, _cat, _grp = "", "", "", "", ""
    for _tuple in _groups_fields_categories:  # _tuple = (DATA_FIELD_NAME, GROUP, CATEGORY)
        for _node in child_list:
            if _node.nodeName == "DATA_FIELD_NAME" and _tuple[0] in _node.firstChild.data:
                _cat, _grp, _dfn, _group_text, _category_text = _tuple[2], _tuple[1], _tuple[0], _tuple[1], _tuple[2]
            if _node.nodeName in ["GROUP", "CATEGORY"]:
                _column.removeChild(_node)
    try:
        _column = attach_group_category(_column, _group_text, _category_text, _file)
    except ValueError:
        _column = handle_no_field_found(_column, _grp, _cat)

    try:
        _column = change_element_value(_column, "EDITABLE", _dfn, f"./src/{_cat}/{_grp}.csv")
        _column = change_element_value(_column, "VISIBLE", _dfn, f"./src/{_cat}/{_grp}.csv")
        _column = change_element_value(_column, "NULLABLE", _dfn, f"./src/{_cat}/{_grp}.csv")
    except ValueError:
        print(f"error in column {_column}")
    return _column


def attach_group_category(_column, _group_text, _category_text, _file):
    if not _group_text or not _category_text:
        raise ValueError
    _group = _file.createElement("GROUP")
    _category = _file.createElement("CATEGORY")
    attach_text_node(_group, _group_text, _file)
    attach_text_node(_category, _category_text, _file)
    _column.appendChild(_group)
    _column.appendChild(_category)
    return _column


def handle_no_field_found(_column, _grp, _cat):
    try:
        print(_column)
        for field in child_list:
            if field.nodeName == "DATA_FIELD_NAME":
                raise NoFieldFound(f"output/error.txt", field.firstChild.data)
    except NoFieldFound:
        return _column
    return _column


def generate_xml(_filepath, _columns, _other_settings):
    # Build the XML as a string
    xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_string += '<ColumnSettingsDS xmlns="http://tempuri.org/ColumnSettingsDS.xsd">\n'
    for _column in _columns:
        xml_string += f"{_column.toxml()}\n"
    for setting in _other_settings:
        xml_string += f"{setting.toxml()}\n"
    xml_string += '</ColumnSettingsDS>'

    # Pretty print the XML string
    dom = parseString(xml_string)
    pretty_xml = dom.toprettyxml()
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])  # Use 4 spaces for indentation

    # Write the pretty XML to the file
    with open(_filepath, 'w+', encoding="UTF-8") as xml_file:
        xml_file.write(pretty_xml)


def modify_column_setting(single_file):
    """
    Modifies the column settings in an XML file based on the provided data.

    :param single_file: XML file to be modified.
    :return: List of updated columns.
    """
    print(f"Modyfing column setting for file: {single_file}")
    try:
        _file = minidom.parse(single_file)
        print(f"Fetching groups and categories...")
        categories_file = "./src/GROUP & CATEGORIES LIST.csv"

        # Returns a list of tuples (DATA_FIELD_NAME, GROUP)
        print("Assigning groups to fields...")
        fields_groups = assign_group(_matching_file="./src/DATA_FIELDS_NAMES.csv")

        # Add category to the list of tuples
        # Returns a list of tuples (DATA_FIELD_NAME, GROUP, CATEGORY)
        print("Assigning categories to groups...")
        groups_fields_categories = generate_final_list(_fields_groups=fields_groups, _filepath=categories_file)

        elements = {
            # Take the column from the xml file
            "COLUMN_SETTING": "COLUMN_SETTING",
            # Take the grid setting from the xml file
            "GRID_SETTING": "GRID_SETTING",
            # Take the classification setting from the xml file
            "CLASSIFICATION_SETTING": "CLASSIFICATION_SETTING",
            # Take the relation setting from the xml file
            "RELATION_SETTING": "RELATION_SETTING"
        }

        elements_list = get_list_of_elements(_parsed_file=_file, _list_of_elements=elements)

        _processed_column_setting = []
        _processed_other_setting = []
        print("Updating column setting...")
        for _column in elements_list["COLUMN_SETTING"]:
            try:
                # Set the current global column variable to the column being processed
                global current_column
                current_column = _column
                # Get the child nodes of the global column variable
                set_column_child_node_list(_column)
                # Takes single column and updates it with the correct group and category
                _processed_column_setting.append(
                    update_column_setting(_groups_fields_categories=groups_fields_categories, _column=_column,
                                          _file=_file))
            except ValueError:
                print(f"error in column {_column}")
        for grid_setting in elements_list["GRID_SETTING"]:
            _processed_other_setting.append(grid_setting)

        for classification_setting in elements_list["CLASSIFICATION_SETTING"]:
            _processed_other_setting.append(classification_setting)

        for relation_setting in elements_list["RELATION_SETTING"]:
            _processed_other_setting.append(relation_setting)

        return _processed_column_setting, _processed_other_setting
    except xml.parsers.expat.ExpatError:
        with open("src/error.txt", "a") as error_file:
            error_file.write(f"{single_file}\n")
            error_file.close()
        return []


def process_files(_file):
    """
    Args:
        _file: A list of file paths.

    """
    processed = modify_column_setting(_file)
    processed_columns = processed[0]
    processed_other_setting = processed[1]
    generate_xml(f"{_file}", processed_columns, processed_other_setting)


if __name__ == '__main__':
    directory_files = glob.glob(f"./*.xml")
    for file in directory_files:
        process_files(file)
        csvtools.read_errors_file()
        add_found_fields()

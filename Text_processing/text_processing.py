
from collections import Counter
import datetime
import re

from lxml import etree


def get_duplicates(elements):
    duplicates = [key for key, value in Counter(elements).items() if value > 1]
    return duplicates


def read_all_lines_from_file(file_path):
    with open(file_path) as file_to_read:
        all_lines = file_to_read.read().splitlines()
    return all_lines


def is_line_contains_anything(line):
    return len(line.strip()) > 0


def is_line_empty(line):
    return len(line.strip()) == 0


def is_line_not_commented(line, comment_signs):
    stripped_line = line.strip()
    return not stripped_line.startswith(comment_signs)


def split_line_by_white_spaces(line):
    split_line = re.split('[ \t]', line)
    return split_line


def split_lines_by_white_spaces(lines):
    split_lines = [split_line_by_white_spaces(line) for line in lines]
    return split_lines


def uppercase_lines(lines):
    lines_in_uppercase = [line.upper() for line in lines]
    return lines_in_uppercase


def remove_empty_lines(lines):
    valuable_lines = [line for line in lines if not is_line_empty(line)]
    return valuable_lines


def is_line_separated_into_columns(line, separator, number_of_columns):
    split_line = line.split(separator)
    return len(split_line) == number_of_columns


def is_line_contains_empty_field(line, separator):
    split_line = line.split(separator)
    return '' in split_line


def is_line_well_formatted_as_one_white_space_between_data(line):
    split_line = split_line_by_white_spaces(line)
    return '' not in split_line


def normalize_wrong_whitespace_separated_line(line, new_separator=' '):
    split_elements = split_line_by_white_spaces(line)
    while '' in split_elements:
        split_elements.remove('')
    well_separated_line = new_separator.join(split_elements)
    return well_separated_line


def get_defective_lines_for_rule_one_white_space_between_data(lines):
    defective_lines = list()
    for line in lines:
        if is_line_empty(line):
            continue
        if not is_line_well_formatted_as_one_white_space_between_data(line):
            defective_lines.append(normalize_wrong_whitespace_separated_line(line))
    return defective_lines


def is_unsigned_decimal(text):
    return text.replace('.', '', 1).isdigit()


def is_valid_date_as_yyyymmdd(text):
    if len(text) == 8:
        try:
            valid_date = datetime.datetime.strptime(text, '%Y%m%d')
            return True
        except ValueError:
            return False
    else:
        return False


def is_xml_well_formed(xml_file_name):
    xml_well_formed = dict().fromkeys(('is_well_formed', 'error_message'))
    try:
        tmp = etree.parse(xml_file_name)
        xml_well_formed['is_well_formed'] = True
    except IOError as io_error:
        xml_well_formed['is_well_formed'] = False
        xml_well_formed['error_message'] = str(io_error)
    except etree.XMLSyntaxError as xml_syntax_error:
        xml_well_formed['is_well_formed'] = False
        xml_well_formed['error_message'] = str(xml_syntax_error.error_log)
    finally:
        return xml_well_formed


def is_xml_valid_against_schema(xml_file_name, xsd_file_name):
    xml_valid = dict().fromkeys(('is_valid', 'error_message'))
    well_formed_result = is_xml_well_formed(xml_file_name)
    if well_formed_result['is_well_formed']:
        xml_file = etree.parse(xml_file_name)
        xsd_file = etree.XMLSchema(file=xsd_file_name)
        if xsd_file.validate(xml_file):
            xml_valid['is_valid'] = True
        else:
            xml_valid['is_valid'] = False
            xml_valid['error_message'] = ('%s is not valid against %s Reason: %s '
                                          % (xml_file_name, xsd_file_name, xsd_file.error_log))
    else:
        xml_valid['is_valid'] = False
        xml_valid['error_message'] = ('xml file with name: %s is not well-formed validity check is NOT POSSIBLE'
                                      % xml_file_name)
    return xml_valid

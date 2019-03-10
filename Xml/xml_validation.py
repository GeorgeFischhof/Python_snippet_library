
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
    
    xsd_well_formed_result = is_xml_well_formed(xsd_file_name)
    if not xsd_well_formed_result['is_well_formed']:
        xml_valid['is_valid'] = False
        xml_valid['error_message'] = ('XSD file with name: %s is not well-formed validity check is NOT POSSIBLE'
                                      % xsd_file_name)
        return xml_valid
    
    xml_well_formed_result = is_xml_well_formed(xml_file_name)
    if xml_well_formed_result['is_well_formed']:
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

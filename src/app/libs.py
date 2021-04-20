import argparse
import json
import xml.etree.cElementTree as e


def retrieve_json(url, page, limit, vcf_object):
    """
    This function returns the paginated data of a vcf file in json format.
    :param url: the request url
    :param page: number of page
    :param limit: number of records in one page
    :param vcf_object: VcfParser object
    :return: Json data
    """
    # retrieve data for one page
    start = (page - 1) * limit
    data_chunk = vcf_object.df.iloc[start:start + limit]

    # build json output
    payload = {}
    # make previous url
    if page == 1:
        payload['previous_url'] = ''
    else:
        payload['previous_url'] = f'{url}?page={page - 1}&limit={limit}'
    # make next url
    if page == 1 + round(vcf_object.df.shape[0] / 20):
        payload['next_url'] = ''
    else:
        payload['next_url'] = f'{url}?page={page + 1}&limit={limit}'

    # make data 
    payload['data'] = json.loads(data_chunk.to_json(orient='records'))

    return payload


def retrieve_record_data(rec_id, vcf_object):
    """
    This function returns the data of a specific record of a vcf file in json format.
    :param rec_id: Record id
    :param vcf_object: VcfParser object
    :return: json data
    """
    data_chunk = vcf_object.df.loc[vcf_object.df['ID'] == rec_id]
    return json.loads(data_chunk.to_json(orient='records'))


def json_toXML(json_object):
    """
    Converts the json object of "retrieve_data" request to XML
    :param json_object: json input
    :return: xml string
    """
    # create root
    root = e.Element('root')

    # create subelements
    e.SubElement(root, 'previous_url').text = json_object['previous_url']

    e.SubElement(root, 'next_url').text = json_object['next_url']

    data = e.SubElement(root, 'data')

    for each in json_object['data']:
        for key, value in each.items():
            e.SubElement(data, key.replace(" ", "_")).text = str(value)

    # build xml
    xml_object = e.ElementTree(root)

    return e.tostring(root)


def write_new_record(record, vcf_object):
    """
    Append new record to vcf file.
    :param record: dict with input data
    :param vcf_object: VcfParser object
    :return:
    """
    vcf_object.df = vcf_object.df.append(record, ignore_index=True)
    vcf_object.write()


def update_record(rec_id, record, vcf_object):
    """
    Modify record of vcf file.
    :param rec_id: id of record
    :param record: dict with input data
    :param vcf_object: VcfParser object
    :return:
    """
    index = vcf_object.df.index[vcf_object.df['ID'] == rec_id].to_list()

    for key in record.keys():
        vcf_object.df.loc[index, key] = record.get(key)
    vcf_object.write()


def remove_record(rec_id, vcf_object):
    """
    Remove record from vcf file.
    :param rec_id: id of record
    :param vcf_object: VcfParser object
    :return:
    """
    index = vcf_object.df.index[vcf_object.df['ID'] == rec_id].to_list()
    vcf_object.df = vcf_object.df.drop(index)
    vcf_object.write()


def check_if_record(rec_id, vcf_object):
    """
    Check if record exists in vcf file based on id.
    :param rec_id: id of record
    :param vcf_object: VcfParser object
    :return: True/False
    """
    index = vcf_object.df.index[vcf_object.df['ID'] == rec_id].to_list()
    return True if len(index) else False


def parse_args():
    """
    Command Line Argument parser.
    """
    parser = argparse.ArgumentParser(
        description="""
        Short description of how package works.
        """
    )
    parser.add_argument(
        '-f',
        '--filename',
        type=str,
        help="""
            Argument that takes the name of VCF file.
            """,
        required=True
    )
    return parser.parse_args()
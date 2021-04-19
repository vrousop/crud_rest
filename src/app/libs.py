import json
import allel
import xml.etree.cElementTree as e
from src import __VCF_FILE__


def retrieve_json(url, page, limit, vcf_object):
    # retrieve data for one page
    start = (page-1) * limit
    data_chunk = vcf_object.df.iloc[start:start+limit]

    # build json output
    payload= {}
    # make previous url
    if page == 1:
        payload['previous_url'] = ''
    else:
        payload['previous_url'] = f'{url}?page={page-1}&limit={limit}'
    # make next url
    if page == 1+ round(vcf_object.df.shape[0]/20):
        payload['next_url'] = ''
    else:
        payload['next_url'] = f'{url}?page={page+1}&limit={limit}'
    
    # make data 
    payload['data'] =  json.loads(data_chunk.to_json(orient='records'))

    return payload

def retrieve_user_data(uid, vcf_object):

    data_chunk = vcf_object.df.loc[vcf_object.df['ID'] == uid]
    return json.loads(data_chunk.to_json(orient='records'))

def json_toXML(json_object):
    # create root
    root = e.Element('payload')

    # create subelements
    e.SubElement(root,'previous_url').text = json_object['previous_url']

    e.SubElement(root,'next_url').text = json_object['next_url']

    data = e.SubElement(root,'data')

    for each in json_object['data']:
        for key, value in each.items():
            e.SubElement(data,key).text = str(value)

    # build xml
    xml_object = e.ElementTree(root)
    xml_object.write("json_to_xml.xml")
    
    return e.tostring(root)


def write_new_record(record, vcf_object):
    vcf_object.df = vcf_object.df.append(record, ignore_index=True)
    vcf_object.write()

def update_record(user_id, record, vcf_object):
    index = vcf_object.df.index[vcf_object.df['ID'] == user_id]
    for key in record.keys():
        vcf_object.df.loc[index, key] = record.get(key)
    vcf_object.write()


def remove_record(user_id, vcf_object):
    index = vcf_object.df.index[vcf_object.df['ID'] == user_id]
    vcf_object.df = vcf_object.df.drop([index[0]])
    vcf_object.write()
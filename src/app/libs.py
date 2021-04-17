import json
import allel
import xml.etree.cElementTree as e
from src import __VCF_FILE__


def retrieve_json(url, page, limit):
    # load vcf file to dataframe
    df = allel.vcf_to_dataframe(__VCF_FILE__)   

    # retrieve data for one page
    start = (page-1) * limit
    data_chunk = df.iloc[start:start+limit]

    # build json output
    payload= {}
    # make previous url
    if page == 1:
        payload['previous_url'] = ''
    else:
        payload['previous_url'] = f'{url}?page={page-1}&limit={limit}'
    # make next url
    if page == 1+ round(df.shape[0]/20):
        payload['next_url'] = ''
    else:
        payload['next_url'] = f'{url}?page={page+1}&limit={limit}'
    
    # make data 
    payload['data'] =  json.loads(data_chunk.to_json(orient='records'))

    return payload

def retrieve_user_data(uid):
    df = allel.vcf_to_dataframe(__VCF_FILE__) 
    data_chunk = df.loc[df['ID'] == uid]
    return json.loads(data_chunk.to_json(orient='records'))

def json_toXML(json_object):
    # create root
    root = e.Element('payload')

    # create subelements
    e.SubElement(root,'previous_url').text = json_object['previous_url']

    e.SubElement(root,'next_url').text = json_object['next_url']

    data = e.SubElement(root,'data')

    for z in json_object['data']:
        e.SubElement(data,'ALT_1').text = z['ALT_1']
        e.SubElement(data,'ALT_2').text = z['ALT_2']
        e.SubElement(data,'ALT_3').text = z['ALT_3']
        e.SubElement(data,'CHROM').text = z['CHROM']
        e.SubElement(data,'FILTER_PASS').text = str(z['FILTER_PASS'])
        e.SubElement(data,'ID').text = z['ID']
        e.SubElement(data,'POS').text = str(z['POS'])
        e.SubElement(data,'QUAL').text = str(z['QUAL'])
        e.SubElement(data,'REF').text = str(z['REF'])

    # build xml
    xml_object = e.ElementTree(root)
    xml_object.write("json_to_xml.xml")
    
    return e.tostring(root)
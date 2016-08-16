import sys
import argparse
import requests
import json

global projects, chrs, variantSetIds, url, outfile
chrs = {'1':249250621,'2':243199373,'3':198022430,'4':191154276,'5':180915260,'6':171115067,'7':159138663,'8':146364022,'9':141213431,'10':135534747,'11':135006516,'12':133851895,'13':115169878,'14':107349540,'15':102531392,'16':90354753,'17':81195210,'18':78077248,'19':59128983,'20':63025520,'21':48129895,'22':51304566,'X':155270560,'Y':59373566}

# for testing
#chrs = {'3': 198022430}
header = 'tumor_name\tchr\tstart_position\tend_position\tbuild\tref_allele\talt_allele\ttumor_f\tt_ref_count\tt_alt_count\n'

def GASearchVariantsRequest(query, url):
    request = {'start':1, 'end': None, 'referenceName': None, 'pageSize': None, 'pageToken': None, 'callSetIds': None, 'variantSetIds': ['harmony']}
    job_list = []
    for key, val in chrs.iteritems():
        request['end'] = val
        request['referenceName'] = key
        oncotator_build(request, url)

def variants_search(this_request, this_url):
    print this_request
    try:
        r = requests.post(this_url + "/variants/search", data=json.dumps(this_request), headers={'content-type':'application/json'})
        print r
        return json.loads(r.text)
    except:
        print 'error in request, continuing with empty object', this_request, this_url
        return {'variants':[], 'nextPageToken': None}

def vs_recurse(this_request, this_url):
    r_json = variants_search(this_request, this_url)
    responses = r_json['variants']
    nextPageToken = r_json['nextPageToken']

    while nextPageToken != None:
        new_request = this_request
        new_request['pageToken'] = nextPageToken
        new_response = variants_search(new_request, this_url)
        responses = responses + new_response['variants']
        nextPageToken = new_response['nextPageToken']
    return responses

def oncotator_build(request, query_url):
    build = 'hg19'

    for url in query_url:
        # request to url
        variants = vs_recurse(request, url)

        # write results to oncotator input file
        for variant in variants:
            ref_allele = variant['referenceBases']
            alt = variant['alternateBases']
            contig = variant['referenceName']
            start_position = variant['start']
            end_position = variant['end']
            # TODO add better checking
            for call in variant['calls']:
                for allele in call['genotype']:
                    if allele != '0':
                        line = []
                        if 'callSetId' != None:
                            line.append(call['callSetId'])
                        else:
                            line.append("None")
                        line.append(contig)
                        line.append(start_position)
                        line.append(end_position)
                        line.append('37')
                        line.append(ref_allele)
                        line.append(alt[int(allele)-1])
                        if ('AF' in call['info']):
                            line.append(call['info']['AF'][0])
                        else:
                            line.append(" ")
                        if ('AN' in call['info']):
                            line.append(call['info']['AN'][0])
                        else:
                            line.append(" ")
                        if ('AC' in call['info']):
                            line.append(call['info']['AC'][0])
                        else:
                            line.append(" ")
            outfile.write('\t'.join(map(str, line)))
            outfile.write('\n')

if __name__ == "__main__":

    # example query:
    # python ga4gh_hp_client.py -u http://<host1>:<port_on_host1>/variants/search http://<host2>:<port_on_host2> http://<host3>:<port_on_host3>/variants/search -q liver
    # http://192.168.100.102:8090 http://192.168.100.103:8090
    parser = argparse.ArgumentParser(description='Variant DB GA4GH Communicator')
    parser.add_argument('-u', '--urls', dest='urls', nargs = "+", type=str, required=True, default=None, help="Path to databases")
    parser.add_argument('-o', '--output', dest='output', type=str, required=True, default=None, help='Path to output file.')
    parser.add_argument('-q', '--query', dest="query", nargs='?', default=None, help='Generic Query Term.')

    args = parser.parse_args()

    url = args.urls

    outfile = open(args.output, 'w')
    outfile.write(header)

    GASearchVariantsRequest(args.query, args.urls)
    outfile.close()
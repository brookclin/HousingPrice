import json
import re

f = open("housingdata.json", 'r')
raw_dict = json.load(f)
f.close()
data_dict = {}

for line in raw_dict:
    # 926-1-2-E-73rd-St-Los-Angeles-CA-90001
    url = line['url'].lower()
    if url not in data_dict:
        data_dict[url] = {}
    postcode = url.split('-')[-1]
    data_dict[url]['postcode'] = postcode

    if 'score' in line:
        data_dict[url]['score'] = line['score']
        continue

    # ["Neighborhood: Southeast Los Angeles"]
    if line['neighborhood']:
        neighborhood = re.findall(r"Neighborhood: (.*)", line['neighborhood'][0])
        if neighborhood:
            data_dict[url]['neighborhood'] = neighborhood[0]

    # ["1,649 sqft"]
    # "anything that isn't a number or a decimal point" -> ""
    if line['flooring']:
        data_dict[url]['flooring'] = re.sub("[^\d\.]", "", line['flooring'][0])

    if line['price']:
        data_dict[url]['price'] = re.sub("[^\d\.]", "", line['price'][0])

    if line['bedrooms']:
        data_dict[url]['bedrooms'] = line['bedrooms'][0]

    if line['Year Built']:
        data_dict[url]['year_built'] = line['Year Built'][0]

    # TODO: some of the number are acres not sqft
    if line['lot']:
        lot = re.sub("[^\d\.]", "", line['lot'][0])
        # if it's measured in acres
        if "acre" in line['lot'][0]:
            lot = str(43560 * float(lot))
        data_dict[url]['lot'] = lot

    if line['type']:
        data_dict[url]['type'] = line['type'][0]


with open('result.json', 'w') as fp:
    json.dump(data_dict, fp, indent=4)

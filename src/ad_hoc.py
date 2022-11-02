import json
 
# Opening JSON file
with open('./result.json') as json_file:
    data = json.load(json_file)
 
def dominent_journal_cites(data):
    count_dict = {}
    for _,v in data.items():
        set_journal = set( dic['name'] for dic in v['journal'])
        for journal_name in set_journal:
            if journal_name not in count_dict.keys():
                count_dict[journal_name] = 1
            else:
                count_dict[journal_name] += 1

    journal_most_cites = max(count_dict, key=lambda k: count_dict[k])
    print(journal_most_cites)


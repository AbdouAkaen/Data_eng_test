import pandas as pd
from sqlalchemy import create_engine, inspect
import json

# gets the table 'table' with sqlalchemy engine
def get_table(engine, table):
    df = pd.read_sql_query('select * from '+table, con=engine)
    return df

#This function retreives the components needed then it fills 'drugname_dict' dictionary with it
#then We'll dump 'drugname_dict' to a json file
#'pub_type' is used to distinguish between the elements 'pubmed' and 'clinical_trials' in the final dict
def fill_dict(drugname_dict, drug_name, pub_type, df):
    for title_index, title in enumerate(df['title']):
        if drug_name in title:
            id = df.iloc[title_index]["id"]
            date = df.iloc[title_index]["date"]
            journal = df.iloc[title_index]["journal"]
            drugname_dict[drug_name][pub_type].append({'id':str(id), 'date':date})
            drugname_dict[drug_name]['journal'].append({'name':journal, 'date':date})

#Main function to  fetch data and construct the json file
def construct_json_file(engine):

    inspector = inspect(engine)
    names = inspector.get_table_names()
    # We could've made a check for every table name except hte '.' 
    if ('pubmed' and 'drugs' and 'clinical_trials') in names:
        df_pubmed = get_table(engine, 'pubmed')
        df_drugs = get_table(engine, 'drugs')
        df_clinical_trials = get_table(engine, 'clinical_trials')
    else:
        # raise some exception here, or use the try except 
        pass

    #Here we set a same column name for title column within both dataframes
    df_clinical_trials.rename(columns={'scientific_title': 'title'}, inplace=True)
    df_drugs["drug"] = df_drugs["drug"].str.lower()
    df_pubmed['title'] = df_pubmed['title'].str.lower()
    df_clinical_trials['title'] = df_clinical_trials['title'].str.lower()

    #the final dict to transform to json
    drugname_dict = {}
    for _, drug_name in enumerate(df_drugs["drug"]):
        drugname_dict[drug_name] = {'pubmed': [], 'clinical_trials':[], 'journal':[]}
        fill_dict(drugname_dict, drug_name, 'pubmed', df_pubmed)
        fill_dict(drugname_dict, drug_name, 'clinical_trials', df_clinical_trials)

    with open('result.json', 'w') as fp:
        json.dump(drugname_dict, fp)

############################
############################
# Another approach would be as follows

#     output = {
#     drug_name: {'pubmed':
#                 [
#                     {'id': df_pubmed.iloc[title_index]["id"], 'date': df_pubmed.iloc[title_index]["date"]}  \
#                         for title_index, title in enumerate(df_pubmed['title']) if drug_name in title
#                     ],
#                     'clinical_trials':                    
#                     [
#                     {'id': df_clinical_trials.iloc[sc_title_index]["id"], 'date': df_clinical_trials.iloc[sc_title_index]["date"]}  \
#                         for sc_title_index, sc_title in enumerate(df_clinical_trials['scientific_title']) if drug_name in sc_title
#                     ]
#                     } for _, drug_name in enumerate(df_drugs["drug"])
# }
# and same with journal



if __name__ == '__main__':
    # Instanciate the DB engine
    # The values under should not be in this file
    # test_ is the name of the database
    db_engine = create_engine('postgresql://root:root@localhost:5432/test_')
    construct_json_file(db_engine)

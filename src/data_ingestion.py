import pandas as pd 
import ntpath
from sqlalchemy import create_engine
import glob
import os

# The local path to our data
LOCAL_PATH = "/test_data_eng"

# here we might provide all necessary changes to the data
# The process can be done before loading data to the database, it can also be done after in the extract part
# for example, transform ids to int values and fill the missing id values by the use of isnull(), fillna() etc
# This short solution is not optimal for all the situations obviously, an example might be a dataframe with only one row
def transform_data(df):
    try:
        index_missing_id = df[df['id']==''].index.tolist()[0]
        id_value_previous_index = df.iloc[index_missing_id-1]["id"]
        df["id"][index_missing_id] = int(id_value_previous_index) + 1
        print(df) 
    except:
        print('Oh !!')

    return df

# A function that loads all the data files from local to pg database where each 
# table is associated to a file except for pubmed
def ingest_data(files,db_engine):
    for filename in files:
        file_basename = ntpath.basename(filename)
        print("Table creation in DB...")

        if "csv" in filename:
            df = pd.read_csv(filename)
            # call the transform function here

        elif "json" in filename:
            df = pd.read_json(filename)
            # call the transform function here
            df = transform_data(df)
        else:
            continue
        
        file_basename_ = os.path.splitext(file_basename)[0]
        # if_exists is set to append to handle the json file, we can also try to merge 
        # all files in one and push it to its associated database
        df.to_sql(name=file_basename_, con=db_engine, if_exists='append') 
        print("Table created for "+file_basename)
        print(df)

if __name__ == '__main__':
    # Instanciate the DB engine 
    db_engine = create_engine('postgresql://root:root@localhost:5432/test_') 
    all_data_files = glob.glob(LOCAL_PATH + "/data/*")
    ingest_data(all_data_files,db_engine)
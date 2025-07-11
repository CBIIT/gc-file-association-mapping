import yaml 
import pandas as pd
#this script generates a TSV file that maps associated files based on the input assiciations YAML file
with open("associations.yaml", 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)
df = pd.DataFrame()
file_id_list = []
parent_id_list = []
for k in data["file_associations"].keys():
    file_id_list.append(k)
    parent_id_list.append(data["file_associations"][k])
df["file_id"] = file_id_list
df["file.file_id"] = parent_id_list
df["type"] = ["file"] * len(df)
df.to_csv("associated_file.tsv", sep='\t', index=False)
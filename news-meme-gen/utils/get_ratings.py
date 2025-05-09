import pandas as pd
import sqlite3
import json
import shutil

db_path = "db/ratings.db"
user_db_path = 'db/database.json'
output_folder = 'ratings_data'
save_ratings_path = output_folder+'/rated_jokes.csv'
save_users_path = output_folder+'/users.json'
with sqlite3.connect(db_path) as conn:
    ratings_df = pd.read_sql_query("SELECT * FROM ratings", conn)
ratings_df.to_csv(save_ratings_path)
json.dump(
    json.load(open(user_db_path))['users'], 
    open(save_users_path,'w+'), 
    indent=4
    )
shutil.make_archive('ratings_data', 'zip', output_folder)
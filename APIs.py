import json
import requests
import pymongo

# Getting mongoDB setup
# TO DO: Add database URL
  client = pymongo.MongoClient(database_url)
  
  # Connecting to the database
  mydb = client[patients]

# APIs
# getteam API
if path is "/getteam":
  status = 1
  team_info = {
    'team_name': 'Arnoldillo', 
    'Team_member_sids': {912141777, 900000000},
    'app_status_code' : status
  }
  jsonString = json.dump(team_info)

# reset API
else if path is "/reset":
  
  # Connecting the to collection
  # TO DO: add collection name
  col = mydb[collection_name]
  d = col.delete_many()
  return_info = {
    'reset_status_code' : '1'
  }
  jsonString = json.dump(return_info)
  
  else if path is "/gethospital":
    query = "SELECT max_capacity AS total_beds, (max_capacity-current_capacity) AS available_beds, zip_code FROM hospitals WHERE hospital_id is " + id

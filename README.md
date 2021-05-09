# rSubscriber
Team Name: Arnoldillo
Team members: Nathan Arnold, Dillon Tate

Individual contributions: 

Both:
  Created database designs and determined attributes;
  Imported CSV files to database websites;
  Meet together to go over code and discuss planning
  
  
Dillon:
  Created github repositories to share files;
  implemented APIs.py to handle web requests including getteam, testcount, reset, gethospital;
  worked on DBtools.py to use for handling database functions;
  implemented webserver.py to start the server (not used anymore);
  created APIhelper functions;
  set up resets and creation of mysql databases;
  switched mongo implementation of zip code distances to use the csv file instead;
  moved APIs.py functionalities into app_attempt.py, flask server that works but with wrong hostname;
  debugging and testing for getteam and testcount;
  formatting current capacities of hospitals as a txt file;
  helper functions for capacities
  
  
Nathan:
  Wrote interactions with MongoDB server (deprecated); 
  Set up web server using Flask; 
  Tested web server and integrated with existing project


Project design:
  Language: Python
  
  We originally planned to use MongoDB: A graph database will be used to store precomputed distances from zip codes to treatment facilities.
  Given a patient zip code, map to the nearest hospitals with open beds. A node is created for each zip code containing at least one hospital.
  Node values: distance, zip_to, zip_from
  
  Instead of this, we moved to using the csv file as a table, and querying on that using pandas whenever we needed to get the zipcode distance to a node. To save time on queries, this could be implemented by precomputing distances and creating a table for each zipcode that lists the distance to every other zipcode, but this would take up more memory.
  
  A query to this database would include the current zipcode and return the list of hopsital_ids in order of least to greatest distance.
  
  atlas: reallysecurepwd
  
  We planned to use a complex event processor (PySiddhi) to handle the event streams containing patient records.
  This CEP would be able to detect activity over time intervals to determine if there is an alert state. It would be used to handle the real time reporting APIs.
  
  We did not get the chance to implement this yet, we have been having difficulties on other parts and PySiddhi did not seem to be a viable choice like we expected to use.
  
  MySQL (PyMYSQL): A relational database will be used to keep track of hospital capacity and patient status. This was chosen for familiarity and ease of use due to extensive documentation, and because it was a language we could use to query specific information with sorting.
  
  Entity: Patient
    
  Attributes: first_name, last_name, mrn, zip_code, patient_status_code, hospital_id (this will be -1 if not assigned and 0 if home)
  
  Entity: Hospital
    
  Attributes: current_capacity, and all properties included in hospital .csv (hospital_id, zip_code, trauma, etc...)
  
  Relation: Patient <-> hospital

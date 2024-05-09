### FAA Accident/Incident Data (AID)

The data in the downloads folder is taken from the FAA Accidenct/Incident Data (AID), originally accessed at https://av-info.faa.gov/dd_sublevel.asp?Folder=%5CAID in June 2022. AID contains accident reports detailing airplane type, an accident-type code, a description of the incident, and more. See downloads/afilelayout.csv for a description of each column.

The records from 1975-2022 were downloaded and concatenated, resulting in over 210K records.

We then selected a subset of these records with accident-types relating to maintenance, found in column c78, specifically:

AF: IMPROPER MAINTENANCE APT FAC\
DE: DEFIC, CO MAINTAIN EQUIP/SERV\
AI: INADEQUATELY MAINTAIN AWY FAC\
AP: INADEQUATELY MAINTAINA PCH FAC\
AU: ATTEMPT OPERATION WITH DEF EQP\
EQ: IMPROPER OPERATION EMEG/EQUIP\
II: INADEQUATE INSP OF AC PREFLT\
ME: FAIL/INCORRECT USE MISC EQUIP

See preprocessing/select_maint_records.py for code. This script outputs Maintenance_Text_Data.csv. Preprocessing/remove_na.py removes the rows in the data with empty natural language description entries (column c119) and outputs Maintenance_Text_Data_nona.csv.

The above link does not work as of at least Feb 2024. They seem to have made the data only available through direct query. See the page: https://www.faa.gov/data_research/accident_incident at faa.gov, and click the link "Search Aviation Accident Reports" : https://www.ntsb.gov/Pages/AviationQueryV2.aspx

For example, the first entry in the Maintenance_Text_data.csv, with the description "TAILWHEEL COCKED RIGHT PRIOR TO TKOF." can be searched by the date (15 March 1975), airplane make (CESSNA) city (IRON MOUNTAIN), and found here: https://www.ntsb.gov/Pages/brief.aspx?ev_id=47422&key=0

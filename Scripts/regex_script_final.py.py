#importing required Libraries

import re # for working with regular expressions
import os # for interacting with the operating systems like reading files
import pandas as pd # for working with with tables and exporting tsv files

#writing list of data rows in tsv file
def write_tsv(rows, column_list, path):
    
#create a table from the list of rows
    
    df= pd.DataFrame(rows, columns=column_list) 

#saving the table to a file withoit row numbers
    df.to_csv(path, sep="\t", index=False)

#define which folder to use
folder= "../articles"

# loads the gazetteer (list of place names):
path = "../gazetteers/geonames_gaza_selection.tsv"

#reading the gazetteer file content
with open(path, encoding="utf-8") as file:
    data = file.read()

#Building dictionary to store patterns and  name mapping
patterns = {} # stores regex patterns and count for each place 

#mapping any name (including alternates) to its main asciiname
name_to_ascii = {} #maps all the name variants to the main name(asciiname)

# splitting gazetteer into rows( one per line)
rows = data.split("\n")

# loop through each row, skipping the header
for row in rows[1:]:
    columns =row.split("\t")
    if len(columns)<6:
        continue  # skips rows without atleast 6 columns

    # extracting asciiname (main name) from column (took help from chatgpt: script 1)
    asciiname = columns[0].strip()
    if not asciiname:
        continue  # skip if main name is missing
    
   # add main name to the patterns and mapping
    patterns[asciiname] = {"pattern": re.escape(asciiname), "count": 0} # escaping speacial characters and adding main name
    name_to_ascii[asciiname.lower()] = asciiname  # map to itself

    #extracting alternative names from 6th column
    alternate_names = columns[5].strip()
    if alternate_names:
        alternate_list=alternate_names.split(",") # Split by commas to handle multiple alternatives
        for alternate in alternate_list:
            alternate=alternate.strip()
            if alternate and alternate.lower() not in name_to_ascii:
                
                # add alternate names to the patterns and map to main name
                patterns[alternate] = {"pattern": re.escape(alternate), "count": 0} # escaping speacial characters and adding alternate names if present
                name_to_ascii[alternate.lower()] = asciiname # map alternate to asciiname

#building dictionary for the frequency of names per month
mentions_per_month = {}

#setting the war date to filter the articles having names after the war date
war_start_date= '2023-10-07'

#loop through all article files 
for filename in os.listdir(folder):
    if not filename.endswith(".txt"): # process only .txt
        continue # skips non text file

    # Extract the date from the filename 
    date_str = filename.split("_")[0]
    if date_str < war_start_date:
        continue #Skip files from before the war

    #Build the full file path
    file_path = os.path.join(folder, filename)

    #Open and read the articles
    with open(file_path, encoding="utf-8") as file:
        text=file.read()

    #looping through places to search for mentions
    for place in patterns:
        pattern=patterns[place]["pattern"] # Get regex-safe pattern
        matches = re.findall(pattern, text, re.IGNORECASE)
        count = len(matches) # number of times the place was found
        if count== 0:
            continue # skips places with zero frequency

        # convert to main asciiname
        ascii_key = name_to_ascii[place.lower()]
        
        patterns[ascii_key]["count"] += count #adding the number of times places found to the total frequency
        month_str = date_str[:7] #extracting the year month from the date string

        # Add count to the mentions_per_month
        if ascii_key not in mentions_per_month:
            mentions_per_month[ascii_key] = {}                  
        if month_str not in mentions_per_month[ascii_key]:
            mentions_per_month[ascii_key][month_str] = 0

        #Adding the new matches on the place names to the number of times it was mentioned that month    
        mentions_per_month[ascii_key][month_str] += count

# print mentions per place by month in a dictionary-style format
for place in mentions_per_month:
    
    print(f'"{place}": {{')

    #Get a list of all the months in which the place names are mentioned
    month_list = list(mentions_per_month[place].keys())

    #loop through each month to print the corresponding mention count
    for month in month_list:
        count = mentions_per_month[place][month] #  get the count for that month

        # display the output with a comma except for the last item to keep it clean
        if month != month_list[-1]:
            print(f' "{month}": {count},')
        else:
            print(f'    "{month}": {count}')
    print("},") # close the dictionary block and print the output

# prepare the data to export as rows in a table 
rows = []

#loop through each place again to prepare structured data for export
for place in mentions_per_month:

    # loop through each month and find the number of times the place is mentioned
    for month in mentions_per_month[place]:
        count = mentions_per_month[place][month]

        #Add each (place, month, count ) to the list
        rows.append((place, month, count))

#save the final table as a TSV file        
write_tsv(rows, ["asciiname","month", "count"],"regex_count.tsv")






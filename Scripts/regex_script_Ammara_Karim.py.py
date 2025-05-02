#importing Libraries

import re # built in library for regular expressions
import os # built in library for os-dependent functions like files
import pandas as pd # library for tabular data and exporting tsv

#writing list of data rows in tsv
def write_tsv(rows, column_list, path):
    
# converting list of rows into dataframe
    df= pd.DataFrame(rows, columns=column_list)

#writing the dataframe to tsv
    df.to_csv(path, sep="\t", index=False)

#define which folder to use
folder= "../articles"

# load the gazetteer from the tsv file:
path = "../gazetteers/geonames_gaza_selection.tsv"

#reading the file
with open(path, encoding="utf-8") as file:
    data = file.read()

#Building dictionary of pattterns for place name and a count of matches
patterns = {}

# splitting gazetteer data by a new line at each row
rows = data.split("\n")

# Skiping header row as the pattern starts from second row
for row in rows[1:]:
    columns=row.split("\t")
    if len(columns)<6:
        continue  # skips rows without atleast 6 columns

    # extracting ascciname from column 1    
    asciiname = columns[0]         
    # Process the row if it has 6 or more columns
    if asciiname:
        patterns[asciiname] = {"pattern": re.escape(asciiname), "count": 0}

    #extracting alternative names from 6th column
    alternate_names = columns[5].strip()
    if alternate_names:
        alternate_list=alternate_names.split(",") # Split by commas to handle multiple alternatives
        for alternate in alternate_list:
            alternate=alternate.strip()
            if alternate:
                patterns[alternate]={"pattern":re.escape(alternate),"count":0} # escaping speacial characters and adding alternate names if present

#building dictionary for the frequency of names per month
mentions_per_month = {}

#setting the war date to filter the articles having names after the war date
war_start_date= '2023-10-07'

#loop through each file in the folder
for filename in os.listdir(folder):
    if not filename.endswith(".txt"): # process only .txt
        continue

    # Extract the date from the filename
    date_str = filename.split("_")[0]
    if date_str < war_start_date:
        continue #Skip the file if it is before the start of  the war

    #filepath to current articles
    file_path = os.path.join(folder, filename)

    #Open and read the articles
    with open(file_path, encoding="utf-8") as file:
        text=file.read()

    #looping through places to search for matches in  the text
    for place in patterns:
        pattern=patterns[place]["pattern"] # Get regex-safe pattern
        matches = re.findall(pattern, text, re.IGNORECASE)
        count = len(matches) # number of times the place was found
        if count== 0:
            continue # skips places with zero frequency

        patterns[place]["count"] += count #adding the number of times places found to the total frequency
        month_str = date_str[:7] #extracting the month from the date string

        # initializing place and month in mentions_per_month dictionary 
        if place not in mentions_per_month:
            mentions_per_month[place] = {}                  
        if month_str not in mentions_per_month[place]:
            mentions_per_month[place][month_str] = 0

        #Adding the new matches on the place names to the number of times it was mentioned that month    
        mentions_per_month[place][month_str] += count

# Loop through each place in the mentions_per-month dictionary
for place in mentions_per_month:
    # Start a dictionary like printout for the current place
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

#Convert the mentions_per_month dictionary to list of rows for output
rows = []

#loop through each place again to prepare structured data for export
for place in mentions_per_month:

    # loop through each month and find the number of times the place is mentioned
    for month in mentions_per_month[place]:
        count = mentions_per_month[place][month]

        #Append a tuple (place, month, count) to the rows list
        rows.append((place, month, count))

#Write final result to tsv file for external use        
write_tsv(rows, ["placename","month", "count"], "regex_counts.tsv")


    















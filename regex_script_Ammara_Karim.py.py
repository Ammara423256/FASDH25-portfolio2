import re
import os
import pandas as pd

# Function to write data to tsv
def write_tsv(data, column_list, path):
    items = []
    for key, value in data.items():
        if isinstance(value, dict):  # for mentions_per_month
            for subkey, subvalue in value.items():
                items.append((key, subkey, subvalue))
        else:
            items.append((key, value))
    df = pd.DataFrame.from_records(items, columns=column_list)
    df.to_csv(path, sep="\t", index=False)

# Define folders
folder = "articles"
gazetteer_path = "gazetteers/geonames_gaza_selection.TSV"

# Load the gazetteer
with open(gazetteer_path, encoding="utf-8") as file:
    data = file.read()

# Build dictionary of patterns
patterns = {}
mentions_per_month = {}
rows = data.split("\n")
for row in rows[1:]:
    if row.strip() == "":
        continue  # skip empty lines
    columns = row.split("\t")
    name = columns[0]
    patterns[re.escape(name)] = 0
    mentions_per_month[name] = {}

# Count the number of times each pattern is found
for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue  # Only process text files

    file_date = filename[:10]  # e.g., "2023-10-15"
    if file_date < "2023-10-07":
        continue  # skip articles before the war started

    month = file_date[:7]  # "2023-10"

    file_path = f"{folder}/{filename}"
    with open(file_path, encoding="utf-8") as file:
        text = file.read()

    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        n_matches = len(matches)
        patterns[pattern] += n_matches

        # Update mentions per month
original_name = re.sub(r"\\", "", pattern)  # undo re.escape
if n_matches > 0:
    if month not in mentions_per_month[original_name]:

for pattern in patterns:
    count = patterns[pattern]
if count >= 1:
    print(f"found {pattern} {count} times")

# Write the overall frequencies
columns_total = ["asciiname", "frequency"]
tsv_filename_total = "frequencies.tsv"
write_tsv(patterns, columns_total, tsv_filename_total)

# Write the monthly frequencies
columns_monthly = ["placename", "month", "count"]
tsv_filename_monthly = "regex_counts.tsv"
write_tsv(mentions_per_month, columns_monthly, tsv_filename_monthly)


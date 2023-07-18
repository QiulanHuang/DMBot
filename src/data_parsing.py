import os
import csv
import json
import ast
import sys
from tqdm import tqdm

print("Starting...")


# Function to extract the desired information from the log entry
def extract_info(log_entry):
    log_data = json.loads(log_entry)  # Parse the log entry as JSON

    try:
        file_id = log_data["_source"]["dcache"]["billing"]["pnfsid"]
    except:
        # print("file id not found. Error occuring with this log entry:" + log_entry)
        file_id = "unknown"

    action = log_data["_source"]["event"]["action"]

    try:
        file_size = log_data["_source"]["dcache"]["billing"]["file"]["size"]
    except:
        # print("file size not found. Error occuring with this log entry:" + log_entry)
        file_size = "unknown"

    file_type = log_data["_source"]["dcache"]["billing"]["storage"]["class"]

    try:
        user_id = log_data["_source"]["dcache"]["billing"]["client"]["user"]["id"]
    except:
        user_id = "unknown"

    timestamp = log_data["_source"]["dcache"]["billing"]["ts"]

    file_path = log_data["_source"]["dcache"]["billing"]["protocol"]["path"]

    try:
        group_id = log_data["_source"]["dcache"]["billing"]["client"]["user"]["group"][
            "id"
        ]
    except:
        # print("group id not found. Error occuring with this log entry:" + log_entry)
        group_id = "unkown"

    try:
        client = log_data["_source"]["dcache"]["billing"]["client"]["address"]
    except:
        # print("client not found. Error occuring with this log entry:" + log_entry)
        client = "unkown"

    return [
        timestamp,
        file_id,
        action,
        file_size,
        file_type,
        user_id,
        group_id,
        client,
        file_path,
    ]


if len(sys.argv) < 3:
    print(
        "Please provide the input filename and output filename as a command-line arguments."
    )
    sys.exit()

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# get the file size
file_size = os.path.getsize(input_filename)

with open(input_filename, "r") as infile, open(
    output_filename, "w", newline=""
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    writer.writerow(
        [
            "Timestamp",
            "File ID",
            "Action",
            "File Size",
            "File Type",
            "User ID",
            "Group ID",
            "Client",
            "File Path",
        ]
    )

    print("Starting to parse data...")
    progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)

    for i, row in enumerate(reader):
        progress_bar.set_description("Processing row %i" % i)
        # current_row = i
        # if i == 0:
        #     continue
        if i == -1:  # Use this to limit the number of lines to read.
            break
        else:
            for i in range(len(row)):
                row[i] = json.dumps(ast.literal_eval(row[i]))  # Convert string to dict
                log_entry = row[i]  # Assuming the log entry is in the first column
                extracted_info = extract_info(log_entry)
                writer.writerow(extracted_info)

        # update progress bar by the size of the data processed
        progress_bar.update(sys.getsizeof(row))

    progress_bar.close()

print("Done!")

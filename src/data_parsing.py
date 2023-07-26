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

    try:
        action = log_data["_source"]["event"]["action"]
    except:
        # print("action not found. Error occuring with this log entry:" + log_entry)
        action = "unknown"

    try:
        file_size = log_data["_source"]["dcache"]["billing"]["file"]["size"]
    except:
        # print("file size not found. Error occuring with this log entry:" + log_entry)
        file_size = "unknown"

    try:
        file_type = log_data["_source"]["dcache"]["billing"]["storage"]["class"]
    except:
        # print("file type not found. Error occuring with this log entry:" + log_entry)
        file_type = "unknown"

    try:
        user_id = log_data["_source"]["dcache"]["billing"]["client"]["user"]["id"]
    except:
        # print("user id not found. Error occuring with this log entry:" + log_entry)
        user_id = "unknown"

    try:
        timestamp = log_data["_source"]["dcache"]["billing"]["ts"]
    except:
        # print("timestamp not found. Error occuring with this log entry:" + log_entry)
        timestamp = "unknown"

    try:
        file_path = log_data["_source"]["dcache"]["billing"]["protocol"]["path"]
    except:
        # print("file path not found. Error occuring with this log entry:" + log_entry)
        file_path = "unknown"

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
        try:
            client = log_data["_source"]["destination"]["address"]
        except:
            try:
                client = log_data["_source"]["source"]["address"]
            except:
                # print(
                #     "client not found. Error occuring with this log entry:" + log_entry
                # )
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
        if i > -1:  # Use this to set start point
            progress_bar.set_description("Processing row %i" % i)
            if i == -1:  # Use this to limit the number of lines to read.
                print("Reached the limit of lines to read.")
                break
            else:
                for i in range(len(row)):
                    row[i] = json.dumps(
                        ast.literal_eval(row[i])
                    )  # Convert string to dict
                    log_entry = row[i]  # Assuming the log entry is in the first column
                    extracted_info = extract_info(log_entry)
                    writer.writerow(extracted_info)

            # update progress bar by the size of the data processed
            progress_bar.update(sys.getsizeof(row))

    progress_bar.close()

print("Done!")

import csv
import json
import ast
import sys


print("Starting...")


# Function to extract the desired information from the log entry
def extract_info(log_entry):
    log_data = json.loads(log_entry)  # Parse the log entry as JSON
    try:
        file_id = log_data["_source"]["dcache"]["billing"]["pnfsid"]
    except:
        file_id = "unknown"
        # print("File ID not found")
    action = log_data["_source"]["event"]["action"]
    try:
        file_size = log_data["_source"]["dcache"]["billing"]["file"]["size"]
    except:
        file_size = "unknown"
        # print("File size not found")
    file_type = log_data["_source"]["dcache"]["billing"]["storage"]["class"]
    try:
        user_id = log_data["_source"]["dcache"]["billing"]["client"]["user"]["id"]
    except:
        try:
            user_id = log_data["_source"]["dcache"]["billing"]["initiator"]["name"]
        except:
            user_id = "unknown"
            # print("User ID not found")
    timestamp = log_data["_source"]["dcache"]["billing"]["ts"]
    file_path = log_data["_source"]["dcache"]["billing"]["protocol"]["path"]
    return [file_id, action, file_size, file_type, user_id, timestamp, file_path]


if len(sys.argv) < 2:
    print("Please provide the input filename as a command-line argument.")
    sys.exit()

input_filename = sys.argv[1]

with open(input_filename, "r") as infile, open(
    "output.csv", "w", newline=""
) as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    writer.writerow(
        [
            "File ID",
            "Action",
            "File Size",
            "File Type",
            "User ID",
            "Timestamp",
            "File Path",
        ]
    )

    print("Starting to parse data...")

    for i, row in enumerate(reader):
        print("Parsing row: " + str(i))
        # current_row = i
        # if i == 0:
        #     continue
        if i == 100:  # Use this to limit the number of lines to read.
            break
        else:
            for i in range(len(row)):
                row[i] = json.dumps(ast.literal_eval(row[i]))  # Convert string to dict
                log_entry = row[i]  # Assuming the log entry is in the first column
                extracted_info = extract_info(log_entry)
                writer.writerow(extracted_info)

print("Done!")

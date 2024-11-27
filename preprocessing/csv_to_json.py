import csv
import json

# Input CSV and output JSON file names
csv_file = './prompt.csv'  # Replace with your CSV file path
json_file = 'prompt.json'  # Replace with your desired JSON file path

# Read the CSV file
data = []
with open(csv_file, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        sl_no = row['sl no']  # Adjust the column name if necessary
        prompt = row['prompt']  # Adjust the column name if necessary
        data.append({
            "source": f"source/{sl_no}.png",
            "target": f"target/{sl_no}.png",
            "prompt": prompt
        })

# Write to a JSON file
with open(json_file, mode='w', encoding='utf-8') as file:
    for entry in data:
        json.dump(entry, file)
        file.write('\n')  # Write each JSON object on a new line

print(f"JSON file written to {json_file}")
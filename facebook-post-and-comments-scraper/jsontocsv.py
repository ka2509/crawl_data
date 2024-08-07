import os
import json
import csv

# Step 1: Read the JSON file
json_file_path = 'C:/Scraping/facebook_posts.json'
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Step 2: Flatten the data structure
flattened_data = []
for post in data:
    post_text = post["post"]
    for root_comment, replies in post["comments"].items():
        for reply in replies:
            flattened_data.append([post_text, root_comment, reply])
        if not replies:  # Handle case with no replies
            flattened_data.append([post_text, root_comment, ""])

# Step 3: Save the data into a CSV file in the same directory as the JSON file
csv_file_path = os.path.splitext(json_file_path)[0] + '.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Post', 'Root Comment', 'Reply'])  # Write CSV header
    writer.writerows(flattened_data)

print(f'Data has been written to {csv_file_path}')

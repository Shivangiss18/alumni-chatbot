import csv
import random
from difflib import SequenceMatcher

# Constants for matching thresholds
EXACT_MATCH_THRESHOLD = 0.9
POSSIBLE_MATCH_THRESHOLD = 0.65

# Similarity function using SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to load data from CSV file
def load_knowledge_base(file_path):
    knowledge_base = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line_count, line in enumerate(reader):
            if line_count == 0:
                continue  # Skip header row
            if not line[0] or not line[1]:
                print(f"WARNING: Skipping row #{line_count + 1} due to missing data.")
                continue
            knowledge_base.append((line[0], line[1]))
    return knowledge_base

# Function to find matching responses
def find_response(sendMsg, knowledge_base, exact_match_threshold=EXACT_MATCH_THRESHOLD, possible_match_threshold=POSSIBLE_MATCH_THRESHOLD):
    exact_matches = []
    possible_matches = []

    for userText, botReply in knowledge_base:
        match_ratio = similar(sendMsg, userText)
        if match_ratio >= exact_match_threshold:
            exact_matches.append(botReply)
            print(f"Likely match: {userText} (Match ratio: {match_ratio:.2f})")
        elif match_ratio >= possible_match_threshold:
            possible_matches.append(botReply)
            print(f"Possible match: {userText} (Match ratio: {match_ratio:.2f})")
    
    return exact_matches, possible_matches

# Main function to get response from bot
def getResponse(sendMsg, dataset_path='data/dataset.csv'):
    knowledge_base = load_knowledge_base(dataset_path)
    
    exact_matches, possible_matches = find_response(sendMsg, knowledge_base)
    
    if exact_matches:
        return random.choice(exact_matches)
    elif possible_matches:
        return random.choice(possible_matches)
    else:
        return "IDKresponse"  # Default response if no match is found


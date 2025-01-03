import msgpack
import sys
import os
import json
from tqdm import tqdm

def inspect_msg(msg_file):
    if not os.path.isfile(msg_file):
        print(f"Input file does not exist: {msg_file}")
        return

    try:
        # Initialize progress bar for reading the MessagePack file
        with tqdm(total=1, desc="Reading MessagePack file") as pbar:
            with open(msg_file, "rb") as f:
                msgpack_data = f.read()
            pbar.update(1)
        
        # Deserialize from MessagePack to Python object
        json_data = msgpack.unpackb(msgpack_data, raw=False)
        
        # Check for 'landmarks' section
        if "landmarks" not in json_data:
            print("Error: 'landmarks' section not found.")
            return
        
        landmarks = json_data["landmarks"]
        
        # Display the type of 'landmarks'
        print(f"Type of 'landmarks': {type(landmarks)}")
        
        if isinstance(landmarks, dict):
            num_landmarks = len(landmarks)
            print(f"Number of landmarks: {num_landmarks}")
            # Display the first 5 landmarks with progress
            print("Displaying first 5 landmarks:")
            for lm_id, lm in tqdm(list(landmarks.items())[:5], desc="Processing Landmarks", unit="landmark"):
                print(f"Landmark ID: {lm_id}")
                print(json.dumps(lm, indent=4))
                print("------------------------")
        elif isinstance(landmarks, list):
            num_landmarks = len(landmarks)
            print(f"Number of landmarks: {num_landmarks}")
            # Display the first 5 landmarks with progress
            print("Displaying first 5 landmarks:")
            for lm in tqdm(landmarks[:5], desc="Processing Landmarks", unit="landmark"):
                print(json.dumps(lm, indent=4))
                print("------------------------")
        else:
            print("The format of the 'landmarks' section is unknown.")
    
    except Exception as e:
        print(f"An error occurred while reading: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python inspect_msg.py input.msg")
        sys.exit(1)
    
    input_msg = sys.argv[1]
    
    # Check if the input file exists
    if not os.path.isfile(input_msg):
        print(f"Input file does not exist: {input_msg}")
        sys.exit(1)
    
    # Perform inspection
    inspect_msg(input_msg)

if __name__ == "__main__":
    main()

from plyfile import PlyData
import sys
import os
from tqdm import tqdm

def inspect_ply(input_file):
    try:
        # Initialize progress bar for reading the PLY file
        with tqdm(total=1, desc="Reading PLY file") as pbar:
            ply = PlyData.read(input_file)
            pbar.update(1)
        
        print(f"Elements contained in PLY file '{input_file}':")
        
        # Calculate total number of properties for nested progress bars
        total_elements = len(ply.elements)
        total_properties = sum(len(element.properties) for element in ply.elements)
        
        # Initialize a main progress bar for elements and properties
        with tqdm(total=total_elements + total_properties, desc="Processing PLY elements and properties") as pbar_main:
            for element in ply.elements:
                print(f" - {element.name} ({element.count} instances)")
                pbar_main.update(1)
                
                for prop in element.properties:
                    if hasattr(prop, 'is_list') and prop.is_list:
                        print(f"    Property: {prop.name} (list {prop.count_type} {prop.item_type})")
                    else:
                        print(f"    Property: {prop.name} ({prop.dtype})")
                    pbar_main.update(1)
                    
    except Exception as e:
        print(f"Failed to read the PLY file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_ply.py input.ply")
    else:
        input_ply = sys.argv[1]
        if not os.path.isfile(input_ply):
            print(f"Input file does not exist: {input_ply}")
            sys.exit(1)
        inspect_ply(input_ply)

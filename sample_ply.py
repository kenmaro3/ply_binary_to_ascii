import open3d as o3d
import sys
import os
from tqdm import tqdm

def sample_ply(input_file, output_file, sample_size):
    try:
        # Initialize the progress bar with 3 steps: Loading, Sampling, Saving
        with tqdm(total=3, desc="Sampling PLY file") as pbar:
            # Load the input PLY file
            pcd = o3d.io.read_point_cloud(input_file)
            pbar.update(1)

            total_points = len(pcd.points)
            if sample_size >= total_points:
                print("Sample size is greater than or equal to the total number of points. Using all points.")
                sampled_pcd = pcd
            else:
                # Calculate the sampling ratio
                sampling_ratio = float(sample_size) / float(total_points)
                sampled_pcd = pcd.random_down_sample(sampling_ratio)
            pbar.update(1)
            
            # Save the sampled PLY file in ASCII format
            success = o3d.io.write_point_cloud(output_file, sampled_pcd, write_ascii=True)
            pbar.update(1)
        
        if success:
            print(f"Sampling completed successfully: {input_file} → {output_file} ({len(sampled_pcd.points)} points)")
        else:
            print("Failed to write the sampled PLY file.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python sample_ply.py input.ply output.ply sample_size")
        sys.exit(1)
    
    input_ply = sys.argv[1]
    output_ply = sys.argv[2]
    
    # Validate sample_size argument
    try:
        sample_size = int(sys.argv[3])
        if sample_size <= 0:
            raise ValueError
    except ValueError:
        print("Sample size must be a positive integer.")
        sys.exit(1)
    
    # Check if the input file exists
    if not os.path.isfile(input_ply):
        print(f"Input file does not exist: {input_ply}")
        sys.exit(1)
    
    # Perform sampling
    sample_ply(input_ply, output_ply, sample_size)

if __name__ == "__main__":
    main()

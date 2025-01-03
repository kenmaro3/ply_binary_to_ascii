import open3d as o3d
import sys
import os
from tqdm import tqdm

def binary_to_ascii_ply(input_file, output_file):
    try:
        # Initialize the progress bar with 2 steps: Reading and Writing
        with tqdm(total=2, desc="Converting PLY file") as pbar:
            # Read the binary PLY file
            ply = o3d.io.read_point_cloud(input_file)
            pbar.update(1)
            
            if not ply.has_points():
                print("The PLY file does not contain point cloud data.")
                return

            # Determine the type of PLY file (PointCloud or TriangleMesh)
            if isinstance(ply, o3d.geometry.PointCloud):
                # Write as a point cloud in ASCII format
                success = o3d.io.write_point_cloud(output_file, ply, write_ascii=True)
            elif isinstance(ply, o3d.geometry.TriangleMesh):
                # Write as a triangle mesh in ASCII format
                success = o3d.io.write_triangle_mesh(output_file, ply, write_ascii=True)
            else:
                print("Unsupported PLY file type.")
                return

            pbar.update(1)

        if success:
            print(f"Conversion completed successfully: {input_file} → {output_file}")
        else:
            print("Failed to write the ASCII PLY file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python binary_to_ascii_open3d.py input_binary.ply output_ascii.ply")
    else:
        input_ply = sys.argv[1]
        output_ply = sys.argv[2]

        if not os.path.isfile(input_ply):
            print(f"Input file does not exist: {input_ply}")
            sys.exit(1)

        binary_to_ascii_ply(input_ply, output_ply)

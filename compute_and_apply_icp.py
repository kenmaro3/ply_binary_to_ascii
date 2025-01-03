import open3d as o3d
import numpy as np
import argparse
import os
from tqdm import tqdm

def load_ply(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"PLY file not found: {file_path}")
    ply = o3d.io.read_point_cloud(file_path)
    if not ply.has_points():
        raise ValueError(f"No valid points found in: {file_path}")
    return ply

def save_ply(point_cloud, file_path):
    success = o3d.io.write_point_cloud(file_path, point_cloud, write_ascii=True)
    if not success:
        raise IOError(f"Failed to save PLY file: {file_path}")

def compute_icp(source, target, threshold=1.0, trans_init=np.identity(4)):
    # Execute the ICP algorithm
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint())
    return reg_p2p

def main():
    parser = argparse.ArgumentParser(description="Script to align two PLY models using ICP")
    parser.add_argument('--source', required=True, help="Path to the source PLY file to be aligned")
    parser.add_argument('--target', required=True, help="Path to the target PLY file")
    parser.add_argument('--output', required=True, help="Path to save the aligned source PLY file")
    parser.add_argument('--threshold', type=float, default=1.0, help="ICP distance threshold (default: 1.0)")

    args = parser.parse_args()

    try:
        # Initialize the progress bar with 4 steps: Load Source, Load Target, Compute ICP, Save Output
        with tqdm(total=4, desc="Aligning PLY files using ICP") as pbar:
            # Load the source PLY file
            source_ply = load_ply(args.source)
            print(f"Loaded source PLY file: {args.source}")
            pbar.update(1)

            # Load the target PLY file
            target_ply = load_ply(args.target)
            print(f"Loaded target PLY file: {args.target}")
            pbar.update(1)

            # Set the initial transformation matrix (identity matrix)
            trans_init = np.identity(4)

            # Compute the transformation matrix using ICP
            print("Executing ICP algorithm...")
            reg_p2p = compute_icp(source_ply, target_ply, threshold=args.threshold, trans_init=trans_init)
            transformation_matrix = reg_p2p.transformation
            print("ICP Result:")
            print(reg_p2p)
            print("Optimal Transformation Matrix:")
            print(transformation_matrix)
            pbar.update(1)

            # Apply the transformation to the source PLY
            source_ply_transformed = source_ply.transform(transformation_matrix)
            print("Applied transformation matrix to the source PLY.")
            
            # Save the transformed source PLY file
            save_ply(source_ply_transformed, args.output)
            print(f"Saved aligned PLY file: {args.output}")
            pbar.update(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

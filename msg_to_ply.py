import msgpack
import sys
import os
import open3d as o3d
from tqdm import tqdm

def msg_to_ply(msg_file, ply_file):
    if not os.path.isfile(msg_file):
        print(f"Input file does not exist: {msg_file}")
        return

    try:
        # Initialize the progress bar with 3 steps: Reading, Processing, Writing
        with tqdm(total=3, desc="Converting MSG to PLY") as pbar:
            # Read the MessagePack file
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

            # Ensure 'landmarks' is a dictionary
            if not isinstance(landmarks, dict):
                print("Error: 'landmarks' section is not in dictionary format.")
                return

            points = []
            colors = []

            # Initialize a secondary progress bar for processing landmarks
            total_landmarks = len(landmarks)
            with tqdm(total=total_landmarks, desc="Processing Landmarks", leave=False) as pbar_landmarks:
                for lm_id, lm in landmarks.items():
                    # Extract the position of each landmark
                    if "pos_w" not in lm:
                        pbar_landmarks.update(1)
                        continue
                    pos = lm["pos_w"]
                    if not isinstance(pos, list) or len(pos) != 3:
                        pbar_landmarks.update(1)
                        continue
                    x, y, z = pos
                    points.append([x, y, z])

                    # Extract color information if available (currently not present, defaulting to white)
                    # Uncomment the following code if color information is available
                    """
                    if "color" in lm:
                        color = lm["color"]
                        red = color.get("red", 255)
                        green = color.get("green", 255)
                        blue = color.get("blue", 255)
                        colors.append([red / 255.0, green / 255.0, blue / 255.0])
                    else:
                        # Default to white if color information is missing
                        colors.append([1.0, 1.0, 1.0])
                    """
                    # Default to white color
                    colors.append([1.0, 1.0, 1.0])

                    pbar_landmarks.update(1)

            print(f"Number of extracted points: {len(points)}")

            if len(points) == 0:
                print("Error: No points were extracted.")
                return

            # Create an Open3D PointCloud object
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            pcd.colors = o3d.utility.Vector3dVector(colors)

            # Write to PLY file in ASCII format
            success = o3d.io.write_point_cloud(ply_file, pcd, write_ascii=True)
            pbar.update(1)

        if success:
            print(f"Successfully converted to PLY: {ply_file} ({len(points)} points)")
        else:
            print("Failed to write the PLY file.")

    except Exception as e:
        print(f"An error occurred during conversion: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python msg_to_ply.py input.msg output.ply")
        sys.exit(1)
    else:
        input_msg = sys.argv[1]
        output_ply = sys.argv[2]
        msg_to_ply(input_msg, output_ply)

if __name__ == "__main__":
    main()

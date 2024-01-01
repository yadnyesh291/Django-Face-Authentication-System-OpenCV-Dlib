import h5py

hdf5_file_path = 'C:/Users/Asus/OneDrive/Desktop/Face/resources/face-rec_Google.h5'

try:
    with h5py.File(hdf5_file_path, 'r') as file:
        print(f"Opened HDF5 file: {hdf5_file_path}")

        # Print the keys (top-level groups/datasets)
        print("File contents:")
        print(list(file.keys()))

        # Optionally, you can explore further into the file structure
        # For example, to print the contents of a specific group:
        # group_name = 'your_group_name'
        # print(f"Contents of group '{group_name}':")
        # print(list(file[group_name].keys()))

except Exception as e:
    print(f"Error opening HDF5 file: {e}")

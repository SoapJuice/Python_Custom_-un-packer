import os

def collect_files_and_dirs(paths):
    all_files = {}
    for path in paths:
        if os.path.isfile(path):
            all_files[path] = os.path.basename(path)
        elif os.path.isdir(path):
            base_dir = os.path.normpath(path)
            for root, _, files in os.walk(base_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, os.path.dirname(base_dir))
                    all_files[full_path] = relative_path
        else:
            print(f"Path not found: {path}")
    return all_files

def pack_files(file_paths, output_file):
    with open(output_file, 'wb') as outfile:
        for full_path, local_path in file_paths.items():
            if os.path.exists(full_path):
                with open(full_path, 'rb') as infile:
                    outfile.write(b"\n-------File Location-------\n")
                    outfile.write(local_path.encode('utf-8'))
                    outfile.write(b"\n-------File Content-------\n")
                    outfile.write(infile.read())
                    outfile.write(b"\n-------End of File-------\n")
                print(f"Added: {local_path}")
            else:
                print(f"File not found: {full_path}")

def list_packed_files(packed_file):
    if not os.path.exists(packed_file):
        print(f"Packed file not found: {packed_file}")
        return

    file_locations = []
    with open(packed_file, 'rb') as infile:
        in_location_section = False
        for line in infile:
            line = line.strip()
            if line == b"-------File Location-------":
                in_location_section = True
            elif in_location_section:
                file_locations.append(line.decode('utf-8'))
                in_location_section = False

    print("Files listed in the packed file:")
    for location in file_locations:
        print(location)

if __name__ == "__main__":
    print("Enter the mode (pack/list):")
    mode = input().strip().lower()

    if mode == "pack":
        print("Enter the file paths to pack, separated by commas:")
        inputs = input().split(",")
        inputs = [path.strip() for path in inputs]  # Remove extra spaces

        print("Enter the name of the output file (e.g., output.txt):")
        output_file = input().strip()

        all_files = collect_files_and_dirs(inputs)

        pack_files(all_files, output_file)
        print(f"Files packed into {output_file}")

    elif mode == "list":
        print("Enter the name of the packed file to list (e.g., output.txt):")
        packed_file = input().strip()
        list_packed_files(packed_file)

    else:
        print("Invalid mode. Please enter 'pack' or 'list'.")

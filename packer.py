import os

def collect_files_and_dirs(paths):
    """
    Collect all files from a list of paths, including directories and their contents.

    Args:
        paths (list of str): List of file and directory paths.

    Returns:
        dict: A dictionary mapping full paths to local paths (relative to the provided base directory).
    """
    all_files = {}
    for path in paths:
        if os.path.isfile(path):
            all_files[path] = os.path.basename(path)
        elif os.path.isdir(path):
            base_dir = os.path.abspath(path)
            for root, _, files in os.walk(base_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, os.path.dirname(base_dir))
                    all_files[full_path] = relative_path
        else:
            print(f"Path not found: {path}")
    return all_files

def pack_files(file_paths, output_file):
    """
    Pack multiple files into a single file by concatenating their contents.

    Args:
        file_paths (dict): Dictionary mapping full paths to local paths to include in the output file.
        output_file (str): Name of the output file.
    """
    with open(output_file, 'wb') as outfile:
        for full_path, local_path in file_paths.items():
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'rb') as infile:
                        content = infile.read()
                        char_count = len(content)
                        outfile.write(b"\n-------File Location-------\n")
                        outfile.write(f"{local_path}".encode('utf-8'))
                        outfile.write(b"\n-------Character Count-------\n")
                        outfile.write(f"{char_count}".encode('utf-8'))
                        outfile.write(b"\n-------File Content-------\n")
                        outfile.write(content)
                        outfile.write(b"\n-------End of File-------\n")
                    print(f"Added: {local_path} ({char_count} characters)")
                except Exception as e:
                    print(f"Error adding file {local_path}: {e}")
            else:
                print(f"File not found: {full_path}")

def list_packed_files(packed_file):
    """
    List all file paths stored in a packed file.

    Args:
        packed_file (str): The packed file to read from.
    """
    if not os.path.exists(packed_file):
        print(f"Packed file not found: {packed_file}")
        return

    try:
        with open(packed_file, 'rb') as infile:
            while True:
                line = infile.readline()
                if not line:
                    break
                line = line.strip()

                if line == b"-------File Location-------":
                    file_location = infile.readline().strip().decode('utf-8')
                    print(file_location)

                elif line == b"-------Character Count-------":
                    char_count = int(infile.readline().strip().decode('utf-8'))
                    infile.seek(char_count, os.SEEK_CUR)

                elif line == b"-------End of File-------":
                    continue

    except Exception as e:
        print(f"Error reading packed file: {e}")


def unpack_files(packed_file, target_dir):
    """
    Unpack files from a packed file into a specified directory.

    Args:
        packed_file (str): The packed file to read from.
        target_dir (str): The directory where the files will be unpacked.
    """
    if not os.path.exists(packed_file):
        print(f"Packed file not found: {packed_file}")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    try:
        with open(packed_file, 'rb') as infile:
            file_location = None
            char_count = None

            while True:
                line = infile.readline()
                if not line:
                    break  # EOF
                line = line.strip()

                if line == b"-------File Location-------":
                    file_location = infile.readline().strip().decode('utf-8')
                elif line == b"-------Character Count-------":
                    char_count = int(infile.readline().strip().decode('utf-8'))
                elif line == b"-------File Content-------":
                    content = infile.read(char_count)
                    file_path = os.path.join(target_dir, file_location)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as file_out:
                        file_out.write(content)
                    print(f"Unpacked: {file_location} ({char_count} characters)")
                elif line == b"-------End of File-------":
                    file_location = None
                    char_count = None
    except Exception as e:
        print(f"Error unpacking file: {e}")

def main():
    while True:
        print("\nEnter the mode (pack/list/unpack/exit):")
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

        elif mode == "unpack":
            print("Enter the name of the packed file to unpack (e.g., output.txt):")
            packed_file = input().strip()

            print("Enter the target directory to unpack files into:")
            target_dir = input().strip()

            unpack_files(packed_file, target_dir)

        elif mode == "exit":
            print("Exiting the script. Goodbye!")
            break

        else:
            print("Invalid mode. Please enter 'pack', 'list', 'unpack', or 'exit'.")

if __name__ == "__main__":
    main()

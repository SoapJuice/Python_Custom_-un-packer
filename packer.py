import os

def collect_files_and_dirs(paths):
    all_files = []
    for path in paths:
        if os.path.isfile(path):
            all_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    all_files.append(os.path.join(root, file))
        else:
            print(f"Path not found: {path}")
    return all_files

def pack_files(file_paths, output_file):
    with open(output_file, 'wb') as outfile:
        for file in file_paths:
            if os.path.exists(file):
                with open(file, 'rb') as infile:
                    outfile.write(b"\n-------File Location-------\n")
                    outfile.write(file.encode('utf-8'))
                    outfile.write(b"\n-------File Content-------\n")
                    outfile.write(infile.read())
                    outfile.write(b"\n-------End of File-------\n")
                print(f"Added: {file}")
            else:
                print(f"File not found: {file}")

print("Enter the file paths to pack, separated by commas:")
inputs = input().split(",")
inputs = [path.strip() for path in inputs]

print("Enter the name of the output file (e.g., output.txt):")
output_file = input().strip()

all_files = collect_files_and_dirs(inputs)

pack_files(all_files, output_file)
print(f"Files packed into {output_file}")

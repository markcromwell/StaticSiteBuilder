import os
import shutil


def copy_static_files(source_dir = "static", dest_dir = "public"):
    """
    Copies static files from the source directory to the destination directory.

    :param source_dir: The directory containing the static files.
    :param dest_dir: The directory where static files should be copied.
    """
    static_path = source_dir
    if not os.path.exists(static_path):
        print(f"No static directory found at {static_path}. Skipping copy.")
        return
    
    if os.path.exists(dest_dir) and not os.path.isdir(dest_dir):
        raise ValueError(f"Destination path {dest_dir} exists and is not a directory.")


    # Use dest_dir here (dest_subdir was undefined). Remove redundant recursion
    # since os.walk already traverses subdirectories.
    print(f"Copying {source_dir} to {dest_dir}")
    if os.path.exists(dest_dir) and os.path.isdir(dest_dir):
        print(f"Destination directory {dest_dir} already exists. Deleting.")
        shutil.rmtree(dest_dir)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(static_path):
        relative_path = os.path.relpath(root, static_path)
        # Normalize relative_path: '.' should map to dest_dir
        if relative_path == '.' or relative_path == './':
            dest_path = dest_dir
        else:
            dest_path = os.path.join(dest_dir, relative_path)

        os.makedirs(dest_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            with open(src_file, 'rb') as fsrc:
                with open(dest_file, 'wb') as fdst:
                    fdst.write(fsrc.read())
            print(f"Copied {src_file} to {dest_file}")
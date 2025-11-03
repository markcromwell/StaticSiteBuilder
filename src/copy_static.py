import os
import shutil
import logging

logger = logging.getLogger(__name__)


def copy_static_files(source_dir="static", dest_dir="public"):
    """Copy files from source_dir to dest_dir preserving metadata.

    If source_dir doesn't exist the function returns without creating dest_dir.
    If dest_dir exists and is not a directory, raises ValueError.
    If dest_dir exists as a directory, it is removed before copying.
    """
    static_path = source_dir
    if not os.path.exists(static_path):
        logger.info("No static directory found at %s. Skipping copy.", static_path)
        return

    if os.path.exists(dest_dir) and not os.path.isdir(dest_dir):
        raise ValueError(f"Destination path {dest_dir} exists and is not a directory.")

    logger.info("Copying %s to %s", source_dir, dest_dir)

    if os.path.exists(dest_dir) and os.path.isdir(dest_dir):
        logger.info("Destination directory %s already exists. Deleting.", dest_dir)
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir, exist_ok=True)

    for root, dirs, files in os.walk(static_path):
        relative_path = os.path.relpath(root, static_path)
        if relative_path == '.' or relative_path == './':
            dest_path = dest_dir
        else:
            dest_path = os.path.join(dest_dir, relative_path)

        os.makedirs(dest_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dest_file)
            logger.info("Copied %s to %s", src_file, dest_file)
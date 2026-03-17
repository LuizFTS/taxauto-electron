import glob
import os


def change_spreadsheet_filename(directory_path: str, new_name: str) -> bool:
    """
    Finds the most recently modified .csv file in a directory and renames it.

    Args:
        directory_path (str): Path to the folder to search.
        new_name (str): The desired new filename (e.g., 'final_report.csv').

    Returns:
        bool: True if successful, False otherwise.
    """
    # 1. Create the search pattern
    search_pattern = os.path.join(directory_path, "*.csv")

    # 2. List all files matching the pattern
    files = glob.glob(search_pattern)

    if not files:
        print(f"[ERROR] No .csv files found in: {directory_path}")
        return False

    # 3. Identify the latest file based on modification time (mtime)
    latest_file = max(files, key=os.path.getmtime)

    # 4. Ensure the new name has the .csv extension
    if not new_name.lower().endswith(".csv"):
        new_name += ".csv"

    new_file_path = os.path.join(directory_path, new_name)

    try:
        # 5. Perform the rename operation
        os.rename(latest_file, new_file_path)
        print(f"[SUCCESS] '{os.path.basename(latest_file)}' renamed to '{new_name}'")
        return True

    except FileExistsError:
        print(f"[ERROR] A file named '{new_name}' already exists in this directory.")
        return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False

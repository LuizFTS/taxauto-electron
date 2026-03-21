import csv
import glob
import os


def get_branch_from_csv(file_path: str) -> str | None:
    """
    Reads cell B4 (row 4, column B) from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        str | None: The value at B4, or None if not found/readable.
    """
    try:
        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 3:  # Row 4 (0-indexed)
                    if len(row) >= 2 and row[1].strip():
                        return row[1].strip()
                    break
    except Exception as e:
        print(f"[WARN] Could not read B4 from '{os.path.basename(file_path)}': {e}")
    return None


def resolve_unique_filepath(directory_path: str, base_name: str) -> str:
    """
    Resolves a unique file path by appending _2, _3, etc. if the name already exists.

    Args:
        directory_path (str): Target directory.
        base_name (str): Desired filename without extension (e.g., '05_ENTRADA').

    Returns:
        str: A full file path guaranteed not to conflict with existing files.
    """
    candidate = os.path.join(directory_path, f"{base_name}.csv")
    if not os.path.exists(candidate):
        return candidate

    counter = 2
    while True:
        candidate = os.path.join(directory_path, f"{base_name}_{counter}.csv")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def change_spreadsheet_filename(
    directory_path: str, fallback_filial: str, book_type: str
) -> bool:
    """
    Finds the most recently modified .csv file in a directory and renames it.

    The new filename is built from the branch number found at cell B4 inside the
    file itself. If B4 is empty or unreadable, `fallback_filial` is used instead.
    If a file with the resolved name already exists, a numeric suffix (_2, _3, ...)
    is appended to avoid collisions.

    Args:
        directory_path (str): Path to the folder to search.
        fallback_filial (str): Branch identifier used when B4 cannot be read.
        book_type (str): Book type label used in the filename (e.g., 'ENTRADA').

    Returns:
        bool: True if successful, False otherwise.
    """
    # 1. Find all .csv files in the directory
    search_pattern = os.path.join(directory_path, "*.csv")
    files = glob.glob(search_pattern)

    if not files:
        print(f"[ERROR] No .csv files found in: {directory_path}")
        return False

    # 2. Pick the most recently modified file
    latest_file = max(files, key=os.path.getmtime)

    # 3. Try to read the branch number from B4; fall back to filial if missing
    branch = get_branch_from_csv(latest_file)
    if branch:
        print(f"[INFO] Branch read from B4: '{branch}'")
    else:
        branch = str(fallback_filial)
        print(f"[INFO] B4 not found — using fallback filial: '{branch}'")

    # 4. Build the base name and resolve a unique path
    base_name = f"{branch.zfill(2)}_{book_type.upper()}"
    new_file_path = resolve_unique_filepath(directory_path, base_name)
    new_name = os.path.basename(new_file_path)

    try:
        os.rename(latest_file, new_file_path)
        print(f"[SUCCESS] '{os.path.basename(latest_file)}' → '{new_name}'")
        return True
    except Exception as e:
        print(f"[ERROR] Rename failed: {e}")
        return False
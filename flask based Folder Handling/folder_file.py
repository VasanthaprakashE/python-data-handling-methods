from pathlib import Path
import pandas as pd

def read_folder_to_dfs(folderpath: str | Path) -> dict[str, pd.DataFrame] | None:

    try:
        folder = Path(folderpath)

        if not folder.is_dir():
            print(f"Error: {folderpath} is not a valid directory.")
            return None

        readers = {
            '.csv': pd.read_csv,
            '.xlsx': pd.read_excel,
            '.xls': pd.read_excel,
            '.json': pd.read_json
        }

        dataframes = {}

        # Recursive search
        for file in folder.rglob("*"):

            if file.is_file():

                reader = readers.get(file.suffix.lower())

                if reader:
                    try:
                        # Keep relative path as key
                        key = file.relative_to(folder).as_posix()

                        dataframes[key] = reader(file)

                        print(f"Loaded: {key}")

                    except Exception as e:
                        print(f"Could not read {file}: {e}")

        return dataframes if dataframes else None

    except Exception as e:
        print(f"Critical process failure: {e}")
        return None
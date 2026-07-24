from pathlib import Path
import pandas as pd

def read_folder_to_dfs(folderpath: str | Path) -> dict[str, pd.DataFrame] | None:
    """Validates a folder path and reads all CSV, Excel and JSON files into a dictionary."""
    try:
        folder = Path(folderpath)
        
        # Guard clause: immediate exit if path is invalid
        if not folder.is_dir():
            print(f"Error: {folderpath} is not a valid directory.")
            return None
            
        # Optimization: Map extensions directly to Pandas reader functions for speed
        readers = {
            '.csv': pd.read_csv,
            '.xlsx': pd.read_excel,
            '.xls': pd.read_excel,
            '.json': pd.read_json
        }
        
        # Single-pass loop: scans, filters, and reads files in one go
        dataframes = {}
        for file in folder.iterdir():
            if file.is_file() and (reader := readers.get(file.suffix.lower())):
                try:
                    dataframes[file.name] = reader(file)
                except Exception as file_error:
                    print(f"Skipping corrupted file {file.name}: {file_error}")
                    
        return dataframes if dataframes else None
        
    except Exception as e:
        print(f"Critical process failure: {e}")
        return None

from flask import Flask, render_template, request
from pathlib import Path
import os
import shutil
from folder_file import read_folder_to_dfs
import openpyxl

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    if UPLOAD_FOLDER.exists():
        shutil.rmtree(UPLOAD_FOLDER)

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    files = request.files.getlist("files")

    for file in files:

        if file.filename == "":
            continue

        filepath = UPLOAD_FOLDER / file.filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        file.save(filepath)

    dfs = read_folder_to_dfs(UPLOAD_FOLDER)

    if dfs is None:
        return "No supported files found."

    import pandas as pd
    combined_df = pd.concat(dfs.values(),ignore_index=True)

    combined_df = combined_df[combined_df['Zone'].fillna("") != ""]

    return render_template(
    "result.html",
    table=combined_df.to_html(index=False, classes="table table-striped"),
    rows=len(combined_df),
    columns=len(combined_df.columns),
    files=len(dfs))



if __name__ == "__main__":
    app.run(debug = True)
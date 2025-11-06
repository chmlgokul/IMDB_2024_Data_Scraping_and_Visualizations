import os
import subprocess

project_path = r"D:\data_science_based\data_science\guvi_ds\projects\IMDB_2024_Data_Scraping_and_Visualizations\final"

streamlit_file = "IMDB_2024_Data_Scraping_and_Visualizations_v002.py"

os.chdir(project_path)

subprocess.run(["streamlit", "run", streamlit_file], shell=True)

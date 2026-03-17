import pandas as pd

path = r"C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (4)\002_ENTRADA.csv"

df = pd.read_csv(path, sep=";")

print(df.head())

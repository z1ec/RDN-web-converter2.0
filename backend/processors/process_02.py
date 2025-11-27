import pandas as pd

def process(file_path):
    df = pd.read_excel(file_path)

    # ЛЮБАЯ ТВОЯ ЛОГИКА
    df["Шаблон"] = "02 обработан"

    return df

import pandas as pd

def process(file_path):
    df = pd.read_excel(file_path)

    # ЛЮБАЯ ТВОЯ ЛОГИКА
    df["Шаблон"] = "00 обработан"

    return df

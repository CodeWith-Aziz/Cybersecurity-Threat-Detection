import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_data(path):
    df = pd.read_csv(path)
    return df

def preprocess_data(df):
    df = df.dropna()

    le = LabelEncoder()
    for col in df.select_dtypes(include='object'):
        df[col] = le.fit_transform(df[col])

    X = df.drop("label", axis=1)
    y = df["label"]

    return train_test_split(X, y, test_size=0.2, random_state=42)
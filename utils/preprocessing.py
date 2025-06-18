import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_csv_data(path, column='Close'):
    df = pd.read_csv(path)
    df = df.dropna()
    print("📋 Original columns:", df.columns.tolist())

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Rename 'Close/Last' to 'Close' for consistent access
    if 'Close/Last' in df.columns:
        df.rename(columns={'Close/Last': 'Close'}, inplace=True)

    print("✅ Columns after rename:", df.columns.tolist())

    # Clean dollar signs and convert to float
    df['Close'] = df['Close'].replace('[\$,]', '', regex=True).astype(float)

    return df[[column]]

def preprocess_data(df, sequence_length=60):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    X, y = [], []
    for i in range(sequence_length, len(scaled)):
        X.append(scaled[i-sequence_length:i])
        y.append(scaled[i])

    return np.array(X), np.array(y), scaler

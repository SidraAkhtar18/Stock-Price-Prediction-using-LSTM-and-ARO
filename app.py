import streamlit as st
import pandas as pd
from utils.preprocessing import preprocess_data
from models.lstm_model import build_lstm_model
from optimization.aro_optimizer import artificial_rabbit_optimization
from utils.metrics import evaluate
from utils.plot import plot_results
import numpy as np

st.title("📈 Stock Price Prediction with LSTM and ARO")
uploaded_file = st.file_uploader("Upload your stock CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file) 
    # Strip spaces from columns and rename Close/Last to Close
    df.columns = [col.strip().replace('Close/Last', 'Close') for col in df.columns]
    st.write("Original DataFrame columns:", list(df.columns))
    
    # Extract Close column only and convert to numeric after removing $ and commas
    df_close = df[['Close']].copy()
    df_close['Close'] = pd.to_numeric(df_close['Close'].astype(str).str.replace('[\$,]', '', regex=True))
    st.write("Preview of Close prices:")
    st.write(df_close.head(100))   
    # Preprocess data with only Close prices
    X, y, scaler = preprocess_data(df_close)
    # Train/test split
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]   
    # Hyperparameter space
    space = {
        "units": [32, 50, 64],
        "dropout": [0.2, 0.3],
        "batch": [16, 32],
        "epochs": [10, 20]
    }
    st.write("🔍 Starting hyperparameter optimization...")
    
    def objective(params):
        model = build_lstm_model(X_train.shape[1:], params['units'], params['dropout'])
        model.fit(X_train, y_train, epochs=params['epochs'], batch_size=params['batch'], verbose=0)
        pred = model.predict(X_test)
        _, _, rmse = evaluate(y_test, pred)
        return rmse   
    best_params = artificial_rabbit_optimization(space, objective_fn=objective, n_iter=5)
    st.success(f"✅ Best Hyperparameters: {best_params}")
    # Train final model with best hyperparameters
    model = build_lstm_model(X_train.shape[1:], best_params['units'], best_params['dropout'])
    model.fit(X_train, y_train, epochs=best_params['epochs'], batch_size=best_params['batch'])
    pred = model.predict(X_test)   
    mae, mse, rmse = evaluate(y_test, pred)
    st.write(f"### Final Evaluation Metrics:")
    st.write(f"- MAE: {mae:.4f}")
    st.write(f"- MSE: {mse:.4f}")
    st.write(f"- RMSE: {rmse:.4f}")
    st.write("### Prediction vs Actual plot:")
    plot_results(y_test, pred)
else:
    st.info("Please upload a CSV file to start.")

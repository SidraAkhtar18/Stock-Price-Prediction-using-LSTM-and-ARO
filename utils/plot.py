import matplotlib
matplotlib.use('TkAgg')  # ya 'Qt5Agg' agar aapke paas Qt installed hai
import matplotlib.pyplot as plt

def plot_results(y_true, y_pred):
    plt.figure(figsize=(10, 4))
    plt.plot(y_true, label='Actual')
    plt.plot(y_pred, label='Predicted')
    plt.legend()
    plt.title("Stock Price Prediction")
    plt.savefig("stock_prediction.png")  # image save kar do
    plt.show()  # interactive window khol do

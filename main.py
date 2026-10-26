from src.data_preprocessing import load_data, preprocess_data
from src.model import train_model
from src.evaluate import evaluate_model
from src.detect import detect_threats

def main():
    df = load_data("data/dataset.csv")

    X_train, X_test, y_train, y_test = preprocess_data(df)

    model = train_model(X_train, y_train)

    preds = evaluate_model(model, X_test, y_test)

    detect_threats(preds)

if __name__ == "__main__":
    main()
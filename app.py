import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

st.title("🔐 AI Cybersecurity Threat Detection Dashboard")

# 🔹 FILE UPLOAD
st.sidebar.header("📂 Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# 🔹 MODEL SELECTION
st.sidebar.header("⚙️ Model Settings")
model_choice = st.sidebar.selectbox(
    "Select Model",
    ["Random Forest", "Isolation Forest"]
)

# 🔹 LOAD DATA
if file is not None:
    df = pd.read_csv(file)
else:
    df = pd.read_csv("data/dataset.csv")

st.subheader("📊 Dataset Preview")
st.write(df.head())

# 🔹 PREPROCESSING
df = df.dropna()

le = LabelEncoder()
for col in df.select_dtypes(include='object'):
    df[col] = le.fit_transform(df[col])

if "label" not in df.columns:
    st.error("Dataset must contain 'label' column")
    st.stop()

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔹 MODEL TRAINING
if model_choice == "Random Forest":
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

else:
    model = IsolationForest(contamination=0.2)
    model.fit(X_train)
    preds = model.predict(X_test)
    preds = [1 if p == -1 else 0 for p in preds]


    # 🔹 FEATURE IMPORTANCE (Only for Random Forest)
if model_choice == "Random Forest":
    st.subheader("🧠 Important Features for Threat Detection")

    importances = model.feature_importances_
    feature_names = X.columns

    feature_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    st.write(feature_df.head(10))

    # Plot
    fig3, ax3 = plt.subplots()
    ax3.barh(feature_df["Feature"][:10], feature_df["Importance"][:10])
    ax3.invert_yaxis()
    st.pyplot(fig3)

# 🔹 METRICS
accuracy = accuracy_score(y_test, preds)

# 🔹 TIMELINE (Simulated if no timestamp exists)
st.subheader("⏳ Threat Detection Timeline")



# If dataset doesn't have time, create fake timeline
if "timestamp" not in df.columns:
    df["timestamp"] = pd.date_range(start="2024-01-01", periods=len(df), freq="min")

timeline_df = pd.DataFrame({
    "timestamp": df["timestamp"].iloc[-len(preds):].values,
    "prediction": preds
})

timeline_df = timeline_df.set_index("timestamp")

# Plot timeline
st.line_chart(timeline_df["prediction"])

# 🔹 SUMMARY CARDS
st.subheader("📈 Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Threats Detected", sum(preds))
col3.metric("Accuracy", f"{accuracy*100:.2f}%")
col4.metric("Model Used", model_choice)

# 🔹 GRAPH
st.subheader("📊 Attack vs Normal Distribution")

preds = list(preds)
normal = preds.count(0)
attack = preds.count(1)

fig, ax = plt.subplots()
ax.bar(["Normal", "Attack"], [normal, attack])
st.pyplot(fig)

# 🔹 CONFUSION MATRIX
st.subheader("📉 Confusion Matrix")

cm = confusion_matrix(y_test, preds)
fig2, ax2 = plt.subplots()
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(ax=ax2)
st.pyplot(fig2)

# 🔹 ALERTS
st.subheader("🚨 Threat Alerts")

for i, val in enumerate(preds[:50]):
    if val == 1:
        st.warning(f"⚠️ Threat detected at index {i}")

# 🔹 DOWNLOAD OUTPUT
st.subheader("📥 Download Results")

result_df = X_test.copy()
result_df["Actual"] = y_test.values
result_df["Predicted"] = preds

csv = result_df.to_csv(index=False)

st.download_button(
    label="Download Prediction Results",
    data=csv,
    file_name="results.csv",
    mime="text/csv",
)
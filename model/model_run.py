import joblib
import pandas as pd
import kagglehub
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pathlib import Path


# Download dataset
print("Downloading heart disease dataset...")
path = kagglehub.dataset_download("johnsmith88/heart-disease-dataset")

# Find and load the CSV file
dataset_path = Path(path)
csv_file = next(dataset_path.rglob("*.csv"))
df = pd.read_csv(csv_file)

# Prepare data
X = df.drop('target', axis=1)
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model to a joblib file
joblib.dump(model, 'model/heart_model.joblib')

print("Model trained and saved successfully.")


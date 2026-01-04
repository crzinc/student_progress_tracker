import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from pathlib import Path
import os

def create_model():
    # Load the dataset
    df = pd.read_csv('/Users/amiramiraslanov/Documents/ML-projects/student_prediction/sample_data/student-mat.csv', sep=';')
    
    # Create binary target: 1 if final grade (G3) >= 10, else 0
    df['success'] = (df['G3'] >= 10).astype(int)
    
    # Select features - using the same features as in the notebook
    feature_columns = [
        'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 
        'failures', 'famrel', 'freetime', 'goout', 'Dalc', 
        'Walc', 'health', 'absences'
    ]
    
    # One-hot encode categorical variables
    categorical = ['Medu', 'Fedu', 'traveltime', 'studytime', 'famrel', 
                  'freetime', 'goout', 'Dalc', 'Walc', 'health']
    
    # Convert categorical columns to string type for one-hot encoding
    for col in categorical:
        df[col] = df[col].astype(str)
    
    # One-hot encode categorical variables
    df_encoded = pd.get_dummies(df[feature_columns], columns=categorical)
    
    # Split data
    X = df_encoded
    y = df['success']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Get feature importances
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 most important features:")
    print(feature_importance.head(10))
    
    # Save model
    model_dir = Path(__file__).resolve().parent
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / 'student_performance_model.pkl'
    
    # Save the model and feature names
    model_data = {
        'model': model,
        'feature_names': X.columns.tolist(),
        'categorical_columns': categorical
    }
    
    joblib.dump(model_data, model_path)
    print(f"\nModel saved to {model_path}")

if __name__ == "__main__":
    create_model()
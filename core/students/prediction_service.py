import joblib
from pathlib import Path
import pandas as pd
from django.conf import settings

class StudentPerformancePredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = Path(settings.BASE_DIR) / 'students' / 'ml_models' / 'student_performance_model.pkl'

        self.model = None
        self.feature_names = []
        self.categorical_columns = []
        self._use_one_hot = False

        try:
            model_data = joblib.load(model_path)

            if isinstance(model_data, dict) and 'model' in model_data:
                self.model = model_data['model']
                self.feature_names = model_data.get('feature_names', [])
                self.categorical_columns = model_data.get('categorical_columns', [])
                self._use_one_hot = True
            else:
                # Backward compatibility: previously we saved only the estimator.
                self.model = model_data
                self.feature_names = list(getattr(self.model, 'feature_names_in_', []))
                self.categorical_columns = []
                self._use_one_hot = False
        except Exception:
            self.model = None
    
    def preprocess_input(self, student_data):
        if self.model is None:
            return pd.DataFrame([student_data])

        student_df = pd.DataFrame([student_data])

        if self._use_one_hot:
            for col in self.categorical_columns:
                if col in student_df.columns:
                    student_df[col] = student_df[col].astype(str)

            student_encoded = pd.get_dummies(student_df, columns=[c for c in self.categorical_columns if c in student_df.columns])

            for feature in self.feature_names:
                if feature not in student_encoded.columns:
                    student_encoded[feature] = 0

            student_encoded = student_encoded[self.feature_names]
            return student_encoded

        if not self.feature_names:
            self.feature_names = list(student_df.columns)

        for col in self.feature_names:
            if col not in student_df.columns:
                student_df[col] = 0

        return student_df[self.feature_names]

    def explain(self, student_data, top_n=5):
        try:
            if self.model is None:
                return []

            if not hasattr(self.model, 'feature_importances_'):
                return []

            processed = self.preprocess_input(student_data)
            row = processed.iloc[0]
            importances = getattr(self.model, 'feature_importances_', None)
            if importances is None:
                return []

            scores = []
            for i, feature in enumerate(processed.columns):
                if i >= len(importances):
                    break
                value = row[feature]
                imp = float(importances[i])
                scores.append((imp * (abs(float(value)) if value is not None else 0.0), feature, value, imp))

            scores.sort(reverse=True, key=lambda x: x[0])
            result = []
            for _, feature, value, imp in scores[:top_n]:
                result.append({
                    'feature': str(feature),
                    'value': float(value) if value is not None else 0.0,
                    'importance': float(imp),
                })
            return result
        except Exception:
            return []
    
    def predict_success_probability(self, student_data):
        try:
            if self.model is None:
                return 0.5

            # Preprocess input
            processed_data = self.preprocess_input(student_data)
            
            # Get prediction probabilities
            proba = self.model.predict_proba(processed_data)
            
            # Handle both 1D and 2D probability arrays
            if proba.ndim == 1:  # If binary classification with predict_proba() returns 1D array
                return float(proba[0])
            else:  # If predict_proba() returns 2D array [prob_class_0, prob_class_1]
                return float(proba[0][1])
        
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return 0.5  # Return neutral probability on error

# Create a default predictor instance
predictor = StudentPerformancePredictor()
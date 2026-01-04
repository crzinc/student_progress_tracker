# In students/management/commands/retrain_model.py
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Retrain the student performance prediction model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-path',
            type=str,
            default=None,
            help='Path to the CSV dataset (semicolon-separated), e.g. student-mat.csv'
        )

    def handle(self, *args, **options):
        self.stdout.write('Training student performance prediction model...')
        
        # Load and preprocess data
        if not options.get('data_path'):
            raise CommandError('Missing --data-path. Example: python manage.py retrain_model --data-path /path/to/student-mat.csv')

        data_path = Path(options['data_path']).expanduser()
        if not data_path.exists():
            raise CommandError(f'Dataset not found: {data_path}')

        df = pd.read_csv(data_path, sep=';')
        
        # Create binary target (1 if G3 >= 10, else 0)
        df['success'] = (df['G3'] >= 10).astype(int)
        
        # Select features (same as create_initial_model.py)
        features = [
            'age', 'Medu', 'Fedu', 'traveltime', 'studytime',
            'failures', 'famrel', 'freetime', 'goout', 'Dalc',
            'Walc', 'health', 'absences'
        ]

        categorical = ['Medu', 'Fedu', 'traveltime', 'studytime', 'famrel',
                      'freetime', 'goout', 'Dalc', 'Walc', 'health']

        X = df[features].copy()

        for col in categorical:
            if col in X.columns:
                X[col] = X[col].astype(str)

        X = pd.get_dummies(X, columns=categorical)
        y = df['success']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        self.stdout.write(
            self.style.SUCCESS(f'Model trained successfully!\n'
                             f'Training accuracy: {train_score:.2f}\n'
                             f'Test accuracy: {test_score:.2f}')
        )
        
        # Save model
        model_dir = Path(__file__).parent.parent.parent / 'ml_models'
        os.makedirs(model_dir, exist_ok=True)
        model_path = model_dir / 'student_performance_model.pkl'

        model_data = {
            'model': model,
            'feature_names': X.columns.tolist(),
            'categorical_columns': categorical,
        }

        joblib.dump(model_data, model_path)
        self.stdout.write(self.style.SUCCESS(f'Model saved to {model_path}'))
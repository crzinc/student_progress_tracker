# Student Progress Tracker

Student Progress Tracker is a Django web app for managing student profiles and predicting academic success probability using a scikit-learn model trained on the Student Performance dataset.

## Features

- CRUD for student profiles
- Automatic success probability prediction after saving a student
- Success probability progress bar
- “Key Factors” section based on model feature importances

## Tech Stack

- Django (project root is `core/`)
- SQLite (default database)
- scikit-learn + pandas + joblib
- HTML templates with Tailwind-like utility classes (no frontend build step)

## Quickstart

Important: `manage.py` is inside the `core/` directory.

```bash
# from repo root
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cd core
python manage.py migrate
python manage.py runserver
```

Open:

- `http://127.0.0.1:8000/students/`

## Project Structure

```text
student-progress-tracker/
  README.md
  requirements.txt
  core/
    manage.py
    core/
      settings.py
      urls.py
      wsgi.py
      asgi.py
    students/
      models.py
      views.py
      forms.py
      signals.py
      prediction_service.py
      ml_models/
        create_initial_model.py
        student_performance_model.pkl
      templates/
        students/
          student_list.html
          student_form.html
          student_detail.html
```

## Usage

- List: `/students/`
- Create: `/students/add/`
- Edit: `/students/<id>/edit/`
- Detail: `/students/<id>/`

`success_probability` is recalculated automatically via `students/signals.py` when relevant fields change.

## ML Model

### Dataset

The training dataset is the “Student Performance” dataset (semicolon-separated CSV, e.g. `student-mat.csv`).

### Target

Binary classification:

- `success = 1` if `G3 >= 10`
- `success = 0` otherwise

### Features

- `age`
- `Medu`, `Fedu`
- `traveltime`, `studytime`
- `failures`
- `famrel`, `freetime`, `goout`
- `Dalc`, `Walc`
- `health`
- `absences`

Categorical columns are one-hot encoded.

### Model artifact

The app loads the model from:

`core/students/ml_models/student_performance_model.pkl`

The pickle is stored as a dict:

- `model`
- `feature_names`
- `categorical_columns`

### Train / Retrain

Option A (script):

```bash
cd core/students/ml_models
python create_initial_model.py
```

Option B (recommended, management command):

```bash
cd core
python manage.py retrain_model --data-path /absolute/path/to/student-mat.csv
```

After training, restart `runserver` to reload the model.

## Troubleshooting

### `python: can't open file .../manage.py`

You ran Django commands from the wrong directory.

Correct:

```bash
cd core
python manage.py runserver
```

### `TypeError: list indices must be integers or slices, not str`

Your `.pkl` is in an unexpected format.

Fix:

- retrain using `python manage.py retrain_model ...`
- or re-run `create_initial_model.py`

## License

MIT. See `LICENSE`.

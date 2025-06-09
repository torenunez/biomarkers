# Biomarkers Tracker

A web application for tracking personal biomarkers and health metrics over time.

## Features

- Track various biomarkers (weight, blood tests, etc.)
- Set reference ranges for each biomarker
- View historical data and trends
- Add notes to measurements

## Technical Stack

- Python 3.8+
- Django 4.2
- SQLite (development)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/torenunez/biomarkers.git
cd biomarkers
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin to access the admin interface.

## Project Structure

```
biomarkers/
├── biomarkers/          # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── admin.py         # Admin interface
│   └── tests.py         # Tests
├── config/              # Project configuration
│   ├── settings.py      # Settings
│   └── urls.py         # URL routing
└── manage.py           # Django management script
```

## Models

### BiomarkerCategory
- name: Name of the biomarker
- description: Optional description
- unit: Unit of measurement
- reference_range_min: Minimum normal value
- reference_range_max: Maximum normal value

### BiomarkerRecord
- user: User who owns the record
- category: Reference to BiomarkerCategory
- value: Measured value
- date_recorded: When the measurement was taken
- notes: Optional notes

## License

MIT License
# django-admin-favorite-filters

## Local development

### Installation

1. Clone _django_admin_favorite_filters_ to a local repo.
1. Install Poetry.
1. Run `poetry install` (installs the defined dependencies in a virtual environment).
1. Navigate to your local Django project where you want to install the package.
1. In your project's virtual environment, run `pip install -e "/path/to/django_admin_favorite_filters_local_repo/"` (ensures that the package is installed in "editable" or "development" mode).
1. Add 'django_admin_favorite_filters' to INSTALLABLE_APPS in the `settings.py` file of your project.

### Testing

1. To run tests for the package, run `poetry run pytest`

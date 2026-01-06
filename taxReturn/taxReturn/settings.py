"""
Django settings for taxReturn project
Production + Local safe configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key-for-local")

# DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS = [
#     "localhost",
#     "127.0.0.1",
#     ".onrender.com",
# ]
DEBUG = True
ALLOWED_HOSTS = ['*']  # temporarily for Render

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "taxApp",
    "accounts",
    "itr",
]

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# URL / WSGI
# =========================
ROOT_URLCONF = "taxReturn.urls"
WSGI_APPLICATION = "taxReturn.wsgi.application"

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================
# DATABASE (PostgreSQL)
# =========================
DATABASES = {
     "default": {
        # "ENGINE": "django.db.backends.postgresql",
        # "NAME": "Taxapp",
        # "USER": "postgres",
        # "PASSWORD": "Tax@1234",
        # "HOST": "127.0.0.1",   # localhost ki jagah ye use kar
        # "PORT": "5432",
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "taxreturn_db_kveu",  # Render DB name
        "USER": "taxreturn_db_kveu_user",  # Render DB username
        "PASSWORD": "RDXRPvrltOvQC6hmOtJaXSf4ipc4FTDA",  # Render DB password
       "HOST": "dpg-d5blu3p5pdvs73bnh8sg-a", 
        "PORT": "5432",  # Render DB port
    }
}

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================
# STATIC & MEDIA FILES
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# AI CONFIG (SAFE MODE)
# =========================
AI_CONFIG = {} if not DEBUG else {
    "MODEL_PATH": BASE_DIR / "data/models",
    "EMBEDDINGS_PATH": BASE_DIR / "data/processed/embeddings",
    "DOCUMENTS_PATH": BASE_DIR / "data/raw",

    "EMBEDDING_MODEL": "sentence-transformers/all-mpnet-base-v2",
    "SIMILARITY_THRESHOLD": 0.7,
    "MAX_RESULTS": 5,
}

# =========================
# CELERY / REDIS (OPTIONAL)
# =========================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

"""
Django settings for jaytipargal project.
Jayti Pargal - Personal Life Companion Website
Created with love by Vivek
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'jayti-pargal-personal-companion-2026-secret-key-for-birthday')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Allowed hosts - handles Railway's dynamic hostnames
# Railway sets its own hostname dynamically, so we need to allow all Railway domains
_default_hosts = 'localhost,127.0.0.1'
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS', _default_hosts)
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_ENV.split(',') if h.strip()]

# Railway deployment: Add Railway domain patterns
# Railway domains follow pattern: *.up.railway.app
railway_domains = ['.up.railway.app', '*.up.railway.app']
for domain in railway_domains:
    if domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(domain)

# Also add any RAILWAY_STATIC_URL domain if present
railway_static_url = os.environ.get('RAILWAY_STATIC_URL', '')
if railway_static_url:
    from urllib.parse import urlparse
    parsed = urlparse(railway_static_url)
    if parsed.hostname and parsed.hostname not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(parsed.hostname)

# Additional Railway environment variables
railway_public_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
if railway_public_domain and railway_public_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_public_domain)

# If running on Railway without explicit ALLOWED_HOSTS, allow all (for debugging)
# In production, you should set explicit ALLOWED_HOSTS
if os.environ.get('RAILWAY_ENVIRONMENT') and not os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.append('*')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'core',
    'notes',
    'diary',
    'goals',
    'astro',
    'ai_chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files on cloud
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jaytipargal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.user_profile',
                'core.context_processors.birthday_check',
                'core.context_processors.daily_inspiration',
            ],
        },
    },
]

WSGI_APPLICATION = 'jaytipargal.wsgi.application'

# Database Configuration
# Uses PostgreSQL in production (via DATABASE_URL), SQLite for local development
# Railway deployment: DATABASE_URL is auto-injected when PostgreSQL is provisioned

def get_database_config():
    """
    Get database configuration with proper SSL handling for Railway.
    Returns a dict compatible with Django DATABASES setting.
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Production: Use PostgreSQL with Railway
        # Parse the URL and handle SSL properly
        config = dj_database_url.parse(
            database_url,
            conn_max_age=600,
        )
        
        # Add SSL mode for Railway PostgreSQL (required for connections)
        # Railway requires SSL for external connections
        if 'OPTIONS' not in config:
            config['OPTIONS'] = {}
        
        # Handle sslmode properly for psycopg2
        # Railway requires SSL but we need to pass it correctly
        config['OPTIONS']['sslmode'] = 'require'
        
        return config
    else:
        # Development: Use SQLite
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }

DATABASES = {
    'default': get_database_config()
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Kolkata')  # Delhi timezone for Jayti
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise for serving static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout redirects
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Jayti's birthday configuration
JAYTI_BIRTH_DATE = int(os.environ.get('BIRTH_DATE_DAY', 6))
JAYTI_BIRTH_MONTH = int(os.environ.get('BIRTH_DATE_MONTH', 2))  # February

# Astrology settings
JAYTI_BIRTH_DETAILS = {
    'year': 1997,
    'month': 2,
    'day': 6,
    'hour': 22,
    'minute': 30,
    'latitude': 28.61,
    'longitude': 77.21,
    'location': 'Delhi, India',
    'timezone': 'Asia/Kolkata'
}

# Gemini API Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-pro')

# Google Service Account Credentials (for Gemini/Vertex AI)
# Option 1: JSON content directly in environment variable
GOOGLE_CREDENTIALS_JSON = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON', '')

# Option 2: Path to credentials file
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')

# Handle Google credentials for Railway deployment
import tempfile
import json

if GOOGLE_CREDENTIALS_JSON:
    # Write JSON credentials to temp file for Google libraries
    try:
        # Validate JSON first
        json.loads(GOOGLE_CREDENTIALS_JSON)
        
        # Create temp file
        creds_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        creds_file.write(GOOGLE_CREDENTIALS_JSON)
        creds_file.close()
        
        # Set path for Google libraries
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_file.name
        GOOGLE_APPLICATION_CREDENTIALS = creds_file.name
        
        print(f"✓ Google credentials loaded from environment variable")
    except json.JSONDecodeError as e:
        print(f"⚠️ Invalid GOOGLE_CREDENTIALS_JSON: {e}")

# Configure Gemini with service account if available
try:
    if GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CREDENTIALS_JSON:
        import google.generativeai as genai
        
        # If using service account, configure accordingly
        if GOOGLE_APPLICATION_CREDENTIALS and os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
            # For Vertex AI / Service account authentication
            genai.configure()
            print("✓ Gemini configured with service account")
        elif GEMINI_API_KEY:
            # Standard API key authentication
            genai.configure(api_key=GEMINI_API_KEY)
            print("✓ Gemini configured with API key")
except ImportError:
    print("⚠️ google-generativeai not installed")
except Exception as e:
    print(f"⚠️ Gemini configuration error: {e}")

# Logging configuration - Enhanced for Railway debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'goals': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create logs directory if it doesn't exist (skip on Railway if read-only)
LOGS_DIR = BASE_DIR / 'logs'
try:
    LOGS_DIR.mkdir(exist_ok=True)
except OSError:
    # Fallback to /tmp for Railway or other read-only filesystems
    LOGS_DIR = Path('/tmp') / 'jaytipargal' / 'logs'
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    # Update logging file handler path
    LOGGING['handlers']['file']['filename'] = LOGS_DIR / 'django.log'

# Railway-specific settings
RAILWAY_DEBUG = os.environ.get('RAILWAY_DEBUG', 'false').lower() == 'true'
if RAILWAY_DEBUG:
    # More verbose logging in debug mode
    LOGGING['loggers']['django']['level'] = 'DEBUG'
    LOGGING['handlers']['console']['level'] = 'DEBUG'

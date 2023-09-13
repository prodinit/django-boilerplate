"""
Django settings for {{cookiecutter.project_name}} project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import environ
from corsheaders.defaults import default_headers
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: ROOT_DIR / 'subdir'.
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("{{ cookiecutter.main_module }}")
# APPS_DIR = ROOT_DIR.path("dummy")

env = environ.Env()

# INSTALLED APPS
# ==========================================================================
# List of strings representing installed apps.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.postgres",
    "django_sites",  # http://niwinz.github.io/django-sites/latest/
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "rest_framework",  # http://www.django-rest-framework.org/
    # "mail_templated",  # https://github.com/artemrizhov/django-mail-templated
    "django_extensions",  # http://django-extensions.readthedocs.org/
    "drf_yasg",
    "versatileimagefield",  # https://github.com/WGBH/django-versatileimagefield/
    "corsheaders",  # https://github.com/ottoyiu/django-cors-headers/
]

LOCAL_APPS = [
    # "users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# AUTH CONFIGURATION
# ==========================================================================

# django.contrib.auth
# ------------------------------------------------------------------------------
# AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 6},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# DJANGO CORE
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
# Defaults to false, which is safe, enable them only in development.
DEBUG = env.bool("DJANGO_DEBUG", False)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "{{ cookiecutter.timezone }}"
# TIME_ZONE = "UTC"

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

# Languages we provide translations for
LANGUAGES = (("en", _("English")),)

if USE_TZ:
    # Add timezone information to datetime displayed.
    # https://mounirmesselmeni.github.io/2014/11/06/date-format-in-django-admin/
    from django.conf.locale.en import formats as en_formats

    en_formats.DATETIME_FORMAT = "N j, Y, P (e)"


# A tuple of directories where Django looks for translation files.
LOCALE_PATHS = (str(APPS_DIR.path("locale")),)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# The list of directories to search for fixtures
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# The Python dotted path to the WSGI application that Django's internal servers
# (runserver, runfcgi) will use. If `None`, the return value of
# "django.core.wsgi.get_wsgi_application" is used, thus preserving the same
# behavior as previous versions of Django. Otherwise this should point to an
# actual WSGI application object.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "wsgi.application"

# URL CONFIGURATION
# ------------------------------------------------------------------------------
ROOT_URLCONF = "{{ cookiecutter.main_module }}.urls"
# ROOT_URLCONF = "dummy.urls"

# Use this to change base url path django admin
DJANGO_ADMIN_URL = env.str("DJANGO_ADMIN_URL", default="admin")


# TEMPLATE CONFIGURATION
# -----------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                # Your stuff: custom template context processors go here
            ],
        },
    }
]


WSGI_APPLICATION = '{{ cookiecutter.main_module }}.wsgi.application'
# WSGI_APPLICATION = 'dummy.wsgi.application'


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Using unix socket for postgres connection by default
DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///elevator")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = 10


# STATIC FILE CONFIGURATION
# -----------------------------------------------------------------------------
# Absolute path to the directory static files should be collected to.
# Example: "/var/www/example.com/static/"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(APPS_DIR.path(".staticfiles"))

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://example.com/static/", "http://static.example.com/"
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# A list of locations of additional static files
STATICFILES_DIRS = (str(APPS_DIR.path("static")),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


#  SECURITY
# -----------------------------------------------------------------------------
CSRF_COOKIE_HTTPONLY = False  # Allow javascripts to read CSRF token from cookies
SESSION_COOKIE_HTTPONLY = True  # Do not allow Session cookies to be read by javascript

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# django-log-request-id - Sending request id in response
REQUEST_ID_RESPONSE_HEADER = "REQUEST_ID"

# CORS
# --------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_HEADERS = default_headers + ("access-control-allow-origin",)

# rest_framework
# ------------------------------------------------------------------------------
DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + ("rest_framework.renderers.BrowsableAPIRenderer",)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10000/day",
    },
}
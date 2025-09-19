INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "ads",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# Replace with actual GitHub Pages domain
CORS_ALLOWED_ORIGINS = [
    "https://calebstrait.github.io",
]

INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "ads",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]

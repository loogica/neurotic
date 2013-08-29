DATABASES = { ########## IN-MEMORY TEST DATABASE
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

SECRET_KEY = "neurotic"

INSTALLED_APPS = (
    'app2',
)

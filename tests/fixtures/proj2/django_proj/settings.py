DATABASES = { ########## IN-MEMORY TEST DATABASE
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

SECRET_KEY = "neurotic"

INSTALLED_APPS = (
    'app1',
)

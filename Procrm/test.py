import os

from django.forms import models


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Procrm.settings")
    import django

    django.setup()
    from crm import models
    persons = models.Person.objects.all()
    print(persons)

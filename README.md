<a href="https://lapzone.tech" target="_blank"><img title="LapZone" alt="Header image" src="./static/images/site_header.webp"></a>

_Internet shop for selling laptops and accessories for them_

### Demo

Click **<a href="https://lapzone.tech" target="_blank">here</a>** to open LapZone internet shop

<p><img title="Demo" alt="Demo image" src="./md_images/demo.jpg"></p>

### Project modules (production)

<a href='https://pypi.org/project/Django'><img alt='Django' src='https://img.shields.io/pypi/v/Django?label=Django&color=blue'></a> <a href='https://pypi.org/project/django-allauth'><img alt='django-allauth' src='https://img.shields.io/pypi/v/django-allauth?label=django-allauth&color=blue'></a> <a href='https://pypi.org/project/django-ckeditor'><img alt='django-ckeditor' src='https://img.shields.io/pypi/v/django-ckeditor?label=django-ckeditor&color=blue'></a> <a href='https://pypi.org/project/django-js-asset'><img alt='django-js-asset' src='https://img.shields.io/pypi/v/django-js-asset?label=django-js-asset&color=blue'></a> <a href='https://pypi.org/project/django-recaptcha3'><img alt='django-recaptcha3' src='https://img.shields.io/pypi/v/django-recaptcha3?label=django-recaptcha3&color=blue'></a> <a href='https://pypi.org/project/psycopg2'><img alt='psycopg2' src='https://img.shields.io/pypi/v/psycopg2?label=psycopg2&color=blue'></a> <a href='https://pypi.org/project/python-dotenv'><img alt='python-dotenv' src='https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv&color=blue'></a> <a href='https://pypi.org/project/pytz'><img alt='pytz' src='https://img.shields.io/pypi/v/pytz?label=pytz&color=blue'></a>

---

### Site structure

The system consists of the following main functional blocks:

-   Registration, authentication and authorization;
-   Guest functionality;
-   User functionality;
-   Admin functionality.

#### Project apps

-   Shop (for working with displaying product lists, product details, brands, etc.);
-   Customer (for working with user profiles and pages that are connected with them);
-   Cart (for working with a user's or guest's cart through sessions);
-   Order (for working with user orders and payments);
-   Mailing (for working with mailing).

#### Technology stack

-   Backend:
    -   Python programming language;
    -   Django framework with the following extensions:
        -   django-allauth;
        -   django-ckeditor;
        -   django-recaptcha3.
    -   PostgreSQL database (Django ORM);
-   Frontend:
    -   HTML & CSS;
    -   JavaScript;
    -   Bootstrap 5.

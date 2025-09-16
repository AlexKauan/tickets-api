# DRF Tickets API

API básica (DRF + CBVs) para gestão de **Eventos**, **Clientes**, **Ingressos** e **Notificações**.

## Stack

- Django, Django REST Framework, django-filter

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

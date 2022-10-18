# sms_api

 #### Migrations:
 
>To init:
>
> - check  project/migrations/env.py (import models)
> - alembic revision --autogenerate -m "init"
> - alembic upgrade head
> 
>To upgrade:
>
> - Change model, or add
> - alembic revision --autogenerate -m "comment"
> - alembic upgrade head

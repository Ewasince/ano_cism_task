### create initial

~~~
alembic revision --autogenerate -m 'initial'
~~~

### create more - migration_1_2

~~~
alembic revision --autogenerate -m 'm_1_2'

~~~

### apply

~~~
alembic upgrade head
~~~

### stamp

~~~
alembic stamp <revision>
alembic stamp heads
~~~

### manual stamp existing DB

~~~
alembic stamp d8e54b7593dd
~~~
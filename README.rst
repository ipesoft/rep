==============
Regional Flora
==============

Regional Flora is a web application designed to store and share data about regional flora (with emphasis in trees), including descriptive, ethnobotany and historical data. The idea is to:

- Facilitate restoration and urban forestry efforts by providing detailed information and search capabilities related to the native flora of a certain region;
- Promote the interest of the general public in the native vegetation;
- Combine history, ethnobotany and forest data in a new way, including information about the use of each species and its relationship with the local community over the time;
- Provide a replicable model that can be applied to other regions interested in a similar system.

This work is part of a larger project funded by the JRS Biodiversity Foundation and coordinated by IPÊ (Instituto de Pesquisas Ecológicas) for the region of Nazaré Paulista, São Paulo, Brazil.

The system was developed in Python using the Django Framework.

Features
========

The system is still under development and only the first module is currently available, including an administrative interface to register species data and a public interface to search and browse the registered species. More than 50 fields can be used to describe species, including taxonomic data, synonyms, vernacular names, special features for urban forestry, data about ecology and reproduction, as well as data for restoration such as guidelines for seedling production. The two other modules to be developed are related to ethnobotany and history, respectively.

Installation
============

Besides a web server, you'll need Django and a relational database compatible with Django. The application was developed with Apache 2.2, PostgreSQL 8.4 and Django 1.3. After installing the basic software, create a new database, copy settings.py.ref to settings.py and edit the configuration. If you want to learn more about Django settings you can look at: https://docs.djangoproject.com/en/1.3/topics/settings/

When you finihsed editing the file, run the following command to create the tables:

::

  python manage.py syncdb

You'll also be prompted to create a superuser account. After that, you can start the Django server to test the system:

::

  python manage.py runserver

Use your superuser credentials to log into the administrative interface where you can create other users and include species data: http://127.0.0.1:8000/admin

Then try the public interface to search and visualize your data: http://127.0.0.1:8000

==============
Regional Flora
==============

Regional Flora is a web application designed to store and share data about regional flora (with emphasis in trees), including descriptive, ethnobotany and historical data. The idea is to:

- Facilitate restoration and urban forestry efforts by providing detailed information and search capabilities related to the native flora of a certain region;
- Promote the interest of the general public in the native vegetation;
- Combine history, ethnobotany and forest data in a new way, including information about the use of each species and its relationship with the local community over the time;
- Provide a replicable model that can be applied to other regions interested in a similar system.

This work is part of a larger project funded by the JRS Biodiversity Foundation and coordinated by IPÊ (Instituto de Pesquisas Ecológicas) and originally created for the region of Nazaré Paulista, São Paulo, Brazil.

The system was developed in Python using the Django Framework.

Features
========

- Searchable database of plants with more than 50 fields including description, taxonomic data, synonyms, vernacular names, uses, special features for urban forestry, data about ecology and reproduction, as well as data for restoration such as guidelines for seedling production (the database must be populated according to the Flora of a particular region).
- Possibility to share species data with the Encyclopedia of Life.
- Images stored on Flickr and shared with the Encyclopedia of Life are also displayed on the system.
- Ethnobotany data can be stored by indicating specific uses for the plants and a special description. 
- Historical data can be stored by means of interviews, including textual content and audio. A specific tagging mechanism can be used in the content allowing interviews to be linked with species. Another tagging mechanism can be used to select highlights from the interview.
- Species, ethnobotany and history are all interlinked, for instance allowing users reading an interview to click on a species mentioned in the text to access more details about it, including ethnobotany information and images.
- Administrative interface to manage data.
- Customizable public interface to search and browse existing content.
- Internationalized system, with English and Portuguese languages ready to use.

Installation
============

Besides a web server, you'll need Python, Django and a relational database compatible with Django. The application was developed with Apache 2.2, PostgreSQL 8.4 and Django 1.5.1. After installing the basic software, create a new database, copy settings.py.ref to settings.py and edit the configuration. If you want to learn more about Django settings you can look at: https://docs.djangoproject.com/en/1.5/topics/settings/

In particular, you need to pay attention to the following parts:

::

  ADMINS --> include your name and e-mail.

  DATABASES --> include all necessary database settings.

  ALLOWED_HOSTS --> specify one or more domains for your system.

  TIME_ZONE --> time zone for your django installation (based on your server locale).

  LANGUAGE_CODE --> default language for your system.

  LOCALE_PATHS --> replace with the absolute path to your django app + /locale
                   add more paths if you have other locale files

  STATIC_ROOT --> you may want to set this to the absolute path of your django app + /static

  STATICFILES_DIRS --> you may need to include the contrib/admin/static dir of your django
                       installation to get the administrative interface working properly.

  SECRET_KEY --> replace with a new value of your own

  TEMPLATE_DIRS --> specify the two template directories:
                    absolute path to your django app + /templates
                    absolute path to your django app + /treebeard/templates

  BASE_TEMPLATE --> replace with your own template, if necessary.

  CONTACT_LINK --> contact e-mail to be displayed on the standard menu.

  PDF_ROOT --> absolute path to your django app + /docs

  FLICKR_API_KEY --> your flickr api key (register at flicker and get the key)

  The following entries must also be completed for sharing data with EoL:
  GUID_FORMAT, SPECIES_URL_FORMAT, HABITAT_DESCRIPTION, CREATOR_NAME, 
  CREATOR_HOMEPAGE, CREATOR_LOGO_URL, COMPILERS

When you finihsed editing the file, run the following command to create the tables:

::

  python manage.py syncdb

You'll also be prompted to create a superuser account. After that, you can start the Django server to test the system:

::

  python manage.py runserver

Use your superuser credentials to log into the administrative interface where you can create other users and start populating the database: http://127.0.0.1:8000/admin

Then try the public interface to search and visualize your data: http://127.0.0.1:8000

Species data
============

**Registering data**

Use the administrative interface to include all data for each species. You may first add as many users/groups as necessary with the corresponding permissions. Note that users should be marked as being part of the "staff" to be able to access the admin interface.

**Sharing with the Encyclopedia of Life**

The following program can be manually run from you django project directory to produce a zipped XML compatible with one of the EoL data standards:

::

  ./manage.py export_data app

The file will be called eol.zip and you will find it under your EOL_FILE_LOCATION. To generate that file periodically, you can put the same command in your crontab.

To start sharing data, first create an account in eol.org and then create a new content partner associated with it. You will need to specify a URL from where EoL can periodically fetch the file.

**Displaying images**

To display Flickr images, you have to create an account on Flickr and then get an API key that you must include in your settings file as FLICKR_API_KEY. There is a command line program that you need to run periodically (for instance using crontab) to check if there are images on Flickr. You can manually run it from your django project directory using:

::

  ./manage.py check_flickr app

Please note that only images that were shared with the EoL Flickr group are searched and displayed. Check the EoL documentation about how to share images with EoL using Flickr.

Interviews
==========

Text Format

Tagging

Static pages
============

Content for static pages can be included in the Django administrative interface (Page class). The default website menu requires pages with the following codes to be registered:

- about: Content about the website/project.
- methods: Content about the methods used.
- ethno_overview: Overview about the ethnobotany work.
- ethno_results: Results for the ethnobotany work.
- hist_overview: Overview about history work.

Customizing the look & feel
===========================

Templates

Internationalization


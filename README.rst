==============
Regional Flora
==============

Regional Flora is a web application designed to store and share data about regional flora (with emphasis in trees), including descriptive, ethnobotany and historical data. The idea is to:

- Facilitate restoration and urban forestry efforts by providing detailed information and search capabilities related to the native flora of a certain region;
- Promote the interest of the general public in the native vegetation;
- Combine history, ethnobotany and forest data in a new way, including information about the use of each species and its relationship with the local community over the time;
- Provide a replicable model that can be applied to other regions interested in a similar system.

This work is part of a larger project funded by the JRS Biodiversity Foundation and coordinated by IPÊ (Instituto de Pesquisas Ecológicas) and originally created for the region of Nazaré Paulista, São Paulo, Brazil.

The system was developed in Python using the Django Framework. You can find a working example here:

http://flora.ipe.org.br

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

Besides a web server, you'll need Python (>=3), Django (>=3), a relational database compatible with Django, the Python module reportlab and the Django modules django-tiny-mce (3.0.1) and django treebeard (4.3.1). This application was developed with Apache 2.4, PostgreSQL 10.15, Python 3.6 and Django 3.1.1. After installing the basic software, create a new database, copy rep/settings.py.ref to rep/settings.py and edit the configuration. If you want to learn more about Django settings you can look at: https://docs.djangoproject.com/en/3.1/topics/settings/

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
  GUID_FORMAT, SPECIES_URL_FORMAT, CREATOR_NAME, 
  CREATOR_HOMEPAGE, CREATOR_LOGO_URL, COMPILERS

When you finihsed editing the file, run the following command to create the tables:

::

  python manage.py syncdb

You'll also be prompted to create a superuser account.

To export all static content to its final destination, use:

::

  ./manage.py collectstatic


After that, you can start the Django server to test the system:

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

Interviews can be included using the administrative interface. Their content must be in plain text following this format:

::

  Person1: Hello, this is an example.
  Person2: OK.

Paragraphs are separated by line breaks. Any initial word with less than 30 characters followed by ': ' is interpreted as the name of a person and is formatted accordingly.

Highlights and links must be manually typed. Highlights start with a particular HTML anchor belonging to the "part" class and end with an HTML horizontal line of the same class:

::

  Someone: Some previous conversation.
  <a class="part" id="1">Interesting part</a>
  Person1: In my childhood I used to visit a special tree in the forest. Some more text, followed or not by opther talks.<hr class="part"/>

You need to pay attention to the highlight id. Each highlight needs its own unique identifier that is manually assigned. Such highlights are automatically detected, indexed and displayed when you save the interview. The same happens with species tags. There are three kinds of species tags:

1) Link to a particular species in the system:

In this case, first you need to find out the species identifier in the system and then add an HTML link like this:

::

  <a href="/sp/28" class="sp_citation">cedro</a>

To find out the species identifier you can navigate the system and click on the species page. You'll notice that the page address follows exactly the pattern above, showing the identifier after 'sp/'.

2) Link to any species with a given vernacular name:

This is a common situation, when somene refers to a species using a vernacular name that can actually correspond to different species. In this case, change the link pattern to:

::

  <a href="/sp/?name=jacarandá" class="sp_citation">Jacarandá</a>

This will tell the system to search for all species with that particular name when someone clicks on the link.

3) Link to a species that is not registered in the system:

You may also want to capture species citations even if the species is not present in your database. Use the following pattern in such cases:

::

  <a class="sp_citation">eucalipto</a>

Before tagging all species citations, you may run the following program which tried to find in your interview all species names that are registered in your database:

::

  ./manage.py detect_citations app [-i --interview interview id]

If you have an audio file for the interview, you can simply put it somewhere accessible on the web and then specify the URL when editing the interview. The system uses JPlayer to play audio, so make sure your file is in one of the supported formats: mp3 or mp4 (AAC/H.264) for both HTML5 or Flash websites, or ogg vorbis and wav for HTML5 websites.

Static pages
============

Content for static pages can be included in the Django administrative interface (Static content class). The default website menu requires pages with the following codes to be registered:

- main: Main page.
- about: Content about the website/project.
- methods: Content about the methods used.
- ethno_overview: Overview about the ethnobotany work.
- ethno_results: Results for the ethnobotany work.
- hist_overview: Overview about history work.
- faq: Frequently asked questions page.

If you click on one of the menu links and the corresponding page is not registered in the database, an HTTP 404 error is raised.

Note that more than one page can be included with the same code - each for a different language. To add more language options you need to edit your settings.py file.

Customizing the look & feel
===========================

The system comes with a generic built-in look & feel that can be customized. Most part of this work can be accomplished just by creating a my_base.html template inside your app/templates directory that, when present, replaces the base.html template. You can use anything in your new template, but make sure to include the following Django template blocks that are used by the other derived pages: header, body_params and content. Also start your template with {% load i18n %} to activate internationalization tags.

In the same way, you may create a my_page.html to replace the static content template, or a my_500.html to replace the Internal Server Error page.

New URL patterns can be specified using a my_urls.py.

More languages can be added by editing the settings.py file. After that, follow the standard Django procedure for dealing with translations. First run this command to generate the new translation file:

::

  django-admin.py makemessages --locale=my_new_lang_code

Then edit the new file located under locale/my_new_lang_code/LC_MESSAGES/django.po to make all translations. After that, run the following command to compile the translations:

::

  django-admin.py compilemessages --locale=my_new_lang_code


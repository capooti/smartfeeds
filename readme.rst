* checkout Sm@rtFeeds::

    $ git clone https://github.com/capooti/smartfeeds.git
    
* create a virtual environment and activate it::

    $ virtualenv --no-site-packages env
    $ . env/bin/activate
    
* add a local_settings.py file::
    
    $ cp local_settings.py.tmpl local_settings.py
    
* edit the local_settings.py file with your database and other credentials

* sync the database and create a superuser::

    $ python manage.py syncdb --all

* Download the GeoNames database::

    $ wget http://download.geonames.org/export/dump/allCountries.zip
    $ unzip allCountries.zip

* Then run ogr2ogr to import the .csv file to PostGIS::

    $ ogr2ogr -f PostgreSQL PG:"dbname='smartfeeds' host='localhost' port='5432' user='myuser' password='mypassword'" geonames.csv geonames
    
* For perfomance reasons::

    smartfeeds=# delete from geonames where length(asciiname)>255;
    smartfeeds=# alter table geonames alter column asciiname type character varying(255);

* In case you want to limit the search just to populated places::

    smartfeeds=# select * INTO geonames from geonames_full where featcode='PPL';
    
* Create the index to speed the text search::

    smartfeeds=# CREATE INDEX geonames_lower_idx
      ON geonames
      USING btree
      (lower(asciiname::text) COLLATE pg_catalog."default" );

* Schedule the importing processes in crontab. Copy the crontab.sh.tmpl file to crontab.sh and modify it as needed::

    $ cp crontab.sh.tmpl crontab.sh
    
* Open the crontab and schedule it as per your need::

    $ crontab -e
    */5 * * * * /home/capooti/git/github/capooti/smartfeeds/crontab.sh > /tmp/smartfeeds.log 2>&1

* Run the server, create a Search object and wait for tweets and feeds

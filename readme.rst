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
    
* Import GeoNames using a GDAL virtual driver. Create this geonames.vrt file::

    <OGRVRTDataSource>
    <OGRVRTLayer name="geonames">
    <SrcDataSource>CSV:allCountries.txt</SrcDataSource>
    <Field name="geonameid" type="String" width="255" />
    <Field name="name" type="String" width="255" />
    <Field name="asciiname" type="String" width="255" />
    <Field name="latitude" type="Real" />
    <Field name="longitude" type="Real" />
    <GeometryType>wkbPoint</GeometryType>
    <LayerSRS>EPSG:4326</LayerSRS>
    <GeometryField encoding="PointFromColumns" x="latitude" y="longitude"/>
    </OGRVRTLayer>
    </OGRVRTDataSource>

* Then run ogr2ogr to import the .csv file to PostGIS::

    $ ogr2ogr -f PostgreSQL PG:"dbname='smartfeeds' host='localhost' port='5432' user='youruser' password='yourpassword'" geonames.vrt
    
* Create the index to speed the text search::

    CREATE INDEX geonames_lower_idx
      ON geonames
      USING btree
      (lower(name::text) COLLATE pg_catalog."default" );

* Schedule the importing processes in crontab. Copy the crontab.sh.tmpl file to crontab.sh and modify it as needed::

    $ cp crontab.sh.tmpl crontab.sh
    
* Open the crontab and schedule it as per your need::

    $ crontab -e
    */5 * * * * /home/capooti/git/github/capooti/smartfeeds/crontab.sh > /tmp/smartfeeds.log 2>&1

* Run the server, create a Search object and wait for tweets and feeds

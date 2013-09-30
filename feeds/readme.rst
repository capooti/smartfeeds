Import GeoNames, virtual driver::

    <OGRVRTDataSource>
    <OGRVRTLayer name="geonames">
    <SrcDataSource>geonames.csv</SrcDataSource>
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

Then ogr2ogr::

    $ ogr2ogr -f PostgreSQL PG:"dbname='smartfeeds' host='localhost' port='5432' user='smartfeeds' password='smartfeeds'" geonames.vrt
    
Create the index::

    CREATE INDEX geonames_lower_idx
      ON geonames
      USING btree
      (lower(name::text) COLLATE pg_catalog."default" );

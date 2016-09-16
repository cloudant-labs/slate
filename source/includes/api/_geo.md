## Geo

> Example design document:

```json
{
  "_id": "_design/geo_index_example",
  "indexes": {
    "geo_index": {
      "index": "function (doc) { ... }"
    }
  }
}
```

> Example geo index:

```
function (doc) {
  st_index(doc.geolocation);
}
```

> Example GeoJSON object:

```json
{ 
  "properties": { 
    "Name": "Quinlan's Ice Cream", 
    "Status": "Delicious" 
  }, 
  "type": "Feature", 
  "geometry": { 
    "coordinates": [-10.0, 10.0],
    "type": "Point" 
  }
} 

```

<aside class="notice" role="complementary" aria-label="onlyondedicated">Geo indexing is only available on dedicated clusters who purchased the feature.</aside>

Geo indexing allows you to perform sophisticated geo-spatial queries returning documents based on their geometric relationships.

The `st_index` function specifically indexes objects, called geometries, encoded as [GeoJSON](http://geojson.org/geojson-spec.html). GeoJSON objects which the `st_index` function can index must have a `geometry` field, containing the object's geometry ([examples here](http://geojson.org/geojson-spec.html#appendix-a-geometry-examples)), and a `type` field with the value `Feature`. The optional `properties` object can contain any fields and values; it's purely for your use as the developer.

### Queries

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_ID/_geo/$INDEX_NAME?g=$GEOMETRY&relation=$RELATION \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.request({
  db: $DATABASE,
  path: ['_design', $DESIGN_ID, '_geo', $GEO_INDEX].join('/'),
  params: {
    g: $GEOMETRY,
    relation: $RELATION
  }
}, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Once you've got an index written, you can query it with a GET request to `https://<account>.cloudant.com/<database>/<design_document_id>/_geo/<index_name>`. All geo queries must provide these two query arguments: `relation` (a relation) and `g` (a geometry). Cloudant returns every document in the database whose indexed geometry has the specified relationship to the given geometry.

#### Geometries

```
POLYGON(
  (
    -106.4739990234375%2039.774769485295465,
    -106.1553955078125%2040.23760536584024,
    -105.4193115234375%2040.11588965267845,
    -105.2655029296875%2039.61838363831913,
    -105.457763671875%2039.42346418978382,
    -106.20483398437499%2039.342794408952386,
    -106.4739990234375%2039.774769485295465
  )
)
```

Geometries are specified by the `g` query parameter, and indicate the geometry against which all indexed geometries will be compared and related. Use any of the following formats to specify a geometry in the query:

Function | Arguments | Description
---------|-----------|-------------
`POINT` | (x, y) | A single 2d point
`MULTIPOINT` | ((x1, y1), (x2, y2), ...) | Multiple unrelated 2d points
`LINESTRING` | (x1, y1, x2, y2, ...) | A line constructed from a series of 2d points
`MULTILINESTRING` | ((x1, y1, x2, y2, ...), (x3, y3, x4, y4, ...)) | Multiple lines constructed from multiple series of 2d points
`POLYGON` | ((x1, y1, x2, y2, x3, y3, ...)) | A polygon constructed by connecting a series of 2d points
`POLYGON` | ((x1, y1, x2, y2, x3, y3, ...), (x4, y4, x5, y5, x6, y6, ...)) | A polygon constructed by connecting a series of 2d points, with the area of a second polygon removed from it.
`MULTIPOLYGON` | (((x1, y1, x2, y2, x3, y3, ...)), ((x4, y4, x5, y5, x6, y6, ...))) | Multiple polygons constructed by connecting multiple series of 2d points. Each polygon takes the same arguments as the `POLYGON` geometry.
`GEOMETRYCOLLECTION` | * | A collection of arbitrary geometries, ex: `POINT(4, 6),LINESTRING(4, 6, 7, 10)`

<!--
`CIRCULARSTRING` | TODO | TODO
`COMPOUNDCURVE` | TODO | TODO
`CURVEPOLYGON` | TODO | TODO
`MULTICURVE` | TODO | TODO
`MULTISURFACE` | TODO | TODO
`CURVE` | TODO | TODO
`SURFACE` | TODO | TODO
`POLYHEDRALSURFACE` | TODO | TODO
`TIN` | TODO | TODO
`TRIANGLE` | TODO | TODO
-->

#### Relations

Relations are specified by the `relation` query parameter, and indicate how indexed geometries must relate to the geometry specified in the query.

Relation | Description
---------|------------
`disjoint` | True if the two geometries do not touch or intersect
`bbox` | True if indexed geometry is within the given geometry. This is equivalent to the opposite of `disjoint`
`equals` | True if the two geometries are the same
`intersect` | True if the two geometries intersect.
`touches` | True if and only if the only common points of the two geometries are in the union of the boundaries of the geometries
`crosses` | True if the intersection of the two geometries results in a value whose dimension is less than the geometries and the maximum dimension of the intersection value includes points interior to both the geometries, and the intersection value is not equal to either of the geometries
`within` | True if the indexed geometry is wholly inside the given geometry
`contains` | True if the given geometry is wholly inside the indexed geometry
`overlaps` | True if the intersection of the geometries results in a value of the same dimension as the geometries that is different from both of the geometries

#### Radius

```shell
curl \
  -H "Content-Type: application/json" \
  -u "$USERNAME:$PASSWORD" \
  'http://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_ID/_geo/$INDEX_NAME\
  ?radius=100\
  &lat=0\
  &lon=0\
  &relation="within"'
```

```javascript
var nano = require('nano');
var account = nano("https://"+$USERNAME+":"+$PASSWORD+"@"+$USERNAME+".cloudant.com");

account.request({
  db: $DATABASE,
  path: ['_design', $DESIGN_ID, '_geo', $GEO_INDEX].join('/'),
  params: {
    radius: 100,
    lat: 0,
    lon: 0,
    relation: '"within"'
  }
}, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Rather than use the `g` parameter, queries regarding a radius use the `radius`, `lat`, and `lon` parameters.

Specifying `lat`, `lon`, and `radius` creates a circle centered at that latitude ('lat') and longitude ('lon') with the given radius in meters, and compares each geometry in the index to that circle using the given relation.

#### Ellipse

```shell
curl 
  -H "Content-Type: application/json" \
  -u "$USERNAME:$PASSWORD" \
  "http://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_ID/_geo/$INDEX_NAME\
  ?lat=0\
  &lon=0\
  &rangex=100\
  &rangey=50"\
  &relation="within"'
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");

account.request({
  db: $DATABASE,
  path: ['_design', $DESIGN_ID, '_geo', $GEO_INDEX].join('/'),
  params: {
    lat: 0,
    lon: 0,
    rangex: 100,
    rangey: 50,
    relation: '"within"'
  }
}, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Like [radius](#radius) queries, `ellipse` queries construct a circular geometry on the fly using the `lat`, `lon`, `rangex`, and `rangey` parameters.

Specifying `lat`, `lon`, `rangex` and `rangey` creates an ellipse centered at that latitude ('lat') and longitude ('lon') with a vertical radius of rangey and with a horizontal radius of rangex, and compares each geometry in the index to that circle using the given relation. Both `rangex` and `rangey` are measured in meters.
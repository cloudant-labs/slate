## Cloudant Geospatial

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the Cloudant Geospatial topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/cloudant-geo.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Cloudant Geospatial, or 'Cloudant Geo', combines the advanced geospatial queries of a Geographic Information System (GIS) with the flexibility and scalability of Cloudant's database-as-a-service (DBaaS) capabilities.

Cloudant Geo:

-   Enables web and mobile developers to enhance their applications using geospatial operations that go beyond simple bounding boxes.
-   Integrates with existing GIS applications, so that they can scale to accommodate different data sizes, concurrent users, and multiple locations.
-   Provides a NoSQL capability for GIS applications, so that large streams of data can be acquired from devices, sensors, and satellites. This data can then be stored, processed, and syndicated across other web applications.

### Cloudant Geo overview

Cloudant Geo lets you structure your data using GeoJSON format. Design documents are used to index the data. Just like working with other Cloudant documents, an initial scan works through all the documents in the database, giving you the first index. Subsequent updates to the documents result in incremental updates to the index.

The key advantage of Cloudant Geo is to enable you to identify, specify, or search for documents based on a spatial relationship; in effect using geometry to provide an additional way of expressing the relationship between and within documents.

<div></div>

> Example of relation using a geospatial polygon:

```
relation=contains&g=POLYGON ((-71.0537124 42.3681995,-71.054399 42.3675178,-71.0522962 42.3667409,-71.051631 42.3659324,-71.051631 42.3621431,-71.0502148 42.3618577,-71.0505152 42.3660275,-71.0511589 42.3670263,-71.0537124 42.3681995))
```

An example would be to specify that a document is considered to be 'contained' if it has a geospatial characteristic that fits within a given geospatial polygon, defined by a series of points.

The basic steps for working with geospatial data in Cloudant Geo is as follows:

1.  Include a GeoJSON geometry object in your JSON document. The geometry object can be of any type defined by the [GeoJSON specification](http://geojson.org/geojson-spec.html).
2.  Index the geometry object using Cloudant Geo defined `st_index` function.
3.  Search the indexed geometry object by using various geometries and geometric relationships.

### Using Cloudant Geospatial through the Dashboard

The Dashboard lets you perform several geospatial tasks:

*	Quick and easy visualisation of data stored in spatial indexes.
*	Spatial query construction.
*	Visualisation of spatial query results.

Before using the geospatial capability through the dashboard,
you must have some spatially indexed data within a database.

To access the geospatial area of the dashboard,
perform the following steps:

1.	Select the database containing spatially indexed data.
2.	Select the Design Documents menu.
3.	Select the Design Document that contains the definition of the spatial index. A 'Geospatial Indexes' sub menu appears for the spatial index.
4.	Select the Geospatial Index for your data. A map view appears, showing a small selection of the spatial features contained within the index.
5.	To see a JSON view of the index, click the corresponding button of the map view.

You can construct spatial queries using the drawing menu available on the map view.
To construct a spatial query:

1.	Open the drawing menu in the map view.
2.	Select the geometry type you require.
3.	Click in the map view to define the geospatial area.

Depending on the geometry type you specify,
a default spatial relation is chosen for you.
The exact relation is visible by selecting the Options menu.

The lowest area of the map view provides tools that let you select how many spatial features are displayed at once,
up to a maximum of 200 at a time.
To see the other results from your geospatial query,
page through them by clicking the left or right arrow buttons.

More information on using Cloudant Geospatial is available through the [Learning Center](http://www.cloudant.com/learning-center#geo).

### GeoJSON

[GeoJSON format](http://geojson.org/geojson-spec.html) is used to express a variety of geographic data structures, including:

-   `Point`
-   `LineString`
-   `Polygon`
-   `MultiPoint`
-   `MultiLineString`
-   `MultiPolygon`
-   `GeometryCollection`

A GeoJSON document is simply a JSON document containing two distinct key:value sections:

#### `type`

It must be present and contain the value `Feature`.

#### `geometry`

It must contain two fields: `type` and `coordinates`, where:

- `type` field specifies a GeoJSON geometry type which must be one of `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, or `MultiPolygon`.

- `coordinates` field specifies an array of latitude and longitude values.

<div></div>

> Example GeoJSON document:

```json
{
  "_id": "79f14b64c57461584b152123e38a6449",
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-71.13687953, 42.34690635]
  },
  "properties": {
    "compnos": "142035014",
    "domestic": false,
    "fromdate": 1412209800000,
    "main_crimecode": "MedAssist",
    "naturecode": "EDP",
    "reptdistrict": "D14",
    "shooting": false,
    "source": "boston"
  ..}
}
```

More information about GeoJSON, including the full specification, is available at <http://geojson.org/>.

### Creating a Cloudant Geo Index

To make it easier to work with Cloudant Geo documents, it is best practice to create a separate design document, specifically for Cloudant Geo.

When you create a geospatial index, you must use the Cloudant Geo defined keyword `st_indexes` to hold one or more Cloudant Geo index definitions, where each index must be defined by the Cloudant Geo `st_index` function.

#### `geoidx`: An example Cloudant Geo index
For example, you could create a design document with the `_id` value `"_design/geodd"` which contains an index called `"geoidx"`. The index is a simple JavaScript function that checks for the presence of a valid geometry object in the document, and if found ensures that the document is included in the `st_index` Cloudant Geo index function.

> Example Cloudant Geo design document, containing an index:


```json
{
  "_id": "_design/geodd",
  "st_indexes": {
    "geoidx": {
      "index": "function(doc) {if (doc.geometry && doc.geometry.coordinates) {st_index(doc.geometry);}}"
    }
  }
}
```


#### Geospatial indexing

There are a number of different algorithms for indexing geospatial data. Some algorithms are simple to understand and implement, but do not produce fast results.

The basic algorithm used by Cloudant Geo is [R\*\_tree](http://en.wikipedia.org/wiki/R*_tree). Although it has a slightly higher resource requirement for building the index, the resulting index offers much better performance in responding to geospatial queries.

### Obtaining information about a Cloudant geo index

> Example request to obtain information about the `geoidx` geospatial index, held within the `geodd` design document of the `crimes` database:

```http
GET /crimes/_design/geodd/_geo_info/geoidx HTTP/1.1
Host: $USERNAME.cloudant.com
```

```shell
curl https://$USERNAME.cloudant.com/crimes/_design/geodd/_geo_info/geoidx \
     -u $USERNAME
```

> Example JSON structure response:

```json
{
	"name": "_design/geodd/geoidx",
	"geo_index": {
		"doc_count": 269,
		"disk_size": 33416,
		"data_size": 26974
	}
}
```

You can obtain information about a geospatial index within a database.
Do this by using the `_geo_info` endpoint.

The data returned within the `geo_index` portion of the JSON response includes
the following fields:

Field | Description
------|------------
`doc_count` | Number of documents in the geospatial index.
`disk_size` | The size of the geospatial index, as stored on disk, in bytes.
`data_size` | The size of the geospatial index, in bytes.

### Querying a Cloudant Geo index

> The basic format for a Cloudant Geo API call:

```
/<database>/_design/<name>/_geo/<geoindexname>?<query-parameters>
```

The fundamental API call for utilizing Cloudant Geo has a simple format, where query parameters `<query-parameters>` include three different types of parameters: query geometry, geometric relation, and result set.

#### Query Geometry
> Example of an `ellipse` query:

```
?lat=-11.05987446&lon=12.28339928&rangex=200&rangey=100
```

> Example of a `radius` query:

```
?lat=-11.05987446&lon=12.28339928&radius=100
```

> Example of a `bbox` query:

```
?bbox=-11.05987446,12.28339928,-101.05987446,62.28339928
```

> Example of a `point` query:

```
?g=point(-71.0537124 42.3681995)
```

> Example of a `polygon` query:

```
?g=polygon((-71.0537124 42.3681995,-71.054399 42.3675178,-71.0522962 42.3667409,-71.051631 42.3659324,-71.051631 42.3621431,-71.0502148 42.3618577,-71.0505152 42.3660275,-71.0511589 42.3670263,-71.0537124 42.3681995))
```


A query geometry parameter must be provided for a Cloudant Geo search. There are four types of query geometries that are defined as follows:

<table>
<colgroup>
<col width="18%" />
<col width="81%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Parameter</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>

<tr class="odd">
<td align="left"><code>ellipse</code></td>
<td align="left">Specify an ellipse query with a latitude <code>lat</code>, a longitude <code>lon</code>, and two radii: <code>rangex</code> and <code>rangey</code> measured in meters.</td>
</tr>

<tr class="even">
<td align="left"><code>radius</code></td>
<td align="left">Specify a circle query with a latitude <code>lat</code>, a longitude <code>lon</code>, and a radius <code>radius</code> measured in meters.</td>
</tr>

<tr class="odd">
<td align="left"><code>bbox</code></td>
<td align="left">Specify a bounding box with two coordinates of lower-left and upper-right corners.</td>
</tr>

<tr class="even">
<td align="left"><code>g</code></td>
<td align="left">Specify a Well Known Text (WKT) object. The valid values for the <code>g</code> parameter include <code>Point | LineString | Polygon | MultiPoint | MultiLineString | MultiPolygon | GeometryCollection</code>.</td>
</tr>

</tbody>
</table>

Note that Cloudant Geo uses `intersects` as the default geometric relation when executing a query with query geometry only.


#### Geometric Relation

Cloudant Geo works with geospatial relationships and follows the [DE-9IM specification](https://en.wikipedia.org/wiki/DE-9IM) for geometric relations. These define the different ways in which two geospatial objects are related to each other, if indeed they are related at all. For example, you might specify a polygon object that describes a housing district. You could then query your document database for people residing within that district by requesting all documents where the place of residence is *contained* within the polygon object.

When you specify a query geometry, you can specify a geometric relationship against the query geometry when you query the documents in your database. Specifically, if Q is a query geometry, then a GeoJSON document, R, is regarded as the result when a geometric relation between Q and R returns true. The geometric relations are defined in the following table:

<table>
<colgroup>
<col width="16%" />
<col width="83%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Relation</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>

<tr class="odd">
<td align="left"><code>Q contains R</code></td>
<td align="left">True if no points of R lie in the exterior of Q.</td>

</tr>
<tr class="even">
<td align="left"><code>Q contains_properly R</code></td>
<td align="left">True if R intersects the interior of Q but not the boundary (or exterior) of Q.</td>
</tr>

<tr class="odd">
<td align="left"><code>Q covered_by R</code></td>
<td align="left">True if Q is entirely within R. <code>covered_by</code> returns the exact opposite result of <code>covers</code>.</td>
</tr>

<tr class="even">
<td align="left"><code>Q covers R</code></td>
<td align="left">True if R is entirely within Q. <code>covers</code> returns the exact opposite result of <code>covered_by</code>.</td>
</tr>

<tr class="odd">
<td align="left"><code>Q crosses R</code></td>
<td align="left">Case 1: True if the interiors intersect and at least the interior of Q intersects with the exterior of R. Apply to the geometry pairs of `multipoint/linestring`, `multipoint/multilinestring`, `multipoint/polygon`, `multipoint/multipolygon`, `linestring/polygon`, and `linestring/multipolygon`.</br>
<br>Case 2: True if the intersection of the interiors of Q and R is a point. Apply to the geometry pairs of `linestring/linestring`, `linestring/multilinestring`, and `multilinestring/multilinestring`.</br></td>
</tr>

<tr class="even">
<td align="left"><code>Q disjoint R</code></td>
<td align="left">True if the two geometries of Q and R do not intersect. <code>disjoint</code> returns the exact opposite result of <code>intersects</code>.</td>
</tr>

<tr class="odd">
<td align="left"><code>Q intersects R</code></td>
<td align="left">True if the two geometries of Q and R intersect. <code>intersects</code> returns the exact opposite result of <code>disjoint</code>.</td>
</tr>

<tr class="even">
<td align="left"><code>Q overlaps R</code></td>
<td align="left">Case 1: True if the interior of both geometries intersects the interior and exterior of the other. Apply to the geometry pairs of `polygon/polygon`, `multipoint/multipoint`, and `multipolygon/multipolygon`.</br>
<br>Case 2: True if the intersection of the geometries is a linestring. Apply to the geometry pairs of linestring/linestring and multilinestring/multilinestring. </br></td>
</tr>

<tr class="odd">
<td align="left"><code>Q touches R</code></td>
<td align="left">True if, and only if, the common points of two geometries are found only at the boundaries of two geometries. At least one geometry must be a linestring, polygon, multilinestring, or multipolygon.</td>
</tr>

<tr class="even">
<td align="left"><code>Q within R</code></td>
<td align="left">True if Q lies entirely within R. <code>within</code> returns the exact opposite result of <code>contains</code>.</td>
</tr>

</tbody>
</table>

> Example of returning all geometries which are contained by a `polygon`:

```
?relation=contains&g=polygon((-71.0537124 42.3681995,-71.054399 42.3675178,-71.0522962 42.3667409,-71.051631 42.3659324,-71.051631 42.3621431,-71.0502148 42.3618577,-71.0505152 42.3660275,-71.0511589 42.3670263,-71.0537124 42.3681995))
```

#### Nearest neighbor search

Cloudant Geo supports nearest neighbor search, known as NN search. If provided, the `nearest=true` search returns all results by sorting their distances to the center of the query geometry. This geometric relation `nearest=true` can be used either with all the geometric relations described earlier, or alone.

For example, one policeman might search five crimes that occurred near a specific location by issuing the query in the following example.

> Example query to find nearest five crimes against a given location:

```
https://education.cloudant.com/crimes/_design/geodd/_geo/geoidx
?g=POINT(-71.0537124 42.3681995)&nearest=true&limit=5
```

It is important to note that the `nearest=true` search can change the semantics of a Cloudant Geo search. For example, without `nearest=true` in the earlier example query, the results only include the GeoJSON documents whose coordinates equal the given query point `(-71.0537124 42.3681995)` or empty results set. However, by using the `nearest=true` search, the results include all GeoJSON documents in the database whose order is measured by the distance to the query point.


#### Result Set

You can use the following parameters to deal with the returned result set, such as returning results in GeoJSON format or limiting the number of returned results.

<table>
<colgroup>
<col width="18%" />
<col width="81%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Parameter</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>

<tr class="odd">
<td align="left"><code>bookmark</code></td>
<td align="left">Allows you to page through the results. The default is 25 results.</td>

<tr class="even">
<td align="left"><code>format</code></td>
<td align="left">Causes the query output to be in a specific format of <code>legacy | geojson | view | application/vnd.geo+json</code>. The default format is <code>view</code>.  
</td>
</tr>

<tr class="odd">
<td align="left"><code>include_docs</code></td>
<td align="left">Adds the entire document as a document object, and includes it in the output results.</td>
</tr>

<tr class="even">
<td align="left"><code>limit</code></td>
<td align="left">An integer to limit the number of results returned. The default value is 100. The maximum value is 200. A value larger than 200 will return an error.</td>
</tr>

<tr class="odd">
<td align="left"><code>skip</code></td>
<td align="left">Skip this number of records before starting to return the results. The default value is 0.</td>
</tr>

<tr class="odd">
<td align="left"><code>stale=ok</code></td>
<td align="left">Speeds up responses by not waiting to complete index re-building or updates between database cluster nodes.</td>
</tr>

</tbody>
</table>

##### Format Parameter Examples

> Example query to return results with `format=legacy`:

```
curl -X GET 'https://education.cloudant.com/crimes/_design/geodd/_geo/geoidx?format=legacy&lat=42.3397&lon=-71.07959&radius=10'
```

> Example response to the query:

```json
{
    "bookmark": "g2wAAAABaANkAB9kYmNvcmVAZGIzLmJpZ2JsdWUuY2xvdWRhbnQubmV0bAAAAAJuBAAAAADAbgQA_____2poAm0AAAAgNzlmMTRiNjRjNTc0NjE1ODRiMTUyMTIzZTM4YThlOGJGPv4LlS19_ztq",
    "features": [
        {
            "id": "79f14b64c57461584b152123e38a8e8b"
        }
    ],
    "type": "FeatureCollection"
}
```

> Example query to return results with `format=view`:

```
curl -X GET 'https://education.cloudant.com/crimes/_design/geodd/_geo/geoidx?format=view&lat=42.3397&lon=-71.07959&radius=10'
```

> Example response to the query:

```json
{
    "bookmark": "g2wAAAABaANkAB9kYmNvcmVAZGIxLmJpZ2JsdWUuY2xvdWRhbnQubmV0bAAAAAJuBAAAAADAbgQA_____2poAm0AAAAgNzlmMTRiNjRjNTc0NjE1ODRiMTUyMTIzZTM4YThlOGJGPv4LlS19_ztq",
    "rows": [
        {
            "geometry": {
                "coordinates": [
                    -71.07958956,
                    42.33967135
                ],
                "type": "Point"
            },
            "id": "79f14b64c57461584b152123e38a8e8b"
        }
    ]
}
```


> Example query to return results with `format=geojson` or `format=application/vnd.geo+json`:

```
curl -X GET 'https://education.cloudant.com/crimes/_design/geodd/_geo/geoidx?format=geojson&lat=42.3397&lon=-71.07959&radius=10'
```

> Example response to the query:

```json
{
    "bookmark": "g2wAAAABaANkAB9kYmNvcmVAZGIyLmJpZ2JsdWUuY2xvdWRhbnQubmV0bAAAAAJuBAAAAADAbgQA_____2poAm0AAAAgNzlmMTRiNjRjNTc0NjE1ODRiMTUyMTIzZTM4YThlOGJGPv4LlS19_ztq",
    "features": [
        {
            "_id": "79f14b64c57461584b152123e38a8e8b",
            "geometry": {
                "coordinates": [
                    -71.07958956,
                    42.33967135
                ],
                "type": "Point"
            },
            "properties": [],
            "type": "Feature"
        }
    ],
    "type": "FeatureCollection"
}
```
These examples show the available results based on the options you specify for the format parameter.

<div></div>

### Example: Querying a Cloudant Geo index

#### Simple Circle

> Example query to find documents that have a geospatial position within a circle:

```
curl -X GET 'https://education.cloudant.com/crimes/_design/geodd/_geo/geoidx?lat=42.3397&lon=-71.07959&radius=10&relation=contains&format=geojson'
```

> Example response to the query:

```json
{
    "bookmark": "g2wAAAABaANkAB9kYmNvcmVAZGIyLmJpZ2JsdWUuY2xvdWRhbnQubmV0bAAAAAJuBAAAAADAbgQA_____2poAm0AAAAgNzlmMTRiNjRjNTc0NjE1ODRiMTUyMTIzZTM4YThlOGJGPv4LlS19_ztq",
    "features": [
        {
            "_id": "79f14b64c57461584b152123e38a8e8b",
            "geometry": {
                "coordinates": [
                    -71.07958956,
                    42.33967135
                ],
                "type": "Point"
            },
            "properties": [],
            "type": "Feature"
        }
    ],
    "type": "FeatureCollection"
}
```

This example demonstrates how Cloudant Geo can find documents that are considered to have a geospatial position within a given geographic circle. This function might be useful to determine insurance customers who live close to a known flood plain.

To specify the circle, you provide:

-   Latitude
-   Longitude
-   Circle radius, specified in meters

This query compares the geometry of each document in the index with the geometry of the specified circle. The comparison is performed according to the relation you request in the query. So, to find all documents that fall within the circle, you use the `contains` relation.

<div></div>

#### A polygon query

A more complex example shows where you specify a polygon as the geometric object of interest. A polygon is simply any object defined by a series of connected points, where none of the connections (the lines between the points) cross any of the other connections.


> Example query to find documents that have a geospatial position within a polygon:

```
https://education.cloudant.com/crimes/_design/geodd/_geo/geoidx
?g=POLYGON((-71.0537124 42.3681995,-71.054399 42.3675178,-71.0522962 42.3667409,-71.051631 42.3659324,-71.051631 42.3621431,-71.0502148 42.3618577,-71.0505152 42.3660275,-71.0511589 42.3670263,-71.0537124 42.3681995))
&relation=contains
&format=geojson
```

> Example response to the query:

``` json
{
    "bookmark": "g2wAAAABaANkAB9kYmNvcmVAZGIzLmJpZ2JsdWUuY2xvdWRhbnQubmV0bAAAAAJuBAAAAADAbgQA_____2poAm0AAAAgNzlmMTRiNjRjNTc0NjE1ODRiMTUyMTIzZTM5MjQ1MTZGP1vW7X5qnWhq",
    "features": [
        {
            "_id": "79f14b64c57461584b152123e38d6349",
            "geometry": {
                "coordinates": [
                    -71.05107956,
                    42.36510634
                ],
                "type": "Point"
            },
            "properties": [],
            "type": "Feature"
        },
        {
            "_id": "79f14b64c57461584b152123e3924516",
            "geometry": {
                "coordinates": [
                    -71.05204477,
                    42.36674199
                ],
                "type": "Point"
            },
            "properties": [],
            "type": "Feature"
        }
    ],
    "type": "FeatureCollection"
}
```

In another example, we might provide a polygon description as the geometric object, and then request that the query return details of documents within the database that are contained by the polygon.

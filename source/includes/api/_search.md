## Search

> Example design document:

```json
{
  "_id": "_design/search_example",
  "indexes": {
    "animals": {
      "index": "function(doc){ ... }"
    }
  }
}
```

Search indexes, defined in design documents, allow databases to be queried using [Lucene Query Parser Syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview). Search indexes are defined by an index function, similar to a map function in MapReduce views. The index function decides what data to index and store in the index.

### Index functions

> Example search index function:

```
function(doc){
  index("default", doc._id);
  if (doc.min_length){
    index("min_length", doc.min_length, {"store": true});
  }
  if (doc.diet){
    index("diet", doc.diet, {"store": true});
  }
  if (doc.latin_name){
    index("latin_name", doc.latin_name, {"store": true});
  }
  if (doc.class){
    index("class", doc.class, {"store": true});
  }
}
```

<aside class="warning" role="complementary" aria-label="fieldmustexist">Attempting to index using a data field that does not exist will fail.
To avoid this problem, use an appropriate [guard clause](#index-guard-clauses).</aside>

The function contained in the index field is a Javascript function that is called for each document in the database. It takes the document as a parameter, extracts some data from it and then calls the `index` function to index that data.

The `index` function takes three parameters, where the third parameter is optional.
The first parameter is the name of the field used when querying the index,
specified in the Lucene syntax portion of the query.
For example,
when querying:

  `q=color:red`

"color" is the Lucene field name.

If the special value `"default"` is used,
the field name is not specified at query time.
The effect is that the query becomes:

  `q=red`

The second parameter is the data to be indexed.

The third, optional parameter is a JavaScript object with the following fields:

Option | Description | Values | Default
-------|-------------|--------|---------
`index` | Whether the data is indexed, and if so, how. If set to `false` or `no`, the data cannot be used for searches, but can still be retrieved from the index if `store` is set to `true`. See [Analyzers](#analyzers) for more information. | `analyzed`, `analyzed_no_norms`, `false`, `no`, `not_analyzed`, `not_analyzed_no_norms` | `analyzed`
`facet` | Creates a faceted index. See [Faceting](search.html#faceting) for more information. | `true`, `false` | `false`
`store` | If `true`, the value is returned in the search result; otherwise, the value is not returned. | `true`, `false` | `false`
`boost` | A number specifying the relevance in search results. Content indexed with a boost value greater than 1 is more relevant than content indexed without a boost value. Content with a boost value less than one is not so relevant. | A positive floating point number | 1 (no boosting)

#### Index Guard Clauses

> Example of failing to check if the index data field exists:

```
if (doc.min_length) {
  index("min_length", doc.min_length, {"store": true});
}
```

The `index` function requires the name of the data field to index as the second parameter.
However,
if that data field does not exist for the document,
an error occurs.
The solution is to use an appropriate 'guard clause' that checks if the field exists,
and contains the expected type of data,
_before_ attempting to create the corresponding index.

<div></div>

> Using a guard clause to check if the required data field exists, and holds a number, _before_ attempting to index:

```
if (typeof(doc.min_length) === 'number') {
  index("min_length", doc.min_length, {"store": true});
}
```

You might use the javascript `typeof` function to perform the guard clause test.
If the field exists _and_ has the expected type,
the correct type name is returned,
so the guard clause test succeeds and it is safe to use the index function.
If the field does not exist,
you would not get back the expected type of the field,
therefore you would not attempt to index the field.

Whatever guard clause test you decide to use,
remember that Javascript considers a result to be false if one of the following values is tested:

-	'undefined'
-	null
-	The number +0
-	The number -0
-	NaN (not a number)
-	"" (the empty string)

<div></div>

> A 'generic' guard clause:

```
if (typeof(doc.min_length) !== 'undefined') {
  // The field exists, and does have a type, so we can proceed to index using it.
  ...
}
```

Therefore,
a possible generic guard clause simply tests to ensure that the type of the candidate data field is defined.

### Analyzers

> Example analyzer document:

```json
{
  "_id": "_design/analyzer_example",
  "indexes": {
    "INDEX_NAME": {
      "index": "function (doc) { ... }",
      "analyzer": "$ANALYZER_NAME"
    }
  }
}
```

Analyzers are settings which define how to recognize terms within text. This can be helpful if you need to [index multiple languages](search.html#language-specific-analyzers).

Here's the list of generic analyzers supported by Cloudant search:

Analyzer | Description
---------|------------
`classic` | The standard Lucene analyzer, circa release 3.1. You'll know if you need it.
`email` | Like the `standard` analyzer, but tries harder to match an email address as a complete token.
`keyword` | Input is not tokenized at all.
`simple` | Divides text at non-letters.
`standard` | The default analyzer. It implements the Word Break rules from the [Unicode Text Segmentation algorithm](http://www.unicode.org/reports/tr29/).
`whitespace` | Divides text at whitespace boundaries.

<div></div>
#### Language-Specific Analyzers

These analyzers will omit very common words in the specific language, and many also [remove prefixes and suffixes](http://en.wikipedia.org/wiki/Stemming). The name of the language is also the name of the analyzer.

* arabic
* armenian
* basque
* bulgarian
* brazilian
* catalan
* cjk (Chinese, Japanese, Korean)
* chinese ([smartcn](http://lucene.apache.org/core/4_2_1/analyzers-smartcn/org/apache/lucene/analysis/cn/smart/SmartChineseAnalyzer.html))
* czech
* danish
* dutch
* english
* finnish
* french
* german
* greek
* galician
* hindi
* hungarian
* indonesian
* irish
* italian
* japanese ([kuromoji](http://lucene.apache.org/core/4_2_1/analyzers-kuromoji/overview-summary.html))
* latvian
* norwegian
* persian
* polish ([stempel](http://lucene.apache.org/core/4_2_1/analyzers-stempel/overview-summary.html))
* portuguese
* romanian
* russian
* spanish
* swedish
* thai
* turkish

<aside class="information" role="complementary" aria-label="optimization">Language-specific analyzers are optimized for the specified language.
You cannot combine a generic analyzer with a language-specific analyzer.
However,
you could use the [`perfield` analyzer](#per-field-analyzers) to select different analyzers for different fields within the documents.</aside>

<div></div>
#### Per-Field Analyzers

> Example of defining different analyzers for different fields:

```json
{
  "_id": "_design/analyzer_example",
  "indexes": {
    "INDEX_NAME": {
      "analyzer": {
        "name": "perfield",
        "default": "english",
        "fields": {
          "spanish": "spanish",
          "german": "german"
        }
      },
      "index": "function (doc) { ... }"
    }
  }
}
```

The `perfield` analyzer configures multiple analyzers for different fields.

<div></div>
#### Stop Words

> Example of defining non-indexed ('stop') words:

```json
{
  "_id": "_design/stop_words_example",
  "indexes": {
    "INDEX_NAME": {
      "analyzer": {
        "name": "portuguese",
        "stopwords": [
          "foo",
          "bar",
          "baz"
        ]
      },
      "index": "function (doc) { ... }"
    }
  }
}
```

Stop words are words that do not get indexed. You define them within a design document by turning the analyzer string into an object.

<aside class="warning" role="complementary" aria-label="stopwords">The `keyword`, `simple` and `whitespace` analyzers do not support stop words.</aside>

<div></div>
#### Testing analyzer tokenization

> [Example test of the `keyword` analyzer](try.html#requestType=analyzers&predefinedQuery=keyword)

```shell
curl 'https://$ACCOUNT.cloudant.com/_search_analyze' -H 'Content-Type: application/json'
  -d '{"analyzer":"keyword", "text":"ablanks@renovations.com"}'
```

```http
Host: <account>.cloudant.com
POST /_search_analyze HTTP/1.1
Content-Type: application/json
{"analyzer":"keyword", "text":"ablanks@renovations.com"}
```

> Result of testing the `keyword` analyzer

```json
{
  "tokens": [
    "ablanks@renovations.com"
  ]
}
```

> [Example test of the `standard` analyzer](try.html#requestType=analyzers&predefinedQuery=standard)

```shell
curl 'https://$ACCOUNT.cloudant.com/_search_analyze' -H 'Content-Type: application/json'
  -d '{"analyzer":"standard", "text":"ablanks@renovations.com"}'
```

```http
Host: <account>.cloudant.com
POST /_search_analyze HTTP/1.1
Content-Type: application/json
{"analyzer":"standard", "text":"ablanks@renovations.com"}
```

> Result of testing the `standard` analyzer

```json
{
  "tokens": [
    "ablanks",
    "renovations.com"
  ]
}
```

You can test the results of analyzer tokenization by posting sample data to the `_search_analyze` endpoint or using our [analyzer test form](try.html#requestType=analyzers).

### Queries

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGN_ID/_search/$INDEX_NAME?q=$QUERY \
```

```javascript
var nano = require('nano');
var account = nano("https://"+$ACCOUNT+".cloudant.com");
var db = account.use($DATABASE);

db.search($DESIGN_ID, $SEARCH_INDEX, {
  q: $QUERY
}, function (err, body, headers) {
  if (!err) {
    console.log(body);
  }
});
```

Once you've got an index written, you can query it with a `GET` request to `https://<account>.cloudant.com/$DATABASE/_design/<deign_id>/_search/<index_name>`. Specify your search query in the `query` query parameter.

#### Query Parameters

<aside class="warning" role="complementary" aria-label="enablebeforeuse">You must enable [faceting](search.html#faceting) before you can use the following parameters:
<ul>
<li> `counts`
<li> `drilldown`
</ul>
</aside>

<!-- The numeric `limit` was suggested by Glynn, in FB 40734. -->

Argument | Description | Optional | Type | Supported Values
---------|-------------|----------|------|------------------
`bookmark` | A bookmark that was received from a previous search. This allows you to page through the results. If there are no more results after the bookmark, you get a response with an empty rows array and the same bookmark. That way you can determine that you have reached the end of the result list. | yes | string |
`counts` | This field defines an array of names of string fields, for which counts should be produced. The response contains counts for each unique value of this field name among the documents matching the search query. [Faceting](search.html#faceting) must be enabled for this parameter to function. | yes | JSON | A JSON array of field names
`drilldown` | This field can be used several times. Each use defines a pair of a field name and a value. The search only matches documents that have the given value in the field name. It differs from using `"fieldname:value"` in the `q` parameter only in that the values are not analyzed. [Faceting](search.html#faceting) must be enabled for this parameter to function. | yes | JSON | A JSON array with two elements, the field name and the value.
`group_field` | Field by which to group search matches. | yes | String | A string containing the name of a string field. Fields containing other data (numbers, objects, arrays) can not be used.
`group_limit` | Maximum group count. This field can only be used if `group_field` is specified. | yes | Numeric |
`group_sort` | This field defines the order of the groups in a search using `group_field`. The default sort order is relevance. | yes | JSON | This field can have the same values as the sort field, so single fields as well as arrays of fields are supported.
`highlight_fields` | Specifies which fields should be highlighted. If specified, the result object contains a `highlights` field with an entry for each specified field. | yes | Array of strings |
`highlight_pre_tag` | A string inserted before the highlighted word in the highlights output | yes, defaults to `<em>` | String |
`highlight_post_tag` | A string inserted after the highlighted word in the highlights output | yes, defaults to `</em>` | String |
`highlight_number` | Number of fragments returned in highlights. If the search term occurs less often than the number of fragments specified, longer fragments are returned. | yes, defaults to 1 | Numeric |
`highlight_size` | Number of characters in each fragment for highlights. | yes, defaults to 100 characters | Numeric |
`include_docs` | Include the full content of the documents in the response | yes | boolean |
`include_fields` | A JSON array of field names to include in search results. Any fields included must have been indexed with the `store:true` option. | yes, the default is all fields | Array of strings |
`limit` | Limit the number of the returned documents to the specified number. In case of a grouped search, this parameter limits the number of documents per group. | yes | numeric | The limit value can be any positive integer number up to and including 200.
`query` | A Lucene query | no | string or number |
`ranges` | This field defines ranges for faceted, numeric search fields. The value is a JSON object where the fields names are numeric, faceted search fields and the values of the fields are again JSON objects. Their field names are names for ranges. The values are Strings describing the range, for example `"[0 TO 10]"` | yes | JSON | The value must be on object whose fields again have objects as their values. These objects must have string describing ranges as their field values.
`sort` | Specifies the sort order of the results. In a grouped search (when `group_field` is used), this parameter specifies the sort order within a group. The default sort order is relevance. | yes | JSON | A JSON string of the form `"fieldname<type>"` or `-fieldname<type>` for descending order, where `fieldname` is the name of a string or number field, and `type` is either number or string or a JSON array of such strings. The type part is optional and defaults to number. Some examples are `"foo"`, `"-foo"`, `"bar<string>"`, `"-foo<number>"` and `["-foo<number>", "bar<string>"]`. String fields used for sorting must not be analyzed fields. Fields used for sorting must be indexed by the same indexer used for the search query.
`stale` | Don't wait for the index to finish building to return results. | yes | string | ok

<aside class="warning" role="complementary" aria-label="donotcombine">Do not combine the `bookmark` and `stale` options. The reason is that both these options constrain the choice of shard replicas to use for determining the response. When used together, the options can result in problems when attempting to contact slow or unavailable replicas.</aside>

<aside class="warning" role="complementary" aria-label="performanceimplications">Note that using `include_docs=true` might have [performance implications](creating_views.html#include_docs_caveat).</aside>

#### POSTing search queries

> Search request using the POST API

```http
POST /db/_design/ddoc/_search/searchname HTTP/1.1
Content-Type: application/json
Host: <account>.cloudant.com
```

```shell
curl 'https://$ACCOUNT.cloudant.com/db/_design/ddoc/_search/searchname' -X POST -H 'Content-Type: application/json' -d @search.json
```

```json
{
  "q": "index:my query",
  "sort": "foo",
  "limit": 3
}
```

Instead of using the `GET` HTTP method, you can also use `POST`. The main advantage of `POST` queries is, that they can have a request body, so you can specify the request as a JSON object. Each parameter in the previous table corresponds to a field in the JSON object in the request body.

<div> </div>

### Query Syntax

> Example search query:

```
// Birds
class:bird
// Animals that begin with the letter "l"
l*
// Carnivorous birds
class:bird AND diet:carnivore
// Herbivores that start with letter
"l" l* AND diet:herbivore
// Medium-sized herbivores
min_length:[1 TO 3] AND diet:herbivore
// Herbivores that are 2m long or less
diet:herbivore AND min_length:[-Infinity TO 2]
// Mammals that are at least 1.5m long
class:mammal AND min_length:[1.5 TO Infinity]
// Find "Meles meles"
latin_name:"Meles meles"
// Mammals who are herbivore or carnivore
diet:(herbivore OR omnivore) AND class:mammal
// Return all results
*:*
```

The Cloudant search query syntax is based on the [Lucene syntax](http://lucene.apache.org/core/4_3_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#Overview). Search queries take the form of name:value (unless the name is omitted, in which case they hit the default field, demonstrated in the example provided).

Queries over multiple fields can be logically combined, and groups and fields can be further grouped. The available logical operators are case sensitive and are `AND`, `+`, `OR`, `NOT` and `-`. Range queries can run over strings or numbers.

If you want a fuzzy search you can run a query with `~` to find terms like the search term. For instance, `look~` will find terms book and took.

You can alter the importance of a search term by adding `^` + a positive number. This makes matches containing the term more or less relevant to the power of the boost value, with 1 as the default. Any decimal between 0 and 1 will reduce importance while anything over 1 will increase it.

Wild card searches are supported, for both single (`?`) and multiple (`*`) character searches. `dat?` would match date and data, `dat*` would match date, data, database, and dates.
Wildcards must come after the search term.
Use `*:*` to return all results.

Result sets from searches are limited to 200 rows, and return 25 rows by default. The number of rows returned can be changed via the limit parameter.
If the search query does *not* specify the `"group_field"` argument,
the response contains a bookmark. If the bookmark is passed back as a URL parameter you'll skip through the rows you've already seen and get the next set of results.

<aside class="warning" role="complementary" aria-label="omitsbookmark">The response never includes a bookmark if the `"group_field"` argument is specified in the search query.</aside>

The following characters require escaping if you want to search on them: `+ - && || ! ( ) { } [ ] ^ " ~ * ? : \ /`

Escape these with a preceding backslash character.

The response to a search query contains an order field for each of the results.
The order field is an array where the first element is the field or fields specified in the sort parameter.
If no sort parameter is included in the query, then the order field contains the lucene relevance score.
If using the 'sort by distance' feature as described in [Geographical Searches](search.html#geographical-searches),
then the first element is the distance from a point,
measured using either kilometers or miles.

<aside class="warning" role="complementary" aria-label="ignoresecond">The second element in the order array can be ignored.
It is used for troubleshooting purposes only.</aside>

### Faceting

> Example search query, specifying that faceted search is enabled:

```
function(doc) {
  index("type", doc.type, {"facet": true});
  index("price", doc.price, {"facet": true});
}
```

> Example of `ranges` faceted search:

```
?q=*:*&ranges={"price":{"cheap":"[0 TO 100]","expensive":"{100 TO Infinity}"}}
```

> Example results for faceted search `ranges` example:

```json
{
  "total_rows":100000,
  "bookmark":"g...",
  "rows":[...],
  "ranges": {
    "price": {
      "expensive": 278682,
      "cheap": 257023
    }
  }
}
```

Cloudant Search also supports faceted searching,
which allows you to discover aggregate information about all your matches quickly and easily.
You can match all documents using the special `?q=*:*` query syntax,
and use the returned facets to refine your query.
To indicate a field should be indexed for faceted queries,
set `{"facet": true}` in its options.

<div></div>
> Example `if` statement:

```
if (typeof doc.town == "string" && typeof doc.name == "string") {
  index("town", doc.town, {facet: true});
  index("town", doc.town, {facet: true});
    }
```


<aside class="warning" role="complementary" aria-label="enablefacets">In order to use facets, all the documents in the index must include all the fields that have faceting enabled. If your documents do not include all the fields, you will receive a `bad_request` error with the following reason, "dim `field_name` does not exist."

If each document does not contain all the fields for facets, it is recommended that you create separate indexes for each field. If you do not create separate indexes for each field, you must include only documents that contain all the fields. Verify that the fields exist in each document using a single `if` statement.

</aside>




<div></div>


#### Counts

> Example query

```
?q=*:*&counts=["type"]
```

> Example response

```json
{
  "total_rows":100000,
  "bookmark":"g...",
  "rows":[...],
  "counts":{
    "type":{
      "sofa": 10,
      "chair": 100,
      "lamp": 97
    }
  }
}
```

The count facet syntax takes a list of fields,
and returns the number of query results for each unique value of each named field.

<aside class="warning" role="complementary" aria-label="stringsonly">The count operation works only if the indexed values are strings.
The indexed values cannot be mixed types.
For example,
if 100 strings are indexed,
and one number,
then the index cannot be used for count operations.
You can check the type using the `typeof` operator,
and convert using `parseInt`, `parseFloat` and `.toString()` functions.
</aside>

<div></div>

#### Drilldown

Add `drilldown=["dimension","label"]` to a search query and restrict results to documents with dimension equal to the given label. You can include multiple drilldown parameters to restrict results along multiple dimensions.

Using a drilldown parameter is similar to using `key:value` in the `q` parameter, but the drilldown parameter returns values that the search's analyzer might skip. For example, if the analyzer did not index a stop word like "a", drilldown will return it by `drilldown=["key","a"]`.

<div></div>

#### Ranges

> Example query

```
?q=*:*&ranges={"price":{"cheap":"[0 TO 100]","expensive":"{100 TO Infinity}"}}
```

> Example response

```json
{
  "total_rows":100000,
  "bookmark":"g...",
  "rows":[...],
  "ranges": {
    "price": {
      "expensive": 278682,
      "cheap": 257023
    }
  }
}
```

The range facet syntax reuses the standard Lucene syntax for ranges to return counts of results which fit into each specified category.
Inclusive range queries are denoted by brackets (`[`, `]`).
Exclusive range queries are denoted by curly brackets (`{`, `}`).

<aside class="warning" role="complementary" aria-label="numbersonly">The range operation works only if the indexed values are numbers.
The indexed values cannot be mixed types.
For example,
if 100 strings are indexed,
and one number,
then the index cannot be used for range operations.
You can check the type using the `typeof` operator,
and convert using `parseInt`, `parseFloat` and `.toString()` functions.
</aside>

### Geographical searches

> Some example data...

```json
{
    "name":"Aberdeen, Scotland",
    "lat":57.15,
    "lon":-2.15,
    "type":"city"
}
```

> ... as well as a design document with a search index for them.

```
function(doc) {
    if (doc.type && doc.type == 'city') {
        index('city', doc.name, {'store': true});
        index('lat', doc.lat, {'store': true});
        index('lon', doc.lon, {'store': true});
    }
}
```

> An example query that sorts cities in the northern hemisphere by their distance to New York:

```shell
curl 'https://docs.cloudant.com/examples/_design/cities-designdoc/_search/cities?q=lat:[0+TO+90]&sort="<distance,lon,lat,-74.0059,40.7127,km>"'
```

```http
GET /examples/_design/cities-designdoc/_search/cities?q=lat:[0+TO+90]&sort="<distance,lon,lat,-74.0059,40.7127,km>" HTTP/1.1
Host: docs.cloudant.com
```

> Example response

```json
{
    "total_rows": 205,
    "bookmark": "g1AAAAEbeJzLYWBgYMlgTmGQS0lKzi9KdUhJMtfLTczJLyrRS87JL01JzCvRy0styQGqY0pkSLL___9_Fpjj5tDCOG974NGNieJZqAaY4DQgyQFIJtUjmyHXJivfY5PIgmaGKU4z8liAJEMDkAIasx9mTnPNv-PSgosTmbOI9QzEnAMQc-DuqY3U-vbZXTSRNSsLAMMnXIU",
    "rows": [
        {
            "id": "city180",
            "order": [
                8.530665755719783,
                18
            ],
            "fields": {
                "city": "New York, N.Y.",
                "lat": 40.78333333333333,
                "lon": -73.96666666666667
            }
        },
        {
            "id": "city177",
            "order": [
                13.756343205985946,
                17
            ],
            "fields": {
                "city": "Newark, N.J.",
                "lat": 40.733333333333334,
                "lon": -74.16666666666667
            }
        },
        {
            "id": "city178",
            "order": [
                113.53603438866077,
                26
            ],
            "fields": {
                "city": "New Haven, Conn.",
                "lat": 41.31666666666667,
                "lon": -72.91666666666667
            }
        }
    ]
}
```

In addition to searching by the content of textual fields,
you can also sort your results by their distance from a geographic coordinate.

You will need to index two numeric fields (representing the longitude and latitude).


You can then query using the special <distance...> sort field which takes 5 parameters:

- longitude field name: The name of your longitude field (“mylon” in this example)
- latitude field name: The name of your latitude field (“mylat” in this example)
- longitude of origin: The longitude of the place you want to sort by distance from
- latitude of origin: The latitude of the place you want to sort by distance from units
- The units to use (“km” or “mi” for kilometers and miles, respectively). The distance itself is returned in the order field


You can combine sorting by distance with any other search query, such as range searches on the latitude and longitude or queries involving non-geographical information. That way, you can search in a bounding box and narrow down the search with additional criteria.

### Highlighting Search Terms

> Search query with highlighting enabled

```http
GET /movies/_design/searches/_search/movies?q=movie_name:Azazel&highlight_fields=["movie_name"]&highlight_pre_tag="<b>"&highlight_post_tag="</b>"&highlights_size=30&highlights_number=2 HTTP/1.1
HOST: <account>.cloudant.com
Authorization: ...
```

```shell
curl "https://$ACCOUNT.cloudant.com/movies/_design/searches/_search/movies?q=movie_name:Azazel&highlight_fields=\[\"movie_name\"\]&highlight_pre_tag=\"<b>\"&highlight_post_tag=\"</b>\"&highlights_size=30&highlights_number=2
```

> Search result with highlights

```json
{
  "highlights": {
    "movie_name": [
      " on the <b>Azazel</b> Orient Express",
      " <b>Azazel</b> manuals, you"
    ]
  }
}
```

Sometimes it is useful to get the context in which a search term was mentioned so that you can display more detailed results to a user. To do this, you add the `search_highlights` parameter to the search query, specifying the field names for which you would like excerpts with the highlighted search term to be returned. By default, the search term is placed in `<em>` tags to highlight it, but this can be overridden using the `highlights_pre_tag` and `highlights_post_tag` parameters. The length of the fragments is 100 characters by default. A different length can be requested with the `hightlights_size` parameter. The `highlights_number` parameter controls the number of fragments returned, which defaults to 1.

In the response, a `highlights` field will be added with one subfield per field name. For each field, you will receive an array of fragments with the search term highlighted.

<aside class="notice" role="complementary" aria-label="storefieldinindex">For highlighting to work, you need to have the field stored in the index by using the `store: true` option.</aside>

### Search index metadata

> Example request

```http
GET /$DATABASE/_design/$DESIGN_DOC/_search_info/$INDEX HTTP/1.1
```

```shell
curl "https://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_DOCUMENT/_search_info/$INDEX" \
     -X GET -u "$ACCOUNT:$PASSWORD"
```

To retrieve information about a search index, you can send a `GET` request to the `_search_info`
endpoint as shown in the example. `DDOC` refers to the design document that contains the index and
`INDEX` is the name of the index.

> Example response

```json
{
  "name": "_design/DDOC/INDEX",
  "search_index": {
    "pending_seq": 7125496,
    "doc_del_count": 129180,
    "doc_count": 1066173,
    "disk_size": 728305827,
    "committed_seq": 7125496
  }
}
```

The response contains information about your index such as the number of document in the index and
its size on disk.

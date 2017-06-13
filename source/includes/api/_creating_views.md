<div id="creating-views"></div>
<div id="working-with-views"></div>

## Views (MapReduce)

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the Views (MapReduce) topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/creating_views.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

Views are used to obtain data stored within a database.
Views are written using Javascript functions.

### View concepts

Views are mechanisms for working with document content in databases.
A view can selectively filter documents.
It can speed up searching for content.
It can be used to 'pre-process' the results before they are returned to the client.

Views are simply Javascript functions,
defined within the `view` field of a design document.
When you use a view,
or more accurately when you perform a query using your view,
the system applies the Javascript function to each and every document in the database.
Views can be complex.
You might choose to define a collection of Javascript functions to create the overall view required.

### A simple view

> Example of a simple view, using a map function:

```
function(employee) {
  if(employee.training) {
    emit(employee.number, employee.training);
  }
}
```

> Simplified example data:

```json
[
    {
        "_id":"23598567",
        "number":"23598567",
        "training":"2014/05/21 10:00:00"
    },
    {
        "_id":"10278947",
        "number":"10278947"
    },
    {
        "_id":"23598567",
        "number":"23598567",
        "training":"2014/07/30 12:00:00"
    }
]
```

> Example response from running the view query

```json
{
	"total_rows": 2,
	"offset": 0,
	"rows": [
		{
			"id":"23598567",
			"number":"23598567",
			"training":"2014/05/21 10:00:00"
		},
		{
			"id":"23598567",
			"number":"23598567",
			"training":"2014/07/30 12:00:00"
		}
	]
}
```

The simplest form of view is a map function.
The map function produces output data that represents an analysis (a mapping) of the documents stored within the database.

For example,
you might want to find out which employees have had some safety training,
and the date when that training was completed.
You could do this by inspecting each document,
looking for a field in the document called "training".
If the field is present,
the employee completed the training on the date recorded as the value.
If the field is not present,
the employee has not completed the training.

Using the `emit` function in the example view function makes it easy to produce a list in response to running a query using the view.
The list consists of key and value pairs,
where the key helps you identify the specific document and the value provides just the precise detail you want.
The list also includes metadata such as the number of key:value pairs returned.

<aside class="notice" role="complementary" aria-label="autoincludeid">The document `_id` is automatically included in each of the key:value pair result records.
This is to make it easier for the client to work with the results.</aside>

### Map function examples

#### Indexing a field

> Example of indexing a field:

```
function(doc) {
  if (doc.foo) {
    emit(doc._id, doc.foo);
  }
}
```

This map function checks whether the object has a `foo` field and emits the value of this field. This allows you to query against the value of the foo field.

#### An index for a one to many relationship

> Example of indexing a one to many relationship:

```
function(doc) {
  if (doc.friends) {
    for (friend in friends) {
      emit(doc._id, { "_id": friend });
    }
  }
}
```

If the object passed to `emit` has an `_id` field,
a view query with `include_docs` set to `true` contains the document with the given ID.

#### Complex Keys

Keys are not limited to simple values. You can use arbitrary JSON values to influence sorting.

When the key is an array, view results can be grouped by a sub-section of the key. For example, if keys have the form [year, month, day] then results can be reduced to a single value or by year, month, or day. See [Using Views](creating_views.html#using-views) for more information.

### Reduce functions

> Example of a reduce function:

```
function (keys, values, rereduce) {
  return sum(values);
}
```

If a view has a reduce function, it is used to produce aggregate results for that view. A reduce function is passed a set of intermediate values and combines them to a single value. Reduce functions must accept, as input, results emitted by its corresponding map function '''as well as results returned by the reduce function itself'''. The latter case is referred to as a ''rereduce''.

Reduce functions are passed three arguments in the order ''keys'', ''values'', and ''rereduce''.

Reduce functions must handle two cases:

1.	When `rereduce` is false:
  -	`keys` will be an array whose elements are arrays of the form `[key,id]`, where `key` is a key emitted by the map function and ''id'' is that of the document from which the key was generated.
  -	`values` will be an array of the values emitted for the respective elements in `keys`, for example: `reduce([ [key1,id1], [key2,id2], [key3,id3] ], [value1,value2,value3], false)`

2.	When `rereduce` is true:
  -	`keys` will be `null`.
  -	`values` will be an array of values returned by previous calls to the reduce function, for example: `reduce(null, [intermediate1,intermediate2,intermediate3], true)`\`

Reduce functions should return a single value, suitable for both the "value" field of the final view and as a member of the "values" array passed to the reduce function.

Often, reduce functions can be written to handle rereduce calls without any extra code, like the summation function described previously. In that case, the `rereduce` argument can be ignored.

#### Built-in reduce functions

For performance reasons, a few simple reduce functions are built in. Whenever possible, you should use one of these functions instead of writing your own. To use one of the built-in functions, put its name into the `reduce` field of the view object in your design document.

<table>
<colgroup>
<col width="11%" />
<col width="88%" />
</colgroup>
<thead>
<tr class="header">
<th align="left">Function</th>
<th align="left">Description</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="left"><code>_sum</code></td>
<td align="left">Produces the sum of all values for a key, values must be numeric</td>
</tr>
<tr class="even">
<td align="left"><code>_count</code></td>
<td align="left">Produces the row count for a given key, values can be any valid json</td>
</tr>
<tr class="odd">
<td align="left"><code>_stats</code></td>
<td align="left">Produces a json structure containing sum, count, min, max and sum squared, values must be numeric</td>
</tr>
</tbody>
</table>

By feeding the results of `reduce` functions back into the `reduce` function, MapReduce is able to split up the analysis of huge datasets into discrete, parallelized tasks, which can be completed much faster.

### Storing the view definition

> Example for `PUT`ting a view into a design document (`training`):

```http
PUT /$DATABASE/_design/training HTTP/1.1
Content-Type: application/json
```

```shell
curl -X PUT https://$ACCOUNT.cloudant.com/$DATABASE/_design/training --data-binary @view.def
# where the design document is stored in the file `view.def`
```

> Example format for the view:

```json
{
  "views" : {
    "hadtraining" : {
      "map" : "function(employee) { if(employee.training) { emit(employee.number, employee.training); } }"
    }
  }
}
```

Each view is a Javascript function.
Views are stored in design documents.
So,
to store a view,
we simply store the function definition within a design document. A design document can be [created or updated just like any other document](document.html#update).

Do this by `PUT`ting the view definition content into a `_design` document.
In this example,
the `hadtraining` view is defined as a map function,
and is available within the `views` field of the design document.

### Using Views

Views enable you to search for content within a database,
that matches specific criteria.
The criteria are specified within the view definition,
or supplied as arguments when you use the view.

-   **Method**: `GET /db/_design/<design-doc>/_view/<view-name>`
-   **Request**: None
-   **Response**: JSON of the documents returned by the view
-   **Roles permitted**: \_reader

Executes the specified `view-name` from the specified `design-doc` design document.

#### Query Arguments

> Example of retrieving a list of the first five documents from a database, applying the user-created `by_title` view:

```http
GET /$DATABASE/_design/<design-doc>/_view/by_title?limit=5 HTTP/1.1
Accept: application/json
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGNDOCUMENT/_view/by_title?limit=5 \
     -H "Content-Type: application/json"
```

> Example response:

```json
{
   "offset" : 0,
   "rows" : [
      {
         "id" : "3-tiersalmonspinachandavocadoterrine",
         "key" : "3-tier salmon, spinach and avocado terrine",
         "value" : [
            null,
            "3-tier salmon, spinach and avocado terrine"
         ]
      },
      {
         "id" : "Aberffrawcake",
         "key" : "Aberffraw cake",
         "value" : [
            null,
            "Aberffraw cake"
         ]
      },
      {
         "id" : "Adukiandorangecasserole-microwave",
         "key" : "Aduki and orange casserole - microwave",
         "value" : [
            null,
            "Aduki and orange casserole - microwave"
         ]
      },
      {
         "id" : "Aioli-garlicmayonnaise",
         "key" : "Aioli - garlic mayonnaise",
         "value" : [
            null,
            "Aioli - garlic mayonnaise"
         ]
      },
      {
         "id" : "Alabamapeanutchicken",
         "key" : "Alabama peanut chicken",
         "value" : [
            null,
            "Alabama peanut chicken"
         ]
      }
   ],
   "total_rows" : 2667
}
```

Argument | Description | Optional | Type | Default | Supported values
---------|-------------|----------|------|---------|-----------------
`descending` | Return the documents in 'descending by key' order. | yes | Boolean | false |
`endkey` | Stop returning records when the specified key is reached. | yes | String or JSON array | |
`endkey_docid` | Stop returning records when the specified document ID is reached. | yes | String | |
`group` | Using the reduce function, group the results to a group or single row. | yes | Boolean | false |
`group_level` | Only applicable if the view uses complex keys: keys that are JSON arrays. Groups reduce results for the specified number of array fields. | yes | Numeric | |
`include_docs` | Include the full content of the documents in the response. | yes | Boolean | false |
`inclusive_end` | Include rows with the specified endkey. | yes | Boolean | true |
`key` | Return only documents that match the specified key. Note: Keys are JSON values, and must be URL encoded. | yes | JSON strings or arrays | |
`keys` | Return only documents that match the specified keys. Note: Keys are JSON values and must be URL encoded. | yes | Array of JSON strings or arrays | |
`limit` | Limit the number of returned documents to the specified count. | yes | Numeric | |
`reduce` | Use the reduce function. | yes | Boolean | true |
`skip` | Skip this number of rows from the start. | yes | Numeric | 0 |
`stable` | Prefer view results from a 'stable' set of shards. This means that the results are from a view that is less likely to be updated soon. | yes | Boolean | false | 
`stale` | Allow the results from a stale view to be used. This makes the request return immediately, even if the view has not been completely built yet. If this parameter is not given, a response is returned only after the view has been built. | yes | String | false | `ok`: Allow stale views.<br/>`update_after`: Allow stale views, but update them immediately after the request.
`startkey` | Return records starting with the specified key. | yes | String or JSON array | |
`startkey_docid` | Return records starting with the specified document ID. | yes | String | |
`update` | Ensure that the view has been updated before results are returned. | yes | String | `true` | `false`: Return view results before updating.<br/>`true`: Return view results after updating.<br/>`lazy`: Return the view results without waiting for an update, but update them immediately after the request.

<aside class="warning" role="complementary" aria-label="includedocsperformance">Note that using `include_docs=true` might have [performance implications](creating_views.html#include_docs_caveat).</aside>

### Indexes

When a view is defined in a design document,
a corresponding index is also created,
based on the information defined within the view.
Indexes let you select for documents by criteria other than their `_id` field, for instance by a field or combination of fields or by a value that is computed based on the contents of the document.
The index is populated as soon as the design document is created. On large databases, this process might take a while.

The index content is updated incrementally and automatically when any one of the following three events has occurred:

-   A new document has been added to the database.
-   An existing document has been deleted from the database.
-   An existing document in the database has been updated.

View indexes are rebuilt entirely when the view definition changes or when another view definition in the same design document changes.
This ensures that changes to the view definitions are reflected in the view indexes.
To achieve this,
a 'fingerprint' of the view definition is created whenever the design document is updated.
If the fingerprint changes,
then the view indexes are completely rebuilt.

<aside class="notice" role="complementary" aria-label="rebuildonchange">View index rebuilds occur whenever a change occurs to any one view from all the views defined in the design document.
For example,
if you have a design document with three views,
and you update the design document,
all three view indexes within the design document are rebuilt.</aside>

If the database has been updated recently, there might be a delay in returning the results when the view is accessed.
The delay is affected by the number of changes to the database, and whether the view index is not current because the database content has been modified.

It is not possible to eliminate these delays,
in the case of newly created databases you might reduce them by creating the view definition
in the design document in your database before inserting or updating documents.
This causes incremental updates to the index when the documents or inserted.

If speed of response is more important than having completely up-to-date data,
an alternative is to allow users to access an old version of the view index.
In effect,
the user has an immediate response from 'stale' index content,
rather than waiting for the index to be updated.
Depending on the document contents,
using a stale view might not return the latest information.
Nevertheless, a stale view returns the results of the view query quickly,
by using an existing version of the index.

### Accessing a stale view

If you are prepared to accept a response that is quicker,
but might not have the most current data,
there are three options you can use.

The `stale` option allows the results from a stale view to be used.
This makes the request return immediately,
even if the view has not been completely built.
If this parameter is not given,
or the value `false` is supplied,
a response is returned only after the view has been built.
The value `ok` allows stale views.
The value `update_after` allows stale views,
but updates them immediately after a response to the request has been created and processed.

The `stable` option allows you to indicate whether you would prefer to get results from a single,
consistent set of shards.
The default value is `false`,
meaning all available shard replicas are queried.
The first response received is the one that is used.
The benefit is that the response is not delayed in the event that any individual shard replica is slow to respond.
By contrast,
setting `stable` to `true` forces the database to use a single,
consistent set of shards to respond to the query.

The `update` option allows you to indicate whether you are prepared to accept
view results without waiting for the view to be updated.
The default value is `true`,
meaning that the view should be updated before results are returned.
The `lazy` value means that the results are returned before the view is updated,
but that the view must then be updated anyway.

When you specify `stable=true` in conjunction with `update=false` or `update=lazy`,
responses are consistent from request to request because a single,
consistent set of shards is used to respond to the query.
However,
if one of those shards is heavily loaded or slow to respond,
the response time might be adversely affected.

When the default `stable=false` value applies,
and you use either of `update=false` or `update=lazy`,
indexes between shard replicas might not be synchronized.
The effect would be that you might get different results,
depending on which replicas respond first.

In summary,
if you want the quickest possible response,
and are prepared to accept results that might not yet be synchronized,
or are returned from the first shard replica to respond rather than your normal set of shards,
then you could use the combination: `stable=false&update=false`.

Remember that using a stale view has consequences.
In particular,
accessing a stale view returns the current (existing) version of the data in the view index,
if it exists,
without waiting for an update.
This would mean that a stale view index result might be different from different nodes in the cluster.

<aside class="notice" role="complementary" aria-label="staleredundant">Cloudant automatically and actively works to keep views up-to-date at all times.
This means that the only time you might notice a difference when using `stable` or `update` options is when
there is an indexing backlog.</aside>

### Sorting Returned Rows

> Example of requesting the last five records by reversing the sort order:

```http
GET /$DATABASE/_design/<design-doc>/_view/by_title?limit=5&descending=true HTTP/1.1
Accept: application/json
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGNDOCUMENT/_view/by_title?limit=5&descending=true \
     -H "Content-Type: application/json"
```

> Example response:

```json
{
   "offset" : 0,
   "rows" : [
      {
         "id" : "Zucchiniinagrodolcesweet-sourcourgettes",
         "key" : "Zucchini in agrodolce (sweet-sour courgettes)",
         "value" : [
            null,
            "Zucchini in agrodolce (sweet-sour courgettes)"
         ]
      },
      {
         "id" : "Zingylemontart",
         "key" : "Zingy lemon tart",
         "value" : [
            null,
            "Zingy lemon tart"
         ]
      },
      {
         "id" : "Zestyseafoodavocado",
         "key" : "Zesty seafood avocado",
         "value" : [
            null,
            "Zesty seafood avocado"
         ]
      },
      {
         "id" : "Zabaglione",
         "key" : "Zabaglione",
         "value" : [
            null,
            "Zabaglione"
         ]
      },
      {
         "id" : "Yogurtraita",
         "key" : "Yogurt raita",
         "value" : [
            null,
            "Yogurt raita"
         ]
      }
   ],
   "total_rows" : 2667
}
```

The data returned by a view query is in the form of an array.
Each element within the array is sorted using native UTF-8 sorting.
The sort is applied to the key defined in the view function.

The basic order of output is as follows:

Value | Order
------|------
`null` | First
`false` |
`true` |
Numbers |
Text (lowercase) |
Text (uppercase) |
Arrays (according to the values of each element, using the order given in this table) |
Objects (according to the values of keys, in key order using the order given in this table) | Last

You can reverse the order of the returned view information by setting the `descending` query value <code>true</code>.

### Specifying Start and End Keys

> Example of querying using `startkey` and `endkey` query arguments:

```http
GET /recipes/_design/recipes/_view/by_ingredient?startkey="alpha"&endkey="beta" HTTP/1.1
Accept: application/json
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGNDOCUMENT/_view/by_ingredient?startkey="alpha"&endkey="beta" \
     -H "Content-Type: application/json"
```

The `startkey` and `endkey` query arguments can be used to specify the range of values to be displayed when querying the view.

The sort direction is always applied first.
Next, filtering is applied using the `startkey` and `endkey` query arguments.
This means that it is possible to have empty view results because the sorting and filtering do not make sense in combination.

<div></div>

> Reversing the order of start and end key might not yield any results:

```http
GET /recipes/_design/recipes/_view/by_ingredient?descending=true&startkey="beta"&endkey="alpha" HTTP/1.1
Accept: application/json
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGN_DOCUMENT/_view/by_ingredient?descending=true&startkey="beta"&endkey="alpha" \
     -H "Content-Type: application/json"
```

For example,
if you have a database that returns ten results when viewing with a `startkey` of "alpha" and an `endkey` of "beta",
you would get no results when reversing the order.
The reason is that the entries in the view are reversed before the key filter is applied.

<div></div>

> The view request returns no entries, because "alpha" is alphabetically before "beta". The returned result is empty:

```json
{
   "total_rows" : 26453,
   "rows" : [],
   "offset" : 21882
}
```

Therefore the `endkey` of "beta" is seen before the `startkey` of "alpha", resulting in an empty list.

<div></div>

> Example of <i>correct</i> filtering and reversing the order of output by using the `descending` query argument, and reversing the `startkey` and `endkey` query arguments:

```http
GET /recipes/_design/recipes/_view/by_ingredient?descending=true&startkey="egg"&endkey="carrots" HTTP/1.1
Accept: application/json
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGN_DOCUMENT/_view/by_ingredient?descending=true&startkey="egg"&endkey="carrots" \
     -H "Content-Type: application/json"
```

The solution is to reverse not just the sort order,
but also the `startkey` and `endkey` parameter values.

### Querying a view using a list of keys

> Example request to return all recipes, where the key for the view matches either "claret" or "clear apple juice":

```http
POST /$DATABASE/_design/$DESIGN_DOC/_view/$VIEWNAME HTTP/1.1
Content-Type: application/json
```

```shell
curl -X POST "https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGN_DOC/_view/$VIEWNAME" -d @request.json
```

```json
{
   "keys" : [
      "claret",
      "clear apple juice"
   ]
}
```

This method of requesting information from a database executes the specified `view-name` from the specified `design-doc` design document. Like the `keys` parameter for the [`GET`](using_views.html#querying-a-view) method,
the `POST` method allows you to specify the keys to use when retrieving the view results.
In all other aspects, the `POST` method is identical to the [`GET`](using_views.html#querying-a-view) API request, in particular, you can use any of its query parameters.

<div></div>

> Example returned view data

```json
{
   "total_rows" : 26484,
   "rows" : [
      {
         "value" : [
            "Scotch collops"
         ],
         "id" : "Scotchcollops",
         "key" : "claret"
      },
      {
         "value" : [
            "Stand pie"
         ],
         "id" : "Standpie",
         "key" : "clear apple juice"
      }
   ],
   "offset" : 6324
}
```

The response contains the standard view information,
but only where the keys match.

<div id="include_docs_caveat"></div>

### Multi-document Fetching

> Example request to obtain the full documents that match the listed keys:

```http
POST /recipes/_design/recipes/_view/by_ingredient?include_docs=true HTTP/1.1
Content-Type: application/json

{
   "keys" : [
      "claret",
      "clear apple juice"
   ]
}
```

```shell
curl "https://$ACCOUNT.cloudant.com/$DATABASE/$DESIGN_DOC/_view/by_ingredient?include_docs=true"
     -X POST \
     -H "Content-Type: application/json" \
     -d "{ "keys" : [ "claret", "clear apple juice" ] }"
```

> Example response (abbreviated), returning the full document for each recipe:

```json
{
   "offset" : 6324,
   "rows" : [
      {
         "doc" : {
            "_id" : "Scotchcollops",
            "_rev" : "1-bcbdf724f8544c89697a1cbc4b9f0178",
            "cooktime" : "8",
            "ingredients" : [
               {
                  "ingredient" : "onion",
                  "ingredtext" : "onion, peeled and chopped",
                  "meastext" : "1"
               }
            ],
            "keywords" : [
               "cook method.hob, oven, grill@hob",
               "diet@wheat-free",
               "diet@peanut-free",
               "special collections@classic recipe",
               "cuisine@british traditional",
               "diet@corn-free",
               "diet@citrus-free",
               "special collections@very easy",
               "diet@shellfish-free",
               "main ingredient@meat",
               "occasion@christmas",
               "meal type@main",
               "diet@egg-free",
               "diet@gluten-free"
            ],
            "preptime" : "10",
            "servings" : "4",
            "subtitle" : "This recipe comes from an old recipe book of 1683 called 'The Gentlewoman's Kitchen'. This is an excellent way of making a rich and full-flavoured meat dish in a very short time.",
            "title" : "Scotch collops",
            "totaltime" : "18"
         },
         "id" : "Scotchcollops",
         "key" : "claret",
         "value" : [
            "Scotch collops"
         ]
      },
      {
         "doc" : {
            "_id" : "Standpie",
            "_rev" : "1-bff6edf3ca2474a243023f2dad432a5a",
            "cooktime" : "92",
            "ingredients" : [
            ],
            "keywords" : [
               "diet@dairy-free",
               "diet@peanut-free",
               "special collections@classic recipe",
               "cuisine@british traditional",
               "diet@corn-free",
               "diet@citrus-free",
               "occasion@buffet party",
               "diet@shellfish-free",
               "occasion@picnic",
               "special collections@lunchbox",
               "main ingredient@meat",
               "convenience@serve with salad for complete meal",
               "meal type@main",
               "cook method.hob, oven, grill@hob / oven",
               "diet@cow dairy-free"
            ],
            "preptime" : "30",
            "servings" : "6",
            "subtitle" : "Serve this pie with pickled vegetables and potato salad.",
            "title" : "Stand pie",
            "totaltime" : "437"
         },
         "id" : "Standpie",
         "key" : "clear apple juice",
         "value" : [
            "Stand pie"
         ]
      }
   ],
   "total_rows" : 26484
}
```

Combining a `POST` request to a given view,
with the `include_docs=true` query argument,
enables you to retrieve multiple documents from a database.
For a client application,
this technique is more efficient than using multiple [`GET`](using_views.html#querying-a-view) API requests.

However,
`include_docs=true` might incur an overhead compared to accessing the view on its own.

The reason is that by using `include_docs=true` in a search,
all of the result documents must be retrieved to construct the response back to the client application.
In effect,
a whole series of document `GET` requests are performed,
each of which competes for resources with other application requests.

One way to mitigate this effect is by retrieving results directly from the Lucene index files.
You can do this by not specifying `include_docs=true`.
Instead,
in your design document specify `store=true` and `index=false` on the fields you want retrieved by your query.

For example,
in your index function,
you might use:

	`index("name", doc.name, {"store": true, "index": false});`

You could use the same approach for view indexes.

### Sending several queries to a view

> Example request:

```http
POST /$DATABASE/_design/$DESIGNDOC/_view/$VIEW HTTP/1.1
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGNDOC/_view/$VIEW -H 'Content-Type: application/json' -d @request-body.json
# where request-body.json is a file containing the following JSON data:
```

```json
{
  "queries": [{

  }, {
    "startkey": 1,
    "limit": 2
  }]
}
```

> Example response:

```json
{
  "results": [
		{
		  "total_rows": 3,
		  "offset": 0,
		  "rows": [
				{
				  "id": "8fbb1250-6908-42e0-8862-aef60dc430a2",
				  "key": 0,
				  "value": {
				    "_id": "8fbb1250-6908-42e0-8862-aef60dc430a2",
				    "_rev": "1-ad1680946839206b088da5d9ac01e4ef",
				    "foo": 0,
				    "bar": "foo"
				  }
				}, {
				  "id": "d69fb42c-b3b1-4fae-b2ac-55a7453b4e41",
				  "key": 1,
				  "value": {
				    "_id": "d69fb42c-b3b1-4fae-b2ac-55a7453b4e41",
				    "_rev": "1-abb9a4fc9f0f339efbf667ace66ee6a0",
				    "foo": 1,
				    "bar": "bar"
				  }
				}, {
				  "id": "d1fa85cd-cd18-4790-8230-decf99e1f60f",
				  "key": 2,
				  "value": {
				    "_id": "d1fa85cd-cd18-4790-8230-decf99e1f60f",
				    "_rev": "1-d075a71f2d47af7d4f64e4a367160e2a",
				    "foo": 2,
				    "bar": "baz"
				  }
				}
		  ]
		}, {
		  "total_rows": 3,
		  "offset": 1,
		  "rows": [
				{
				  "id": "d69fb42c-b3b1-4fae-b2ac-55a7453b4e41",
				  "key": 1,
				  "value": {
				    "_id": "d69fb42c-b3b1-4fae-b2ac-55a7453b4e41",
				    "_rev": "1-abb9a4fc9f0f339efbf667ace66ee6a0",
				    "foo": 1,
				    "bar": "bar"
				  }
				}, {
				  "id": "d1fa85cd-cd18-4790-8230-decf99e1f60f",
				  "key": 2,
				  "value": {
				    "_id": "d1fa85cd-cd18-4790-8230-decf99e1f60f",
				    "_rev": "1-d075a71f2d47af7d4f64e4a367160e2a",
				    "foo": 2,
				    "bar": "baz"
				  }
				}
		  ]
  	}
  ]
}
```

To send several view queries in one request, use a `POST` request to `/$DATABASE/_design/$DESIGN_DOC/_view/$VIEW`. The request body is a JSON object containing only the `queries` field. It holds an array of query objects with fields for the parameters of the query. The field names and their meaning are the same as the query parameters of a regular view request.

The JSON object returned in the response contains only the `results` field, which holds an array of result objects - one for each query. Each result object contains the same fields as the response to a regular view request.

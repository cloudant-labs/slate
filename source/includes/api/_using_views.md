## Using Views

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the 'Using Views' topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/using_views.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

View enable you to search for content within a database,
that matches specific criteria.
The criteria are specified within the view definition,
or supplied as arguments when you use the view.

### Querying a view

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
`stable` | Prefer view results from a 'stable' set of shards. This means that the results are from a view that is less likely to be updated soon. | yes | Boolean | true | 
`stale` | Allow the results from a stale view to be used. This makes the request return immediately, even if the view has not been completely built yet. If this parameter is not given, a response is returned only after the view has been built. | yes | String | false | `ok`: Allow stale views.<br/>`update_after`: Allow stale views, but update them immediately after the request.
`startkey` | Return records starting with the specified key. | yes | String or JSON array | |
`startkey_docid` | Return records starting with the specified document ID. | yes | String | |
`update` | Ensure that the view has been updated before results are returned. | yes | String | `true` | `false`: Return view results before updating.<br/>`true`: Return view results after updating.<br/>`lazy`: Return the view results without waiting for an update, but update them immediately after the request.

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

<aside class="notice" role="complementary" aria-label="rebuildsafterchange">View index rebuilds occur whenever a change occurs to any one view from all the views defined in the design document.
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

<aside class="notice" role="complementary" aria-label="staledeprecated">The earlier method of obtaining potentially older results from a view index,
using the <code class="prettyprint">stale=ok</code> option,
is no longer recommended.</aside>

If you are prepared to accept a response that is quicker,
but might not have the most current data,
there are two options you can use:

Option   | Purpose                                                                                                         | Default value
---------|-----------------------------------------------------------------------------------------------------------------|--------------
`stable` | Should the view results be obtained from a 'stable' set of shards? Possible values include `true`, and `false`. | `true`
`update` | Should the view be updated before the results are returned? Possible values include `true`, `false` and `lazy`. | `true`

The `stable` option allows you to indicate whether you are prepared to accept
view results from a set of shards that might still be in the process of updating,
that is they are not 'stable' as far as the current view query is concerned.
The default value is `true`,
meaning that the results should be from a stable set of shards.

The `update` option allows you to indicate whether you are prepared to accept
view results without waiting for the view to be updated.
The default value is `true`,
meaning that the view should be updated before results are returned.
The `lazy` value means that the results are returned before the view is updated,
but that the view must then be updated anyway.

The option combination `stable=true&update=false` corresponds to the older option `stale=ok`.
The option combination `stable=true&update=lazy` corresponds to the older option `stale=update_after`.

Remember that using a stale view has consequences.
In particular,
accessing a stale view returns the current (existing) version of the data in the view index,
if it exists,
without waiting for an update.
This would mean that a stale view index result might be different on different nodes in the cluster.

### Sorting Returned Rows

> Example of requesting the last five records by reversing the sort order:

```http
GET /$DATABASE/_design/<design-doc>/_view/by_title?limit=5&descending=true HTTP/1.1
Accept: application/json
Content-Type: application/json
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
GET /recipes/_design/recipes/_view/by_ingredient?startkey=%22alpha%22&endkey=%22beta%22 HTTP/1.1
Accept: application/json
Content-Type: application/json
```

The `startkey` and `endkey` query arguments can be used to specify the range of values to be displayed when querying the view.

The sort direction is always applied first.
Next, filtering is applied using the `startkey` and `endkey` query arguments.
This means that it is possible to have empty view results because the sorting and filtering do not make sense in combination.

<div></div>

> Reversing the order of start and end key will not yield any results:

```http
GET /recipes/_design/recipes/_view/by_ingredient?descending=true&startkey=%22beta%22&endkey=%22alpha%22 HTTP/1.1
Accept: application/json
Content-Type: application/json
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
GET /recipes/_design/recipes/_view/by_ingredient?descending=true&startkey=%22egg%22&endkey=%22carrots%22 HTTP/1.1
Accept: application/json
Content-Type: application/json
```

The solution is to reverse not just the sort order,
but also the `startkey` and `endkey` parameter values.

### Querying a view using a list of keys

> Example request to return all recipes, where the key for the view matches either "clear apple juice" or "lemonade":

```http
POST /$DATABASE/_design/$DESIGN_DOC/_view/$VIEWNAME HTTP/1.1
Content-Type: application/json
```

```shell
curl -X POST "https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DDOC/_view/$VIEWNAME" -d @request.json
```

```json
{
   "keys" : [
      "some-key",
      "some-other-key"
   ]
}
```

This method of requesting information from a database executes the specified `view-name` from the specified `design-doc` design document. Like the `keys` parameter for the [`GET`](#querying-a-view) method,
the `POST` method allows you to specify the keys to use when retrieving the view results.
In all other aspects, the `POST` method is identical to the [`GET`](#querying-a-view) API request, in particular, you can use any of its query parameters.

<div></div>

The response contains the standard view information, but only where the keys match:

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

> Example response, returning the full document for each recipe:

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
               },
            ...
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
...            ],
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

Combining a `POST` request to a given view, with the `include_docs=true` query argument, enables you to retrieve multiple documents from a database.
This technique is more efficient than using multiple [`GET`](#querying-a-view) API requests.
However,
`include_docs=true` adds a slight overhead compared to accessing the view on its own.

### Sending several queries to a view

> Example request:

```http
POST /$DATABASE/_design/<design_doc>/_view/<view> HTTP/1.1
Content-Type: application/json
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/_design/$DESIGN_DOC/_view/$VIEW -H 'Content-Type: application/json' -d @request-body.json
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

To send several view queries in one request, use a `POST` request to `/$DATABASE/_design/<design_doc>/_view/<view>`. The request body is a JSON object containing only the `queries` field. It holds an array of query objects with fields for the parameters of the query. The field names and their meaning are the same as the query parameters of a regular view request.

The JSON object returned in the response contains only the `results` field, which holds an array of result objects - one for each query. Each result object contains the same fields as the response to a regular view request.

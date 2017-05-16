## Cloudant Query Guide

Cloudant Query is an easy to use, RESTful API to create indexes and query data on Cloudant. The query syntax will feel familiar to anyone who has written queries for MongoDB. This guide explains how to define indexes and query documents and notes some differences to MongoDB. We also talk about managing indexes and how indexes are represented in design documents.

### Sample Data

In this guide, we will use a database with information about actors and movies they've starred in to illustrate Cloudant Query. To make the requests, we will use the command line tool `curl <http://curl.haxx.se/>`_. The database contains JSON documents like this one:

```json
{
    "Person_dob": "1996-09-16",
    "Movie_year": 2006,
    "Person_pob": "New York, New York, USA",
    "_id": "ef880463bcc2deabd3f9798dbe5e4aaf",
    "_rev": "1-6d5923d2e34da6e293a0ec1ba72b39d2",
    "Movie_runtime": 101,
    "Movie_rating": "R",
    "Person_name": "Abigail Breslin",
    "Movie_genre": "CD",
    "Movie_name": "Little Miss Sunshine"
}
```

The dataset we’re using is a small (subset of IMDb data)[http://www.imdb.com/interfaces] that the service makes available for non-commercial and educational purposes. Here, we’ve denormalized the separate tables for Actor, Movie, and Person to fit within Cloudant’s JSON document-oriented model.
    
So in accordance with IMDb’s (Conditions of Use)[http://www.imdb.com/help/show_article?conditions], we’d like to add:
 
 | Information courtesy of
 | IMDb
 | (http://www.imdb.com).
 | Used with permission.

To follow along, replicate the database `https://examples.cloudant.com/movies-demo/` into your own account. This database only contains the sample data. No indexes have been defined yet. In order to do queries, you must define indexes yourself. Alternatively, you could instead use the following :ref:`test form <cloudant-query-guide-form>`.

```shell
    curl 'https://user:password@user.cloudant.com/_replicate' -X POST -H 'Content-Type: application/json' -d '{
      "source": "https://examples.cloudant.com/movies-demo",
      "target": "https://user:password@user.cloudant.com/movies-demo",
      "create_target": true,
      "use_checkpoints": false
      }'
```

### Defining indexes and queries

Cloudant Query is a good starting point to learn how to query data in a Cloudant database. It makes your life easier even if you have plenty of experience with CouchDB or Cloudant. Cloudant Query lets you declaratively define indexes and query them. Data can only be queried if there is an appropriate index available. If there isn't, the query will result in an error informing you of the missing index. This might sound more difficult, but is actually a good thing. It ensures that your queries will perform well even on large datasets and lets you address performance issues before they become a problem in production.

#### Creating Indexes

To create an index, you need to choose the fields you want to be indexed and submit a `POST` request. 

You can create an index for the `Person_name``field:

```shell
   curl -X POST 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_index' -d '{ "index": { "fields": ["Person_name"] } }'
```

Let's look at the JSON object submitted in the request body.

```json
{
  "index": {
    "fields": ["Person_name"]
  }
}
```

It has a single field, describing the index, which is itself an object with a single field, an array of the fields to be indexed.

The databse server will return

```json
{
  "result": "created"
}
```

to confirm that the index was created. If the index already exists the response is:

```json
{
  "result": "exists"
}
```

In both cases, the HTTP status code will be 200.

#### Querying data

Once you have an index, you can query the database by POSTing a JSON document to the `_find` endpoint.

```shell
curl -X POST https://<user>:<pass>@<user>.cloudant.com/movies-demo/_find -d '{ "selector": { "Person_name": "Zoe Saldana" } }'
```

And again we look at the request body:

```json
{
  "selector": {
    "Person_name": "Zoe Saldana"
  }
}
```

This is the most simple query possible. It has a selector, which specifies which documents to return. The selector matches any document where the `Person_name` field is `"Zoe Saldana"`. For our example data set, only a single document matches this query, but that need not be the case in general. Here's the result:

```json
{
  "docs": [
    {
      "Movie_earnings_rank": "1",
      "Movie_genre": "AVYS",
      "Movie_name": "Avatar",
      "Movie_rating": "PG-13",
      "Movie_runtime": 162,
      "Movie_year": 2009,
      "Person_dob": "1978-06-19",
      "Person_name": "Zoe Saldana",
      "Person_pob": "New Jersey, USA",
      "_id": "1f003ce73056238720c2e8f7da545390",
      "_rev": "1-8522c9a1d9570566d96b7f7171623270"
    }
  ]
}
```

The result format is very straight forward. You get an object with a single field, ``docs``, which contains an array with all (or the first batch of, if there are too many) matching documents.

##### What happens if there is no index for my query?

As I warned you earlier, sending a query that doesn’t have a suitable index will result in an error. Let's see:

```shell
curl -X POST 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_find' -d '{ "selector": { "Movie_earnings_rank": 191 } }'
```

Because your database may be terabytes in size, indexing all fields in all documents is not desirable. Cloudant Query will not automatically index your data. It *will* tell you the indexes you need to define, if a query cannot be satisfied. How you choose to handle that error is up to you, you can change your query or you can create a new index.

```json
{
  "reason": "No index exists for this selector, try indexing one of: Movie_earnings_rank",
  "error": "no_usable_index"
}
```

##### Some more indexes

Lets define a few more indexes. This one is for ``Person_dob``, date of birth, using descending sort order:

```shell
curl -X POST 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_index' -d '{ "index": { "fields": [{"Person_dob": "desc"}] } }'
```

And one to combine `Movie_name` and `Person_name`:

```shell
curl -X POST 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_index' -d '{ "index": { "fields": ["Movie_name", "Person_name"] } }'
```

This allows efficient queries to check whether an actor starred in a movie.

##### Refining results

> Refining results

```shell
curl -X POST 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_find' -d '
  {
    "selector": {
      "Movie_year": 1978,
      "Person_name": "Robert De Niro"
    }
  }'
```

> Result:

```json
{
  "docs": [
    {
      "Movie_genre": "DW",
      "Movie_name": "Deer Hunter, The",
      "Movie_rating": "R",
      "Movie_runtime": 183,
      "Movie_year": 1978,
      "Person_dob": "1943-08-17",
      "Person_name": "Robert De Niro",
      "Person_pob": "New York, New York, USA",
      "_id": "1f003ce73056238720c2e8f7da428f32",
      "_rev": "1-3fa59b11f43719f46c288b9bb9943d1d"
    }
  ]
}
```

You can refine queries by filtering on fields that are not in the index. Assuming we have an index for ``Person_name``, but not for ``Movie_year``, the following query will still work, but it will have to go through all documents with a matching name to filter out those that do not match the given year. In this case, that shouldn't be a problem, because even Robert De Niro didn't star in a million movies. But for other data sets, performance can be an issue.

#### Let's do something a bit more difficult

> SQL query example

```
SELECT Movie.name, Movie.year 
  FROM Actor, Person, Movie 
    WHERE Movie.year > 1960 
      AND Movie.id = Person.movie_id 
      AND Person.name = 'Alec Guinness'
    ORDER BY Movie.year DESC;
```

> In the MongoDB shell, you could use the following command:

```
db.movies_demo.find({
  Movie_year: {"$gt": 1960},
  Person_name: "Alec Guinness"
},{
  Movie_name: 1,
  Movie_year: 1,
  _rev: 1
}).sort({ Movie_year: -1 });
```

> Here is the Cloudant query:

```shell
curl -X POST 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_find' -d '{
  "fields": ["Movie_name", "Movie_year", "_id", "_rev"],
  "selector": {
    "Movie_year": {"$gt": 1960},
    "Person_name": "Alec Guinness"
  },
  "sort": [{"Movie_year": "desc"}]
}'
```

> And here is the result:

```json
{
  "docs": [
    {
      "_rev": "1-f82449fc19cd9019adf33b8b7f8f18de",
      "_id": "ef880463bcc2deabd3f9798dbe5f93b8",
      "Movie_year": 1984,
      "Movie_name": "Passage to India, A"
    },
    {
      "_rev": "1-5127049d787ceb1bde7512a359db52c6",
      "_id": "ef880463bcc2deabd3f9798dbe5f85bb",
      "Movie_year": 1977,
      "Movie_name": "Star Wars"
    },
    {
      "_rev": "1-7c5efddbd37d313eed7b4a6ccf572d9d",
      "_id": "ef880463bcc2deabd3f9798dbe5f8681",
      "Movie_year": 1962,
      "Movie_name": "Lawrence of Arabia"
    }
  ]
}
```

So far we've only looked at very simple selectors and haven't used other features at all. For the next query, we use the ``$gt`` operator to find movies made after 1960 and to get a smaller reply, we tell the database which fields to return. Our query is equivalent to this SQL query:

The `fields` field is the list of fields we want, similar to the `SELECT` clause in an SQL query. If the `fields` object is omitted, the entire object is returned, equivalent to `SELECT *`. The `selector` field has the same function as the `WHERE` clause with `"Movie_year": {"$gt": 1960}` corresponding to `Movie.year > 1960`.


### Try it yourself!

.. raw:: html

    <form action="#" id="testForm">
        <textarea rows="10" cols="80" id="requestBody"></textarea><br /><br />
        <input type="submit" value="query"></input><br />
    </form>
    <pre style="display:none;" id="testOutput"></pre>
    <script>
        $(document).ready(function() {
        var requestBodyInput = $("#requestBody");
        requestBodyInput.val('{\n    "selector": {\n        "Movie_year": { "$gte": 2012 }\n    },\n    "limit": 1\n}');
        var form = $("#testForm");
        form.submit(function(event) {
            var requestBody = requestBodyInput.val();
            jQuery.ajax({
                url: '/examples/_find',
                type: 'POST',
                data: requestBody,
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("Content-Type", "application/json");
                    // xhr.setRequestHeader("Authorization", "Basic " + btoa('thereencespedgetytolisir:c1IimpBSAC3b3A66N8LHKwKF'));
                },
                complete: function(jqXHR, textStatus) {
                    var result = JSON.stringify(jQuery.parseJSON(jqXHR.responseText), null, '    ');
                    var outputField = $("#testOutput");
                    outputField.show();
                    outputField.text(result);
                }
            });
            event.preventDefault();
        });
        form.submit();
        });
    </script>

.. Differences between Cloudant Query and MongoDB
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. While Cloudant Query will be easy to pick up for anyone who has worked with MongoDB, it does not aim to be a compatibility layer. Here are a few points to keep in mind when transitioning from MongoDB.

..  * Cloudant Query uses HTTP. Like any other Cloudant API, Cloudant Query uses RESTful HTTP as the basis.
..  * You need an appropriate index for all queries. While MongoDB lets you do queries without defining an index first, Cloudant Query does not let you do that. However, it will tell you which indeces are missing, and creating the missing index is easy. This also ensures that when the amount of data in your database grows, your queries will still perform well.
..  * Cloudant Query uses different syntax for selecting fields to be returned and for sorting the result of a query.
..  * Cloudant Query uses JSON, not Javascript. The MongoDB Shell uses Javascript and thus many code examples you will find also use Javascript, for example to specify selectors. This is just a minor syntactical difference, but it can trip you up. While ``{ selector: { name: 'John'} }`` is valid Javascript, it is not valid JSON and you have to write ``{ "selector": { "name": "John"} }`` instead.

.. And a few more nitpicks:

..  * The ``$or`` operator behaves differently, as it requires all its selectors to use the same index.
..  * By default, Cloudant Query returns only the first 25 matching documents. This can be changed by setting a different value for the ``limit`` field.
..  * The sort order (as well as the ordering used by comparison operators like $gt) might differ from MongoDB in some ways. It follows `CouchDB's view collation sort order <http://wiki.apache.org/couchdb/View_collation>`_.


### Managing indexes

When you create an index with Cloudant Query, a design document containing the index will be created (or updated) and a view will be built based on this index. In this section, we look at how to list and delete indexes.

#### Listing indexes

> Getting a list of indexes

```shell
curl -X GET https://<user>:<pass>@<user>.cloudant.com/movies-demo/_index
```

> Result showing several indexes:

```json
{
  "indexes": [
    {
      "def": {
        "fields": [
          {
            "Person_dob": "asc"
          }
        ]
      },
      "type": "json",
      "name": "4c4a214887d5ef7e5594091be1ce51ecb0aeaf37",
      "ddoc": "_design/4c4a214887d5ef7e5594091be1ce51ecb0aeaf37"
    },
    {
      "def": {
        "fields": [
          {
            "Person_name": "asc"
          }
        ]
      },
      "type": "json",
      "name": "6d1f30b1f2f363a750d9891c007f1020e20da714",
      "ddoc": "_design/6d1f30b1f2f363a750d9891c007f1020e20da714"
    },
    {
      "def": {
        "fields": [
          {
            "Movie_year": "asc"
          },
          {
            "Movie_runtime": "asc"
          },
          {
            "Movie_rating": "asc"
          },
          {
            "Movie_genre": "asc"
          },
          {
            "Movie_name": "asc"
          }
        ]
      },
      "type": "json",
      "name": "c85c94c6f67ad0ea697e2a8d99a19a71a1eea34b",
      "ddoc": "_design/c85c94c6f67ad0ea697e2a8d99a19a71a1eea34b"
    }
  ]
}
```

To get a list of all indexes in a database, send a ``GET`` request to the ``/db/_index`` endpoint.

In this example, you can see three indexes. The first two indexes each index one field while the last index has five fields. It could be used to do queries that combine several search criteria.

You can use the `name` (view name) and the `ddoc` (design document ID) you find there to query the view in the usual manner, should you need to use the :ref:`view API <index-functions>`.

#### Deleting indexes

> Here is how you would delete the first index listed:

```shell
curl -X DELETE 'https://<user>:<pass>@<user>.cloudant.com/movies-demo/_index/4c4a214887d5ef7e5594091be1ce51ecb0aeaf37/json/4c4a214887d5ef7e5594091be1ce51ecb0aeaf37""'
```

To delete an index, send a `DELETE` request to `/$db/_index/$designdoc/$type/$name`, where `$db` is the name of the database, `$designdoc` is the ID of the design document, `$type` is the type of the index (e.g. json or text), and `$name` is the name of the index. 



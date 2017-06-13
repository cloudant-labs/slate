## Querying data

In this guide we look at how to query data using Cloudant Query. We create a database by replicating
some sample data, create an index, and finally execute some queries. You can follow along and run
our curl commands from the browser.

## How to use the interactive guide

All code snippets can be *run and edited* in the browser. Make sure to follow along step-by-step
and run the examples in the correct order. If you skip one of the code snippets, other ones might
not work. For example, if you don't run the first step, creating a session token, none of the other
code snippets will work because you need the session token to authenticate. We encourage you to
change the examples and see how the service will respond.

<aside class="warning" role="complementary" aria-label="notForSensitiveData"> Note: The interactive guide is only intended as a "playground" to try out Cloudant.
*Don't use it with sensitive data!*
</aside>

You can find instructions on [how to run the code snippets locally](#running-code-locally) towards
the end of this guide.

### Logging in

Before you can do anything with the service, you need to obtain a session token. Use basic
authentication to get the token and then use the session token to authenticate. Otherwise,
requests will take longer because the service will need to verify your credentials at each step.

The following code contains all we need for the initial connection to Cloudant. It sets up variables
for the credentials and the base URL of a Cloudant account and it sets some defaults parameters for curl.
If you don't have an account yet, you can [sign up](https://cloudant.com/sign-up/) and copy your
credentials into the script. You can also use the 'docs-playground' account, if you don't want to
use your own account.

Once the variables are set, the script sends a request to the [`/_session` endpoint](api.html#authentication).
The response contains your session token in the `SET-COOKIE` header, which curl stores in `cookie.txt`
and which we'll use for authentication in subsequent requests.

We use [jq](https://stedolan.github.io/jq/) to parse and display the JSON response.

<pre class="thebe">
# You can replace those with your credentials (username, password, and account name).
USER='docs-playground'
PASS='docs-playground'
URL='https://docs-playground.cloudant.com'
# some defaults for curl
alias curl='curl --max-time 180 --connect-timeout 5 --silent --show-error --cookie cookie.txt'
# get the session cookie and store it in cookie.txt
echo 'logging in...'
curl "${URL}/_session" -X POST -d "name=$USER" -d "password=$PASS" -c cookie.txt | jq '.'
echo "Here is our session cookie: $(tail -1 cookie.txt | cut -f 7)"
</pre>

#### Things you might want to try - logging in

 * Change the user name or password and see what errors you get.
 * Look at the response headers with `curl -v`.

### Replicating sample data

The sample database contains 9,000 movie documents like the following one:

```json
{
    "_id": "71562",
    "_rev": "1-72726eda3b8b2973ef259dd0c7410a83",
    "title": "The Godfather: Part II",
    "year": 1974,
    "rating": "R",
    "runtime": "200 min",
    "genre": [
        "Crime",
        "Drama"
    ],
    "director": "Francis Ford Coppola",
    "writer": [
        "Francis Ford Coppola (screenplay)",
        "Mario Puzo (screenplay)",
        "Mario Puzo (based on the novel \"The Godfather\")"
    ],
    "cast": [
        "Al Pacino",
        "Robert Duvall",
        "Diane Keaton",
        "Robert De Niro"
    ],
    "poster": "http://ia.media-imdb.com/images/M/..._V1_SX300.jpg",
    "imdb": {
        "rating": 9.1,
        "votes": 656,
        "id": "tt0071562"
    }
}
```

We create a new database by replicating the sample dataset from
`examples.cloudant.com`. We pipe the response through `jq '.'` for nicer output formatting.

<pre class="thebe">
echo "creating the replicator database... (will fail if it already exists, but that's okay)"
curl "$URL/_replicator" \
     -X PUT \
| jq '.'

# make a timestamped database name (or use any database name if you're using your own account)
DBNAME="movies$(date '+%s')"
# write our replication request into replication.json
cat << ENDREPLICATION >replication.json
{
  "source": "https://examples.cloudant.com/query-movies",
  "target": {
    "url": "$URL/$DATABASE",
    "headers": {
      "Cookie": "AuthSession=$(tail -1 cookie.txt | cut -f 7)"
    }
  },
  "create_target": true
}
ENDREPLICATION

echo "creating the replication job to copy data to $DATABASE ..."
curl "$URL/_replicator/$DATABASE" \
     -X PUT \
     -H 'Content-Type: application/json' \
     -d @replication.json \
| jq '.'
</pre>

This does two things: It creates a special database called `_replicator` to hold our replication jobs.
Don't worry if this first step fails - the database might already exist. Then we create a new document
in `_replicator` that describes our replication job, setting a source and a target and telling the
service to create the target database.

Now that the replication job has been created, we can check on its status by running the following commands:

<pre class="thebe">
echo 'querying the replication document...'
curl "$URL/_replicator/$DATABASE" | jq '.'

echo 'getting more information about the replication status...'
curl "$URL/_active_tasks" | jq ". | map(select(.doc_id == \"$DATABASE\"))"
</pre>

When the replication job has been started, the document in the replicator databse will have been updated with `"replication_state": "triggered"`
allowing you to monitor its status. You can run the earlier snippet again until you see `"replication_state": "completed"`
indicating all data has been copied to your target database. The second command queries the `_active_tasks` endpoint
and filters the result by `doc_id` in order to get more information about the status of the replication job,
such as the number of documents written.

<aside class="warning" role="complementary" aria-label="bePatient">
The replication job might take a minute or two. Just run the earlier snippet again to see when it is done.
There is no need to wait though; you can continue with the tutorial while the snippet is still running.
</aside>

#### Things you might want to try - replicating sample data

 * Changing the database name.
 * Creating multiple databases.
 * Using `curl "$URL/$DATABASE" -X DELETE` to remove the replicated database and start over.

### Creating an index

Cloudant supports different ways of querying data: Cloudant Query, map-reduce indexes, and full-text
search indexes. Let's start with the easiest one, Cloudant Query.

First, we'll need to create an index. We make a `POST` request to the `/_index` endpoint of our
newly created movies database containing a description of the index we want to create in the request
body.

<pre class="thebe">
echo 'creating an index...'
curl "$URL/$DATABASE/_index" \
     -X POST \
     -H 'Content-Type: application/json' \
     -d '{
           "type": "text",
           "index": {}
         }' \
| jq '.'
</pre>

We choose a text index so that we'll be able to do full-text queries. Since we haven't specified
any fields to index, Cloudant Query will index everything.

#### Things to try

 * Creating an index of type `json`
 * Indexing only some fields
 * Have a look at the API reference to learn more about [creating Cloudant Query indexes](cloudant_query.html#creating-an-index)

### Querying your data

With Cloudant Query, you can do far more complex queries, but let's start with something simple -
getting all movies with an IMDB rating of exactly 8. This time we send a `POST` request to the
`/_find` endpoint. Similarly to the index creation, we send a JSON document describing the
query in the request body. We limit our query to 3 so that the output won't be too long.

<pre class="thebe">
echo 'getting movies with rating = 8 ...'
curl "$URL/$DATABASE/_find" \
     -X 'POST' \
     -H 'Content-Type: application/json' \
     -d '{
           "selector": {
             "imdb": { "rating": 8}
           },
           "limit": 3
         }' \
| jq '.'
</pre>

The result will contain 3 documents from our database that match the given selector. Try to change
the selector and run the code again to experiment with different conditions. The
[API reference for Cloudant Query](cloudant_query.html#finding-documents-using-an-index)
provides more in depth information about different querying options.

#### Sorting

To sort your results, just specify a field name and its type (`string` or `number`) to sort by. In
this example, we sort alphabetically by movie title. Setting `fields` to `["title"]` let's us
retrieve only the `title` field of each document.

<pre class="thebe">
echo 'getting 2001 movies sorted by title...'
curl "$URL/$DATABASE/_find" \
     -X 'POST' \
     -H 'Content-Type: application/json' \
     -d  '{
            "selector": {
              "year": 2001
            },
            "sort": [ "title:string" ],
            "fields": [ "title" ],
            "limit": 3
          }' \
| jq '.'
</pre>

#### Searching the entire document

Until now we have only searched within specific fields, but sometimes you might want to search the
entire document. The `$text` operator does just that (and more), as the following example
illustrates:

<pre class="thebe">
echo 'getting bond movies...'
curl "$URL/$DATABASE/_find" \
     -X 'POST' \
     -H 'Content-Type: application/json' \
     -d  '{
            "selector": {
              "$text": "Bond"
            },
            "fields": [ "title", "cast" ],
            "limit": 3
          }' \
| jq '.'
</pre>

#### Finding a value in an array

A common query against a movie database is to list all movies an actor has appeared in. We can use
the `$in` operator to find out whether a value is present in the array of actors that is the value
of the `cast` field.

<pre class="thebe">
echo 'getting movies featuring Zoe Saldana...'
curl "$URL/$DATABASE/_find" \
     -X 'POST' \
     -H 'Content-Type: application/json' \
     -d  '{
            "selector": {
              "cast": {
                "$in": [ "Zoe Saldana" ]
              }
            },
            "fields": [ "title", "cast", "director" ],
            "limit": 3
          }' \
| jq '.'
</pre>

The examples in this guide only scratch the surface of what you can do with Cloudant Query. To learn
more, check out the [API Reference](cloudant_query.html) and play around with the queries on this site.

### Running code locally

To run the code snippets in this guide on your own machine, you need `bash`, `curl`, and `jq`.

1. If you're using MacOS or Linux, `bash` will already be installed as the default shell. On Windows, you need to install [Cygwin](https://cygwin.com/install.html).
2. Download and install [curl](https://curl.haxx.se/download.html).
3. Download the [jq](https://stedolan.github.io/jq/download/) executable and put it on your path.

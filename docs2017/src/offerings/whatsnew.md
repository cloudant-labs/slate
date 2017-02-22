---

copyright:
  years: 2015, 2017
lastupdated: "2017-01-31"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-01-26 -->

# What's new for Cloudant users

CouchDB 1.x now supports the following features.

-   Changes feeds now support view-based filters
-   Changes feeds now support the _doc_ids filter
-   `POST` requests are supported for _changes
-   Both _all_docs and _changes now support the  attachments=true parameter
-   Support for the CouchDB 1.6 _users database features (server-side password hashing when creating documents in the _users database, etc).

CouchDB 2.x and Cloudant now support the following features.

-   /_bulk_get endpoint to reduce the number of requests used in replication to mobile clients
-   Design document meta data now contains an "update pending" field
-   Views now support stable/update keywords


# Breaking / behaviour changes

Active tasks

-   Indexer entries in the _active_tasks response no longer report the "user" field.
-   Search indexer entries in the _active_tasks response no longer report the "user" field.

Views

 * Unicode normalisation of key values is now consistent between reduced and non-reduced view results. If raw collation is specified in a design document, result order may change as a result of this fix.
 * It is an error to specify the "keys" parameter and any of "key", "startkey" and "endkey" when querying a view or _all_docs.
 * It is now an error to pass "startkey" and "endkey" parameters to a view if it is impossible for any row to match, for example when "startkey" is higher than "endkey "for "descending=false", or when "startkey" is lower than "endkey" for "descending=true". In this scenario, Cloudant will return 400 Bad Request.

Design documents

 * Stricter validation of design documents. This should not cause problems with existing design documents, but malformed design documents will now fail to save.
 * Views written in an unsupported language now all respond with an "error" of "unknown_query_language". Previously, the response was a "reason" of "unknown_query_language".
 * When a null reducer is used to put a database design document, the system now responds with the error reason of "'(null)'", previously it returned "((new String("null")))".
 * "updates" must not have a null value, if specified in a design document.

Authentication

 * The "_session" meta data "authentication_handlers" now no longer contains ["delegated", "local"]

Misc

 * The _db_updates endpoint now returns a result set containing a key named "db_name". Previously it returned a result set with a key named "dbname".


Replication 

 * Replicator documents preserve the last error message in the "_replication_state_reason" JSON field. The field remains there even after replication is restarted and is in the 'triggered' state. This change helps the replicator code detect and so avoid writing the same error to the document repeatedly.

    

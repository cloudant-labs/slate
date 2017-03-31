---

copyright:
  years: 2017
lastupdated: "2017-02-23"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

# What's new in Cloudant

Keep up to date with the latest on Cloudant.
{:shortdesc} 

## Build 5638

-   Introduces new "stable" and "update" query parameters for views.
-   Replicator no longer retries forever if it cannot write checkpoints to the source database.

## Build 5421

-   Changes feeds support view-based filters.
-   Changes feeds support the `_doc_ids` filter.
-   `POST` requests are supported for `_changes`.
-   Both `_all_docs` and `_changes` support the `attachments=true` parameter.
-   Support for the CouchDB 1.6 `_users` database features, including server-side password hashing when creating documents in the `_users` database.
-   `/_bulk_get` endpoint to reduce the number of requests used in replication to mobile clients.
-   Design document metadata contains an `update pending` field.


### Breaking/behavior changes

Active tasks

-   Indexer entries in the `_active_tasks` response no longer report the `user` field.
-   Search indexer entries in the `_active_tasks` response no longer report the `user` field.

Views

-   Unicode normalization of key values is consistent between reduced and non-reduced view results. If raw collation is specified in a design document, result order might change as the result of this fix.
-   When you query a view or `_all_docs` database, it is an error to specify the `keys` parameter and any of the `key`, `startkey`, and `endkey` parameters.
-   It is an error to pass `startkey` and `endkey` parameters to a view if it is impossible for any row to match. For example, when the `startkey` parameter is higher than the `endkey` parameter for `descending=false`, or when the `startkey` parameter is lower than the `endkey` parameter for `descending=true`, Cloudant returns the `400 Bad Request` error.
-   When `dbcopy` is configured in a view document, it is automatically transformed to the `options` field in the design document. 

Design documents

-   Stricter validation of design documents. This should not cause problems with existing design documents, but malformed design documents will fail to save.
-   Views written in an unsupported language all respond with an `error` of `unknown_query_language`. Previously, the response was a `reason` of `unknown_query_language`.
-   When a null reducer is used to put a database design document, the system responds with the error reason of `'(null)'`, previously it returned `((new String("null")))`.
-   If `updates` is specified in a design document, it must not have a null value.

Authentication

-   The `_session` metadata `authentication_handlers` no longer contains `["delegated", "local"]`.

User documents

-   Validate structure of user documents in the `_users` database. Now, after a DBNext upgrade, the user documents must comply with ASF CouchdDB requirements,  http://docs.couchdb.org/en/1.6.1/intro/security.html#authentication-database. Previously, Cloudant did not validate user documents created in the `_users` database. 

Replication 

-   Replicator documents preserve the last error message in the `_replication_state_reason` JSON field. The field remains even after replication restarts and is in the `triggered` state. This change helps the replicator code detect and avoid writing the same error to the document repeatedly.
-   A replication error does not update the replication document unless the reason for the error changes. Previously, if a replication job crashed, it started an update process loop that generated shards almost 1TB in size.  

Result set

-   The `_db_updates` endpoint returns a result set containing a key named  `db_name`. Previously, it returned a result set with a key named `dbname`.
-   Set limits for the maximum length of the document ID, including setting the value `infinity` so the length is not checked. Previously, it was not possibly to define a maximum document ID length. 
    

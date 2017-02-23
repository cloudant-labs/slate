# What's new for Cloudant users

Read about new features available in Cloudant.

CouchDB 1.x supports the following features:

-   Changes feeds support view-based filters.
-   Changes feeds support the `_doc_ids` filter.
-   `POST` requests are supported for `_changes`.
-   Both `_all_docs` and `_changes` support the `attachments=true` parameter.
-   Support for the CouchDB 1.6 `_users` database features, including server-side password hashing when creating documents in the `_users` database.

CouchDB 2.x and Cloudant support the following features:

-   `/_bulk_get` endpoint to reduce the number of requests used in replication to mobile clients.
-   Design document metadata contains an `update pending` field.
-   Views support stable/update keywords.


# Breaking/behavior changes

Active tasks

-   Indexer entries in the `_active_tasks` response no longer report the `user` field.
-   Search indexer entries in the `_active_tasks` response no longer report the `user` field.

Views

-   Unicode normalization of key values is consistent between reduced and non-reduced view results. If raw collation is specified in a design document, result order might change as the result of this fix.
-   When you query a view or `_all_docs` database, it is an error to specify the `keys` parameter and any of the `key`, `startkey` and `endkey` parameters.
-   It is an error to pass `startkey` and `endkey` parameters to a view if it is impossible for any row to match. For example, when the `startkey` parameter is higher than the `endkey` parameter for `descending=false`, or when the `startkey` parameter is lower than the `endkey` parameter for `descending=true`, Cloudant returns the `400 Bad Request` error.

Design documents

-   Stricter validation of design documents. This should not cause problems with existing design documents, but malformed design documents will fail to save.
-   Views written in an unsupported language all respond with an `error` of `unknown_query_language`. Previously, the response was a `reason` of `unknown_query_language`.
-   When a null reducer is used to put a database design document, the system responds with the error reason of `'(null)'`, previously it returned `((new String("null")))`.
-   If `updates` is specified in a design document, it must not have a null value.

Authentication

-   The `_session` metadata `authentication_handlers` no longer contains `["delegated", "local"]`.


Replication 

-   Replicator documents preserve the last error message in the `_replication_state_reason` JSON field. The field remains even after replication restarts and is in the `triggered` state. This change helps the replicator code detect and avoid writing the same error to the document repeatedly.

Result set

-   The `_db_updates` endpoint returns a result set containing a key named  `db_name`. Previously, it returned a result set with a key named `dbname`.
    

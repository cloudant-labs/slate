---

copyright:
  years: 2017
lastupdated: "2017-06-16"

---

{:new_window: target="_blank"}
{:shortdesc: .shortdesc}
{:screen: .screen}
{:codeblock: .codeblock}
{:pre: .pre}

<!-- Acrolinx: 2017-05-04 -->

# What's new in Cloudant

Keep up to date with changes and updates for Cloudant.
{:shortdesc}

## Build 6069

- Previously, a replication job which crashed for some reason resulted in an update to the replication document,
  followed by a fresh attempt to start a new replication.
  Under some circumstances,
  this behavior could continue indefinitely: many duplicates of the same error message.
  A fix was introduced so that the replication document is not updated unless the reason for the error has changed.
- If the design document that is intended to specify a geospatial index is invalid,
  an attempt to retrieve information about the index by using
  the [`_geo_info` endpoint](../api/cloudant-geo.html#obtaining-information-about-a-cloudant-geo-index)
  results in an [HTTP `404`](http.html#404) response.

## Build 5834

- The maximum length of a document `id` is now 7168 characters (7k).

## Build 5728

- Cloudant is more tolerant of malformed user documents stored within the `_users` database.
  User documents should be structured and populated to comply with
  [Apache Software Foundation CouchDB requirements ![External link icon](../images/launch-glyph.svg "External link icon")](http://docs.couchdb.org/en/2.0.0/intro/security.html#users-documents){:new_window}.

## Build 5638

-   Introduces new "stable" and "update" query parameters for views.
-   Replicator no longer retries forever if it cannot write checkpoints to the source database.

## Build 5421

-	Changes feeds support view-based filters.
-	Changes feeds support the `_doc_ids` filter.
-	`POST` requests are supported for `_changes`.
-	Both `_all_docs` and `_changes` support the `attachments=true` parameter.
-	Support for the CouchDB 1.6 `_users` database features, including server-side hashing of passwords when documents are created in the `_users` database.
-	`/_bulk_get` endpoint to reduce the number of requests that are used in replication to mobile clients.
-	Design document metadata contains an `update pending` field.
-	Cloudant Query no longer returns an error if no valid index exists.

### Breaking/behavior changes

Active tasks

-   Indexer entries in the `_active_tasks` response no longer report the `user` field.
-   Search indexer entries in the `_active_tasks` response no longer report the `user` field.

Views

-   Unicode normalization of key values is consistent between reduced and non-reduced view results. If raw collation is specified in a design document, result order might change as the result of this fix.
-   When you query a view or `_all_docs` database, it is an error to specify the `keys` parameter and any of the `key`, `startkey`, and `endkey` parameters.
-   It is an error to pass `startkey` and `endkey` parameters to a view if it is impossible for any row to match. For example, when the `startkey` parameter is higher than the `endkey` parameter for `descending=false`, or when the `startkey` parameter is lower than the `endkey` parameter for `descending=true`, Cloudant returns the `400 Bad Request` error.
-   When `dbcopy` is configured in a view document, it is automatically transformed to the `options` field in a design document. 

Design documents

-   Stricter validation of design documents. This validation is not expected to cause problems with existing design documents, but malformed design documents fail to save.
-   Views that are written in an unsupported language all respond with an `error` of `unknown_query_language`. Previously, the response was a `reason` of `unknown_query_language`.
-   When a null reducer is used to put a database design document, the system responds with the error reason of `'(null)'`, previously it returned `((new String("null")))`.
-   If `updates` is specified in a design document, it must not have a null value.

Authentication

-   The `_session` metadata `authentication_handlers` no longer contains `["delegated", "local"]`.

User documents

-   Validate the structure of user documents created in the `_users` database. After the DBNext upgrade, the user documents must comply with ASF CouchdDB requirements. Previously, Cloudant did not validate the user documents' structure. 

Replication 

-   Replicator documents preserve the last error message in the `_replication_state_reason` JSON field. The field remains even after replication restarts and is in the `triggered` state. This change helps the replicator code detect and avoid writing the same error to the document repeatedly.
-   An error during replication does not update the replication document unless the reason for the error changes. Previously, when an error occurred during replication, an infinite loop started that generated sizable shards.  

Result set

-   The `_db_updates` endpoint returns a result set containing a key that is named  `db_name`. Previously, it returned a result set with a key named `dbname`.
-   Set the maximum length of the document ID. Previously, it was not possibly to define a maximum document ID length.

`dbcopy`

- The `dbcopy` feature can cause problems under some circumstances.
  Information about the feature has been removed from the documentation.
  Use of `dbcopy` is strongly discouraged.

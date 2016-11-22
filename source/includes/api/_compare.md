## Comparison of Cloudant and CouchDB API endpoints

This section provides a simple list of the Cloudant and CouchDB API endpoints,
showing you which endpoints are present in each service.

Endpoint |Method |Cloudant |CouchDB |Summary |Notes
---------|-------|---------|--------|--------|-----
/ | GET | Y | Y | Meta information about the cluster. |
/_active_tasks | GET | Y | Y | List running tasks. |
/_all_dbs | GET | Y | Y | List all the databases in the instance. |
/_api/v2/api_keys | POST | Y | | Generate an API key. |
/_api/v2/db/{db}/_security | GET | Y | | Who has permissions to read, write, and manage the database. |
/_api/v2/db/{db}/_security | PUT | Y | | Modify who has permissions to read, write, and manage a database. Assign an API key. |
/_api/v2/monitoring/{endpoint} | GET | Y | | Monitor a specific cluster aspect. |
/_api/v2/user/config/cors | GET | Y | | Current CORS configuration. |
/_api/v2/user/config/cors | PUT | Y | | Changes the CORS configuration. |
/_api/v2/user/virtual_hosts | GET | Y | | List all virtual hosts. |
/_api/v2/user/virtual_hosts | POST | Y | | Create a virtual host. |
/_api/v2/user/virtual_hosts | DELETE | Y | | Delete a virtual host. |
/_config | GET | | Y | Get the server configuration. |
/_config/{section} | GET | | Y | Get the configuration for the specified section. |
/_config/{section}/{key} | GET | | Y | Get the configuration value of a specific key within a configuration section. |
/_config/{section}/{key} | PUT | | Y | Update a configuration value. The new value should be supplied in the request body in the corresponding JSON format. |
/_config/{section}/{key} | DELETE | | Y | Delete a configuration value. |
/_db_updates | GET | Y | Y | List all database events in the instance. | In Cloudant the endpoint is only available to dedicated customers. Its documentation references additional query params (limit, since, descending) and an additional feed type value (normal) For CouchDB, its documentation references an additional feed type value (eventsource)
/_log | GET | | Y | Get the log. Equivalent to accessing the local log file of the corresponding instance. |
/_membership | GET | Y | Y | List the names of nodes in the cluster. Active clusters are indicated in the cluster_nodes field, while all_nodes has all nodes. |
/_replicate | POST | Y | Y | Request, configure, or stop, a replication operation. | Cloudant documentation references additional request body fields (selector, since_seq).
/_replicator | POST | Y | Y | Trigger a replication. | Cloudant documentation references additional request body fields (selector, since_seq).
/_replicator | PUT | Y | Y | Trigger a replication. | Cloudant documentation references additional request body fields (selector, since_seq).
/_replicator | DELETE | Y | Y | Cancel an ongoing replication | Cloudant documentation references additional request body fields (selector, since_seq).
/_restart | POST | | Y | Restart the instance. You must be authenticated as a user with administration privileges. |
/_search_analyze | POST | Y | | Test the results of analyzer tokenization by posting sample data. |
/_session | GET | Y | Y | Returns information about the authenticated user. | CouchDB documentation references an additional query param (basic).
/_session | POST | Y | Y | Initiate a new session for the specified user credentials. Cookie based user login. | CouchDB documentation references an additional query param (next).
/_session | DELETE | Y | Y | Closes user’s session. Logout cookie based user. |
/_stats | GET | | Y | Return the statistics for the running server. |
/_utils | GET | | Y | Access the built-in Fauxton administration interface. |
/_uuids | GET | Y | Y | Request one or more Universally Unique Identifiers (UUIDs). |
/favicon.ico | GET | | Y | Get the binary content for the favicon.ico site icon. |
/{db} | HEAD | | Y | Return the HTTP Headers containing a minimal amount of information about the specified database. |
/{db} | GET | Y | Y | Get information about the specified database. |
/{db} | POST | Y | Y | Create a new document in the specified database, using the supplied JSON document structure. |
/{db} | PUT | Y | Y | Create a new database. | Database names must start with a lowercase letter and contain only the following characters: Lowercase characters (a-z), Digits (0-9), Any of the characters _, $, (, ), +, -, and /
/{db} | DELETE | Y | Y | Delete the specified database, and all the documents and attachments contained within it. |
/{db}/_all_docs | GET | Y | Y | List all the documents in a database. | CouchDB documentation references additional query params (end_key, endkey_docid, end_key_doc_id, stale, start_key, startkey_docid, start_key_doc_id, update_seq).
/{db}/_all_docs | POST | Y | Y | List all the documents in a database. | CouchDB documentation references additional query params (end_key, endkey_docid, end_key_doc_id, stale, start_key, startkey_docid, start_key_doc_id, update_seq).
/{db}/_bulk_docs | POST | Y | Y | Create and update multiple documents at the same time within a single request. | CouchDB documentation references an additional request object field (new_edits).
/{db}/_bulk_get | POST | Y | Y | Get multiple documents in a single request. |
/{db}/_changes | GET | Y | Y | List of changes made to documents in the database, including insertions, updates, and deletions. | CouchDB includes query params (attachments, att_encoding_info, last-event-id, view).
/{db}/_changes | POST | Y | Y | List of changes made to documents in the database, including insertions, updates, and deletions. |
/{db}/_compact | POST | | Y | Request compaction of the specified database. |
/{db}/_compact/{ddoc} | POST | | Y | Compact the view indexes associated with the specified design document. |
/{db}/_design/{ddoc} | HEAD | Y | Y | Return the HTTP Headers containing a minimal amount of information about the specified design document. |
/{db}/_design/{ddoc} | GET | Y | Y | Get the contents of the design document specified with the name of the design document and from the specified database from the URL. |
/{db}/_design/{ddoc} | PUT | Y | Y | Create a new named design document or create a new revision of the existing design document. | Cloudant documentation references an additional request body field (indexes) CouchDB documentation references additional request body fields (language, options).
/{db}/_design/{ddoc} | DELETE | Y | Y | Delete the specified document from the database. |
/{db}/_design/{ddoc} | COPY | Y | Y | Copy an existing design document to a new or existing one. |
/{db}/_design/{ddoc}/_geo_info/{index} | GET | Y | | Obtain information about a geospatial index. |
/{db}/_design/{ddoc}/_geo/{index} | GET | Y | | Query a geo index. |
/{db}/_design/{ddoc}/_info | GET | Y | Y | Obtain information about the specified design document, including the index, index size, and current status of the design document. |
/{db}/_design/{ddoc}/_list/{func}/{other-ddoc}/{view} | GET | Y | Y | Apply the list function for the view function from the other design document. |
/{db}/_design/{ddoc}/_list/{func}/{other-ddoc}/{view} | POST | Y | Y | Apply the list function for the view function from the other design document. |
/{db}/_design/{ddoc}/_list/{func}/{view} | GET | Y | Y | Apply the list function for the view function from the same design document. | The result of a list function is not stored. This means that the function is executed every time a request is made.
/{db}/_design/{ddoc}/_list/{func}/{view} | POST | Y | Y | Apply the list function for the view function from the same design document. |
/{db}/_design/{ddoc}/_rewrite/{path} | ANY | Y | Y | Rewrite the specified path by rules defined in the specified design document. |
/{db}/_design/{ddoc}/_search_info/{index} | GET | Y | | Obtain information about a search specified within a given design document. |
/{db}/_design/{ddoc}/_search/{index} | GET | Y | | Query an index. |
/{db}/_design/{ddoc}/_search/{index} | POST | Y | | Query an index. |
/{db}/_design/{ddoc}/_show/{func} | GET | Y | Y | Apply the show function for null document. |
/{db}/_design/{ddoc}/_show/{func} | POST | Y | Y | Apply the show function for null document. |
/{db}/_design/{ddoc}/_show/{func}/{docid} | GET | Y | Y | Apply the show function for the specified document. | The result of a show function is not stored. This means that the function is executed every time a request is made.
/{db}/_design/{ddoc}/_show/{func}/{docid} | POST | Y | Y | Apply the show function for the specified document. |
/{db}/_design/{ddoc}/_update/{func} | POST | Y | Y | Execute the update function on server side for null document. |
/{db}/_design/{ddoc}/_update/{func}/{docid} | PUT | Y | Y | Execute the update function on server side for the specified document. |
/{db}/_design/{ddoc}/_view/{view} | GET | Y | Y | Execute the view function from the specified design document. | CouchDB documentation references additional query params (conflicts, end_key, end_key_doc_id, attachments, att_encoding_info, sorted, start_key, start_key_doc_id, update_seq).
/{db}/_design/{ddoc}/_view/{view} | POST | Y | Y | Execute the view function from the specified design document. | CouchDB documentation references additional query params (conflicts, end_key, end_key_doc_id, attachments, att_encoding_info, sorted, start_key, start_key_doc_id, update_seq).
/{db}/_design/{ddoc}/{attname} | HEAD | Y | Y | Return the HTTP headers containing a minimal amount of information about the specified attachment. |
/{db}/_design/{ddoc}/{attname} | GET | Y | Y | Return the file attachment associated with the design document. |
/{db}/_design/{ddoc}/{attname} | PUT | Y | Y | Upload the supplied content as an attachment to the specified design document. |
/{db}/_design/{ddoc}/{attname} | DELETE | Y | Y | Delete the attachment of the specified design document. |
/{db}/_ensure_full_commit | POST | Y | Y | Commit any recent changes to the specified database to disk. |
/{db}/_explain | POST | Y | Y | Identify which index is being used by a particular query. |
/{db}/_find | POST | Y | Y | Find documents using a declarative JSON querying syntax. | Cloudant documentation references additional request body fields (r, bookmark)
/{db}/_index | GET | Y | Y | List indexes. |
/{db}/_index | POST | Y | Y | Create a new index. |
/{db}/_index/_design/{ddoc}/{type}/{name} | DELETE | Y | Y | Delete an index. |
/{db}/_local/{docid} | GET | Y | Y | Get the specified local document. |
/{db}/_local/{docid} | PUT | Y | Y | Store the specified local document. | Local documents are not replicated to other databases.
/{db}/_local/{docid} | DELETE | Y | Y | Delete the specified local document. |
/{db}/_local/{docid} | COPY | Y | Y | Copy the specified local document. |
/{db}/_missing_revs | GET | Y | | Return the document revisions from the given list that do not exist in the database. |
/{db}/_missing_revs | POST | Y | Y | Return the document revisions from the given list that do not exist in the database. |
/{db}/_purge | POST | | Y | Remove the references to deleted documents from the database. |
/{db}/_revs_diff | POST | Y | Y | Given a set of document/revision IDs, return the subset of those that do not correspond to revisions stored in the database. |
/{db}/_revs_limit | GET | Y | Y | Get the number of document revisions tracked. |
/{db}/_revs_limit | PUT | Y | Y | Set the maximum number of document revisions tracked. |
/{db}/_security | GET | Y | Y | Return the current security object from the specified database. |
/{db}/_security | PUT | Y | Y | Set the security object for the given database. |
/{db}/_shards | GET | Y | | Return information about the shards in the cluster |
/{db}/_view_cleanup | POST | | Y | Remove view index files that are no longer required by as a result of changed views within design documents. |
/{db}/{docid} | HEAD | Y | Y | Return the HTTP Headers containing a minimal amount of information about the specified document. |
/{db}/{docid} | GET | Y | Y | Return the document specified by the docid from the specified db. |
/{db}/{docid} | PUT | Y | Y | Create a new named document or create a new revision of the existing document. |
/{db}/{docid} | DELETE | Y | Y | Mark the specified document as deleted. |
/{db}/{docid} | COPY | Y | Y | Copy an existing document to a new or existing document. |
/{db}/{docid}/{attname} | HEAD | Y | Y | Return the HTTP headers containing a minimal amount of information about the specified attachment. |
/{db}/{docid}/{attname} | GET | Y | Y | Return the file attachment associated with the document. |
/{db}/{docid}/{attname} | PUT | Y | Y | Upload the supplied content as an attachment to the specified document. |
/{db}/{docid}/{attname} | DELETE | Y | Y | Delete the attachment attachment of the specified doc. |

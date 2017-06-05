## Errors

The Cloudant API uses the following error codes:

Error Code | Meaning
---------- | -------
200 | OK -- Request completed successfully.
201 | Created -- Resource created successfully.
202 | Accepted -- Request has been accepted, but the corresponding operation may not have completed. This is used for background operations, such as [database compaction](#document-versioning-and-mvcc) or for bulk operations where some updates might have led to a conflict.
304 | Not Modified -- The content requested has not been modified. This is used with the ETag system to identify the version of information returned.
400 | Bad Request -- Bad request structure. The error can indicate an error with the request URL, path or headers. Differences in the supplied MD5 hash and content also trigger this error, as this may indicate message corruption.
401 | Unauthorized -- The item requested was not available using the supplied authorization, or authorization was not supplied.
403 | Forbidden -- The requested item or operation is forbidden.
404 | Not Found -- The requested resource could not be found. The content will include further information, as a JSON object, if available. The structure will contain two keys, error and reason. For example: `{"error":"not_found","reason":"no_db_file"}`
405 | Resource Not Allowed -- A request was made using an invalid HTTP request type for the URL requested. For example, you have requested a PUT when a POST is required. Errors of this type can also be triggered by invalid URL strings.
406 | Not Acceptable -- The requested content type is not supported by the server.
409 | Conflict -- Request resulted in an update conflict.
412 | Precondition Failed -- The request headers from the client and the capabilities of the server do not match.
415 | Bad Content Type -- The content types supported, and the content type of the information being requested or submitted indicate that the content type is not supported.
416 | Requested Range Not Satisfiable -- The range specified in the request header cannot be satisfied by the server.
417 | Expectation Failed -- When sending documents in bulk, the bulk load operation failed.
500 | Internal Server Error -- The request was invalid, either because the supplied JSON was invalid, or invalid information was supplied as part of the request.

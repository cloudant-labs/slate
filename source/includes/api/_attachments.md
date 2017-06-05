## Attachments

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/index.html">here</a>,
and the Attachments topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/api/attachments.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

If you want to store data, use attachments.
Attachments are Binary Large Object ([BLOb](http://en.wikipedia.org/wiki/Binary_large_object)) files contained within documents.
The BLOb is stored in the `_attachments` component of the document.
The BLOb includes data about the attachment name, the type of the attachment, and the actual content.
Examples of BLObs would be images and multimedia.

<aside class="warning" role="complementary" aria-label="usebase64">If you include the attachment as an '[inline](#inline)' component of the overall JSON,
the attachment content should be represented using BASE64 form.</aside>

The content type corresponds to a [MIME type][mime].
For example, if you want to attach a `.jpg` image file to a document,
you specify the attachment MIME type as `image/jpeg`.

<aside class="warning" role="complementary" aria-label="keepattachmentssmall">As a best practice, keep attachments small in size and number because attachments can impact performance.</aside>

### Create / Update

> Example instruction for creating or updating an attachment:

```http
PUT /$DATABASE/$DOCUMENT_ID/$ATTACHMENT?rev=$REV HTTP/1.1
Content-Type: $$ATTACHMENT_MIME_TYPE
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID/$ATTACHMENT?rev=$REV \
     -X PUT \
     -H "Content-Type: $ATTACHMENT_MIME_TYPE" \
     --data-binary @$ATTACHMENT_FILEPATH
```

```javascript
var nano = require('nano');
var fs = require('fs');
var account = nano("https://$ACCOUNT.cloudant.com");
var db = account.use($DATABASE);

fs.readFile($FILEPATH, function (err, data) {
  if (!err) {
    db.attachment.insert($DOCUMENT_ID, $ATTACHMENT, data, $ATTACHMENT_MIME_TYPE, {
      rev: $REV
    }, function (err, body) {
      if (!err)
        console.log(body);
    });
  }
});
```

To create a new attachment at the same time as creating a new document,
include the attachment as an '[inline](#inline)' component of the JSON content.

To create a new attachment on an existing document,
or to update an attachment on a document,
make a PUT request with the document's latest `_rev` to `https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID/$ATTACHMENT`.
The attachment's [content type][mime] must be specified using the `Content-Type` header.
The `$ATTACHMENT` value is the name by which the attachment is associated with the document.

<aside class="information" role="complementary" aria-label="attachmentsmustbeunique">You can create more than one attachment for a document;
simply ensure that the `$ATTACHMENT` value for each attachment is unique within the document.</aside>

<div></div>

> Example response:

```json
{
  "id" : "FishStew",
  "ok" : true,
  "rev" : "9-247bb19a41bfd9bfdaf5ee6e2e05be74"
}
```

The response contains the document ID and the new document revision. Note that attachments do not have their own revisions. Instead, updating or creating an attachment changes the revision of the document it is attached to.

### Read

> Example instruction for reading an attachment:

```http
GET /$DATABASE/<documenat_id>/<attachment http>/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID/$ATTACHMENT \
     -u $ACCOUNT >blob_content.dat
# store the response content into a file for further processing.
```

```javascript
var nano = require('nano');
var account = nano("https://$ACCOUNT.cloudant.com");
var db = account.use($DATABASE);

db.attachment.get($DOCUMENT_ID, $FILENAME, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

To retrieve an attachment,
make a GET request to `https://$ACCOUNT.cloudant.com/$DATABASE/$document_id/$attachment/`.
The body of the response is the raw content of the attachment.

### Delete

> Example instruction for deleting an attachment:

```http
DELETE /$DATABASE/$DOCUMENT_ID/$ATTACHMENT?rev=<rev HTTP>/1.1
```

```shell
curl https://$ACCOUNT.cloudant.com/$DATABASE/$DOCUMENT_ID/$ATTACHMENT?rev=$REV \
     -X DELETE
```

```javascript
var nano = require('nano');
var account = nano("https://$ACCOUNT.cloudant.com");
var db = account.use($DATABASE);

db.attachment.destroy($DOCUMENT_ID, $FILENAME, $REV, function (err, body) {
  if (!err) {
    console.log(body);
  }
});
```

To delete an attachment, make a DELETE request with the document's latest `_rev` to `https://$ACCOUNT.cloudant.com/$DOCUMENT_ID/$ATTACHMENT`.
If you do not supply the latest `_rev`,
the response is a [409 error](basics.html#http-status-codes).

<div></div>

> Example response:

```json
{
  "ok": true,
  "id": "DocID",
  "rev": "3-aedfb06537c1d77a087eb295571f7fc9"
}
```

If the deletion is successful, the response contains `"ok": true`, and the ID and new revision of the document.

### Inline

> Example JSON content that includes an inline attachment of a jpeg image:

```json
{
  "_id":"document_with_attachment",
  "_attachments":
  {
    "name_of_attachment":
    {
      "content_type":"image/jpeg",
      "data": "iVBORw0KGgoAA... ...AASUVORK5CYII="
    }
  }
}
```

Inline attachments are attachments included as part of the JSON content.
The content must be provided using BASE64 representation,
as shown in the example.

[mime]: http://en.wikipedia.org/wiki/Internet_media_type#List_of_common_media_types

### Performance considerations

While document attachments are very useful,
they do have implications for application performance.
In particular,
having a large number of attachments can have an adverse performance impact during replication.

For example, if your application requires lots of images to be stored as attachments,
or has large images, a better approach would be to use an alternative BLOb storage mechanism for the images, with the image metadata (such as URLs) in Cloudant.

You might find it helpful to carry out performance testing for your specific application to determine which approach works best for your circumstances.  
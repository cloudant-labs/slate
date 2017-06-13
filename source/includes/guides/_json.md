## JSON

<table border='1'>
<tr>
<td><b>Important:</b> All Cloudant documentation has moved to the IBM Bluemix platform.
You can find the new content
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/getting-started.html">here</a>,
and the JSON topic in particular
<a href="https://console.ng.bluemix.net/docs/services/Cloudant/guides/json.html">here</a>.
<br/><br/>
<p>Content on this page will no longer be updated (Jan 31st, 2017).</p>
</td>
</tr>
</table>

The majority of requests and responses to and from Cloudant use the JavaScript Object Notation (JSON) for formatting the content and structure of the data and responses.

JSON is used because it is the simplest and easiest solution for working with data using a web browser.
This is because JSON structures can be evaluated and used as JavaScript objects within the web browser environment. JSON also integrates with the server-side JavaScript used within Cloudant. JSON documents are always UTF-8 encoded.

<aside class="warning" role="complementary" aria-label="takecare">Care should be taken to ensure that:

-  Your JSON structures are valid. Invalid structures cause Cloudant to return an HTTP status code of [400 (bad request)](http.html#400).
-  You normalize strings in JSON documents retrieved from Cloudant, before you compare them. This is because Unicode normalization might have been applied, so that a string stored and then retrieved is not identical on a binary level.

</aside>

JSON supports the same basic types as supported by JavaScript:

- [Numbers](#numbers)
- [Strings](#strings)
- [Booleans](#booleans)
- [Arrays](#arrays)
- [Objects](#objects)

### Numbers

> numbers

```json
123
```

Numbers can be integer or floating point values.

### Strings

> strings

```json
"A String"
```

String should be enclosed by double-quotes. Strings support Unicode characters and backslash escaping.

### Booleans

> booleans

```json
{ "value": true}
```

A `true` or `false` value.

### Arrays

> arrays

```json
["one", 2, "three", [], true, {"foo": "bar"}]
```

A list of values enclosed in brackets. The values enclosed can be any valid JSON.


### Objects

> objects

```json
{
   "servings" : 4,
   "subtitle" : "Easy to make in advance, and then cook when ready",
   "cooktime" : 60,
   "title" : "Chicken Coriander"
}
```

A set of key/value pairs, such as an associative array, or hash. The key must be a string, but the value can be any of the supported JSON values.

In Cloudant databases, the JSON object is used to represent a variety of structures, including all documents in a database.

Parsing JSON into a JavaScript object is supported through the `JSON.parse()` function in JavaScript, or through various [libraries](libraries.html#-client-libraries) that perform the parsing of the content into a JavaScript object for you. [Libraries](libraries.html#-client-libraries) for parsing and generating JSON are available for many major programming languages.


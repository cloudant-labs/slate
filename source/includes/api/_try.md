<script type="text/javascript">
  $(document).ready(function() {
    var outputField = $("#output-marker").next();
    var httpRequestField = $("#request-http-marker").next();
    var curlRequestField = $("#request-curl-marker").next();
    var highlight = function(elem) {
      elem.each(function(i, block) {
        hljs.highlightBlock(block);
      });
    };
    var requestTypes = {
      analyzers: {
        queries: {
          'email-address': {query: '{\n  "analyzer": "email",\n  "text":"Jane\'s email address is jane.smith@example.com."\n}'},
          'english': {query: '{\n  "analyzer": "english",\n  "text":"Peter Piper picked a peck of pickled peppers. A peck of pickled peppers Peter Piper picked. If Peter Piper picked a peck of pickled peppers. Where’s the peck of pickled peppers Peter Piper picked?"\n}'},
          'german': {query: '{\n  "analyzer": "german",\n  "text":"Fischers Fritz fischt frische Fische, frische Fische fischt Fischers Fritz."\n}'},
          'default': 'email-address',
          'keyword': {query: '{\n  "analyzer":"keyword",\n  "text":"ablanks@renovations.com"\n}' },
          'standard': {query: '{\n  "analyzer":"standard",\n  "text":"ablanks@renovations.com"\n}' },
          'whitespace': {query: '{\n  "analyzer":"whitespace",\n  "text":"Jane\'s email address is jane.smith@example.com."\n}' }
        },
        form: $('form.analyzers'),
        queryInput: $('form.analyzers .query'),
        renderHttpRequest: function() {
          return 'POST /_search_analyze HTTP/1.1\nHost: examples.cloudant.com\nContent-Type: application/json\n\n' + this.queryInput.val();
        },
        renderCurlRequest: function() {
          return "curl 'https://examples.cloudant.com/_search_analyze' -H 'Content-Type: application/json' -X POST -d '" + this.queryInput.val() + "'";
        },
        submitForm: function(event) {
          var query = this.queryInput.val();
          jQuery.ajax({
            url: 'https://examples.cloudant.com/_search_analyze',
            type: 'POST',
            data: query,
            beforeSend: function(xhr) {
              xhr.setRequestHeader("Content-Type", "application/json");
              xhr.setRequestHeader("Authorization", "Basic " + btoa('thereencespedgetytolisir:c1IimpBSAC3b3A66N8LHKwKF'));
            },
            error: function(one, two) {},
            complete: displayResult
          });
          event.preventDefault();
        }
      },
      search: {
        queryInput: $('form.search #test-search-query'),
        countsInput: $('form.search #search-counts'),
        drilldownInput: $('form.search #search-drilldown'),
        groupFieldInput: $('form.search #search-group-field'),
        groupLimitInput: $('form.search #search-group-limit'),
        groupSortInput: $('form.search #search-group-sort'),
        includeDocsInput: $('form.search #search-include-docs'),
        limitInput: $('form.search #search-limit'),
        rangesInput: $('form.search #search-ranges'),
        sortInput: $('form.search #search-sort'),
        form: $('form.search'),
        queries: {
          'author-is-john': { query: 'author:John' },
          'sorting': { query: 'author:J*', sort: '"-year"' },
          'default': 'author-is-john',
          'drilldown': { query: 'year:[2000 TO 2010]', drilldown: '["author","J. K. Rowling"]' },
          'counts': { query: 'year:[2000 TO 2010]', counts: '["author"]', limit: 0 },
          'ranges': { query: 'author:J*', ranges: '{"year":{"21st century":"[2000 TO 2099]","20th century":"[1900 TO 1999]"}}', limit: 0 },
        },
        buildUrl: function() {
          var url = '/docs-examples/_design/ddoc/_search/books?q=' + this.queryInput.val();
          var counts = this.countsInput.val();
          if (counts != '') {
            url += '&counts=' + encodeURIComponent(counts);
          }
          var drilldown = this.drilldownInput.val();
          if (drilldown != '') {
            url += '&drilldown=' + encodeURIComponent(drilldown);
          }
          var groupField = this.groupFieldInput.val();
          if (groupField != '') {
            url += '&group_field=' + encodeURIComponent(groupField);
          }
          var groupLimit = this.groupLimitInput.val();
          if (groupLimit != '') {
            url += '&group_limit=' + encodeURIComponent(groupLimit);
          }
          var groupSort = this.groupSortInput.val();
          if (groupSort != '') {
            url += '&group_sort=' + encodeURIComponent(groupSort);
          }
          var limit = this.limitInput.val();
          if (limit != '') {
            url += '&limit=' + encodeURIComponent(limit);
          }
          var ranges = this.rangesInput.val();
          if (ranges != '') {
            url += '&ranges=' + encodeURIComponent(ranges);
          }
          var sort = this.sortInput.val();
          if (sort != '') {
            url += '&sort=' + encodeURIComponent(sort);
          }
          var includeDocs = this.includeDocsInput.is(':checked');
          if (includeDocs) {
            url += '&include_docs=' + encodeURIComponent(includeDocs);
          }
          return url;
        },
        renderHttpRequest: function() {
          return 'GET ' + this.buildUrl() + ' HTTP/1.1';
        },
        renderCurlRequest: function() {
          return 'curl "https://examples.cloudant.com' + this.buildUrl() + '"';
        },
        doAjaxRequest: function() {

        },
        submitForm: function(event) {
          var query = this.queryInput.val();
          var url = 'https://examples.cloudant.com' + this.buildUrl();
          jQuery.ajax({
            url: url,
            type: 'GET',
            beforeSend: function(xhr) {
              xhr.setRequestHeader("Authorization", "Basic " + btoa('thereencespedgetytolisir:c1IimpBSAC3b3A66N8LHKwKF'));
            },
            error: function(one, two) {},
            complete: displayResult
          });
          event.preventDefault();
        }
      },
      cq: {
        queryInput: $('form.cq .query'),
        form: $('form.cq'),
        queries: {
          'actor-is-zoe-saldana': {query: '{\n  "selector": {\n    "cast": {\n      "$in": ["Zoe Saldana"]\n    }\n  },\n  "limit": 10\n}'},
          'sorting': {query: '{\n  "selector": {\n    "year": {\n      "$gte": 2000,\n      "$lte": 2001\n    }\n  },\n  "limit": 10,\n  "sort": ["year"]\n}'},
          'pg2010': {query: '{\n  "selector": {\n    "year": 2010,\n    "rating": {\n      "$in": ["PG", "PG-13"]\n    }\n  }\n}'},
          'year2010ascending': { query: '{\n  "selector": {\n    "year": {\n      "$gt": 2010\n    }\n  },\n  "fields": ["_id", "_rev", "year", "title"],\n  "sort": [{"year": "asc"}],\n  "limit": 10,\n  "skip": 0\n}' },
          'simple': { query: '{\n  "selector": {\n    "director": "Lars von Trier"\n  }\n}' },
          'bond': { query: '{\n  "selector": {\n    "$text": "Bond"\n  }\n}' },
          'bond-title-cast': { query: '{\n  "selector": {\n    "$text": "Bond"\n  },\n  "fields": [\n    "title",\n    "cast"\n  ]\n}' },
          'trier2003': { query: '{\n  "selector": {\n    "director": "Lars von Trier",\n    "year": 2003\n  }\n}' },
          'imdb-rating-8': { query: '{\n  "selector": {\n    "imdb": {\n      "rating": 8\n    }\n  }\n}' },
          'after2010': { query: '{\n  "selector": {\n    "year": {\n      "$gt": 2010\n    }\n  }\n}' },
          '2010-by-title': { query: '{\n  "selector": {\n    "year": {\n      "$eq": 2001\n    }\n  },\n  "sort": [\n    "title:string"\n  ],\n  "fields": [\n    "title"\n  ]\n}' },
          'schwarzenegger': { query: '{\n  "selector": {\n    "$and": [\n      {\n        "$text": "Schwarzenegger"\n      },\n      {\n        "year": {\n          "$in": [1984, 1991]\n        }\n      }\n    ]\n  },\n  "fields": [\n    "year",\n    "title",\n    "cast"\n  ]\n}' },
          'default': 'actor-is-zoe-saldana'
        },
        renderHttpRequest: function() {
          return 'POST /query-movies-with-indexes/_find HTTP/1.1\nHost: examples.cloudant.com\n\n' + this.queryInput.val();
        },
        renderCurlRequest: function() {
          return "curl 'https://examples.cloudant.com/query-movies-with-indexes/_find' -X POST -d '" + this.queryInput.val() + "'";
        },
        submitForm: function(event){
          var query = this.queryInput.val();
          jQuery.ajax({
            url: 'https://examples.cloudant.com/query-movies-with-indexes/_find',
            type: 'POST',
            data: query,
            beforeSend: function(xhr) {
              xhr.setRequestHeader("Authorization", "Basic " + btoa('thereencespedgetytolisir:c1IimpBSAC3b3A66N8LHKwKF'));
            },
            error: function(one, two) {},
            complete: displayResult
          });
          event.preventDefault();
        }

      }
    };
    var saveFormState = function() {
      var requestType = requestTypeSelect.val();
      var predefinedQuery = $('form.' + requestType + ' .predefined').val();
      window.location.hash = '#requestType=' + requestType + '&predefinedQuery=' + predefinedQuery;
    };
    var displayResult = function(jqXHR, textStatus) {
      var result = JSON.stringify(jQuery.parseJSON(jqXHR.responseText), null, '    ');
      outputField.show();
      outputField.text(result);
      highlight(outputField);
    }

    for (var rt in requestTypes) {
      requestTypes[rt].form.submit(requestTypes[rt].submitForm);
    }

    var requestChanged = function(formName) {
      httpRequestField.text(requestTypes[formName].renderHttpRequest());
      highlight(httpRequestField);
      curlRequestField.text(requestTypes[formName].renderCurlRequest());
      highlight(curlRequestField);
      requestTypes[formName].submitForm({preventDefault:function(){}});
    }

    var requestTypeSelect = $('div.test-form-container select.request-type');
    var showSelectedType = function() {
      for (var requestType in requestTypes) {
        requestTypes[requestType].form.hide();
      }
      var type = requestTypeSelect.val();
      requestTypes[type].form.show();
    };
    requestTypeSelect.on("change", showSelectedType);
    requestTypeSelect.on("change", saveFormState);
    requestTypeSelect.on("change", function() {
      var rt = requestTypeSelect.val();
      var defaultQuery = requestTypes[rt].queries['default']
      initForm(rt, requestTypes[rt].queries[defaultQuery]);
      requestChanged(rt);
    });

    var initForm = function(formName, request) {
      $('form.' + formName + ' input[type=text]').val('');
      for (var field in request) {
        $('form.' + formName + ' .' + field).val(request[field]);
      }
    };
    var initPredefinedSelect = function(formName) {
      var predefinedSelect = $('form.' + formName + ' select.predefined');
      predefinedSelect.on('change', function() {
        var request = predefinedSelect.val();
        initForm(formName, requestTypes[formName].queries[request]);
        requestChanged(formName);
        saveFormState();
      });
    };
    for (var rt in requestTypes) {
      initPredefinedSelect(rt);
      initForm(rt, requestTypes[rt].queries['default']);
    }
    requestTypes.search.includeDocsInput.on('change', function() {requestChanged('search');});
    for (var rt in requestTypes) {
      var createFunc = function(rtp) { return function(){requestChanged(rtp)}}
      requestTypes[rt].form.on('keyup', $.debounce(createFunc(rt), 300));
    }
    //init form from query param values
    function getParameterByName(name) {
      name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
      var regex = new RegExp("[\\#&]" + name + "=([^&#]*)"), results = regex.exec(window.location.hash);
      return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
    var requestType = getParameterByName('requestType');
    if (!requestType) { requestType = 'search'; }
    var predefinedQuery = getParameterByName('predefinedQuery');
    if (!predefinedQuery) { predefinedQuery = requestTypes[requestType].queries['default']; }
    requestTypeSelect.val(requestType);
    $('form.' + requestType + ' .predefined').val(predefinedQuery);
    showSelectedType();
    initForm(requestType, requestTypes[requestType].queries[predefinedQuery]);
    requestChanged(requestType);
    $("#lang-selector a").unbind("click");
    $("#lang-selector a").bind("click", function(event) {
      var language = $(this).data("language-name");
      activateLanguage(language);
      event.preventDefault();
    });

  });
</script>

## Try it!

> Request

<p id="request-http-marker"></p>

```http
GET /examples/_design/ddoc/_search/books?q=author:John HTTP/1.1
```

<p id="request-curl-marker"></p>

```shell
curl https://$ACCOUNT.cloudant.com/examples/_design/ddoc/_search/books?q=author:John
```

> Response

<p id="output-marker"></p>

```json
{
  "total_rows": 1,
  "bookmark": "g2wAAAABaANkACFkYmNvcmVAZGIxMS5tZXJpdGFnZS5jbG91ZGFudC5uZXRsAAAAAm4EAAAAAIBuBAD___-_amgCRkACik3gAAAAYRtq",
  "rows": [
    {
      "id": "book91",
      "order": [
        2.3175313472747803,
        27
      ],
      "fields": {
        "author": "John Steinbeck",
        "title_English": "The Grapes of Wrath"
      }
    }
  ]
}
```

You can try out requests and obtain output results in the code column. We have put together some sample data so that you can experiment with Cloudant straight away.

<div class="test-form-container">

  <label for="request-type">Type of request</label>
  <select id="request-type" name="request-type" class="request-type">
    <option selected="selected" value="search">Search</option>
    <option value="analyzers">Search analyzers</option>
    <option value="cq">Cloudant Query</option>
  </select>
  <br>
  <form action="#" class="search">
    <label for="predefined">Predefined queries</label>
    <select id="predefined" name="predefined" class="predefined">
      <option selected="selected" value="author-is-john">Books written by John</option>
      <option value="sorting">Sorting by year</option>
      <option value="ranges">Year ranges</option>
      <option value="counts">Count authors</option>
      <option value="drilldown">Drilldown</option>
    </select>
    <label for="test-search-query">Search query (q)</label>
    <input size="100" type="text" name="query" class="query" id="test-search-query">
    <label for="search-counts">Counts</label>
    <input size="100" type="text" name="counts" class="counts" id="search-counts">
    <label for="search-drilldown">Drilldown</label>
    <input size="100" type="text" name="drilldown" class="drilldown" id="search-drilldown">
    <label for="search-group-field">Group field</label>
    <input size="100" type="text" name="groupfield" class="groupField" id="search-group-field">
    <label for="search-group-limit">Group limit</label>
    <input size="100" type="text" name="group-limit" class="groupLimit" id="search-group-limit">
    <label for="search-group-sort">Group sort</label>
    <input size="100" type="text" name="group-sort" class="groupSort" id="search-group-sort">
    <label for="search-limit">Limit</label>
    <input size="100" type="text" name="limit" class="limit" id="search-limit">
    <label for="search-ranges">Ranges</label>
    <input size="100" type="text" name="ranges" class="ranges" id="search-ranges">
    <label for="search-sort">Sort</label>
    <input size="100" type="text" name="sort" class="sort" id="search-sort">

    <input type="checkbox" name="include-docs" class="includeDocs" id="search-include-docs">
    <label style="margin-left: 0px;display: inline" for="search-include-docs">Include docs</label>
  </form>

  <form action="#" class="cq">
    <label for="predefined2">Predefined queries</label>
    <select name="predefined2" id="predefined2" class="predefined">
      <option selected="selected" value="actor-is-zoe-saldana">Movies with Zoe Saldana</option>
      <option value="sorting">Query with sorting</option>
      <option value="pg2010">2010 Movies rated PG or PG-13</option>
      <option value="year2010ascending">Movies released after 2010 sorted by year</option>
      <option value="simple">Simple selector</option>
      <option value="bond">Find the word Bond anywhere</option>
      <option value="bond-title-cast">Find Bond anywhere, only return title and cast</option>
      <option value="trier2003">Movies directed by Lars von Trier and released in 2003</option>
      <option value="imdb-rating-8">Movies rated 8 on IMDB</option>
      <option value="after2010">Movies released after 2010</option>
      <option value="2010-by-title">2010 movies sorted by title</option>
      <option value="schwarzenegger">Schwarzenegger movies</option>

    </select>
    <label for="requestBody">RequestBody</label>
    <textarea rows="10" class="query" cols="80" id="requestBody"></textarea><br /><br />
    <p style="margin-left: 40px;">The sample database contains 9,000 movie documents in the following format:</p>

    <code style="white-space: pre; color: black; background-color: inherit; display: block; margin-left: 40px;">
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
    </code>
  </form>

  <form action="#" class="analyzers">
    <label for="predefined3">Predefined queries</label>
    <select id="predefined3" name="predefined3" class="predefined">
      <option selected="selected" value="email-address">Email address analyzer</option>
      <option value="english">English analyzer</option>
      <option value="german">German analyzer</option>
      <option value="keyword">Keyword analyzer</option>
      <option value="standard">Standard analyzer</option>
      <option value="whitespace">Whitespace analyzer</option>
    </select>
    <label for="analyzersRequestBody">AnalyzersRequestBody</label>
    <textarea rows="10" class="query" cols="80" id="analyzersRequestBody"></textarea><br /><br />
  </form>

</div>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

<style type="text/css">
  .test-form-container textarea {

  }
  div.test-form-container {
    clear:none;
  }
  div.test-form-container * {
    margin: 0;
    padding: 0;
  }
  .test-form-container textarea, div.test-form-container input[type=text], div.test-form-container select, div.test-form-container label {
    margin-left: 40px;
    display: block;
  }
  .test-form-container textarea, div.test-form-container input[type=text], div.test-form-container select {
    margin-bottom: 12px;
    width: 40%;
    height: 24px;
  }
  .test-form-container textarea {
    height: 300px;
    font-family: monospace;
  }
  .test-form-container form {
    display: none;
  }
  .test-form-container form.search {
    display: block;
  }

  .test-form-container input[type=text] {
    padding-left: 5px;
  }

  .test-form-container input[type=checkbox] {
    display: inline;
    margin-left: 40px;
    width: 20px;
  }
  pre span.hljs-string {
    color: #00a69f;
  }
  pre span.hljs-number {
    color: #90a959;
  }
  pre.hljs span.hljs-title {
    color: #fff;
  }
  #hideCodeButton {
    display: none;
  }



</style>

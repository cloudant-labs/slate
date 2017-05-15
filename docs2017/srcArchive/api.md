---
title: Cloudant Documentation - API reference

language_tabs:
  - http 
  - shell: curl
#  - javascript: node.js
#  - python

toc_footers:
  - <a href="https://cloudant.com/">Cloudant</a>
  - <a href="https://cloudant.com/sign-up/">Sign up</a> / <a href="https://cloudant.com/sign-in/">Sign in</a>
  - <a href="http://stackoverflow.com/questions/tagged/cloudant">Cloudant on StackOverflow</a>
  - <a href='http://github.com/tripit/slate'>Documentation Powered by Slate</a>
  - <a href="https://github.com/cloudant-labs/slate">Documentation Source</a>

includes:
  - api/index

---

<script>
fragments = {
  '#http': 'http.html',
  '#account': 'account.html',
  '#authentication': 'authentication.html',
  '#authorization': 'authorization.html',
  '#cors': 'cors.html',
  '#databases': 'databases.html',
  '#documents': 'document.html',
  '#attachments': 'attachments.html',
  '#query': 'cloudant_query.html',
  '#design-documents': 'design_documents.html',
  '#creating-views': 'creating_views.html',
  '#using-views': 'using_views.html',
  '#search': 'search.html',
  '#cloudant-geospatial': 'geo.html',
  '#405': 'http.html#405',
  '#replicationAPI': 'replication.html',
  '#400': 'http.html#400',
  '#404': 'http.html#404',
  '#409': 'http.html#409',
  '#503': 'http.html#503',
  '#304': 'http.html#304',
  '#misc': 'active_tasks.html',
  '#update': 'document.html#update',
  '#documentCreate': 'document.html#documentCreate',
  '#analyzers': 'search.html#analyzers',
  '#cloudant-query': 'query.html',
  '#http-status-codes': 'http.html#http-status-codes',
  '#replication': 'replication.html',
  '#http-headers': 'http.html#http-headers',
  '#ping': 'account.html#ping',
  '#basic-authentication': 'authentication.html#basic-authentication',
  '#cookie-authentication': 'authentication.html#cookie-authentication',
  '#roles': 'authorization.html#roles',
  '#viewing-permissions': 'authorization.html#viewing-permissions',
  '#modifying-permissions': 'authorization.html#modifying-permissions',
  '#creating-api-keys': 'authorization.html#creating-api-keys',
  '#browser-support': 'cors.html#browser-support',
  '#security': 'cors.html#security',
  '#configuration-endpoints': 'cors.html#configuration-endpoints',
  '#json-format': 'cors.html#json-format',
  '#setting-the-cors-configuration': 'cors.html#setting-the-cors-configuration',
  '#reading-the-cors-configuration': 'cors.html#reading-the-cors-configuration',
  '#get-databases': 'database.html#get-databases',
  '#get-documents': 'database.html#get-documents',
  '#get-changes': 'database.html#get-changes',
  '#read-many': 'document.html#read-many',
  '#bulk-operations': 'document.html#bulk-operations',
  '#inline': 'attachments.html#inline',
  '#index-functions': 'search.html#index-functions',
  '#queries': 'search.html#queries',
  '#query-syntax': 'search.html#query-syntax',
  '#faceting': 'search.html#faceting',
  '#geographical-searches': 'search.html#geographical-searches',
  '#highlighting-search-terms': 'search.html#highlighting-search-terms',
  '#cloudant-geo-overview': 'geo.html#cloudant-geo-overview',
  '#advanced-replication': 'advanced_replication.html',
  '#active-tasks': 'active_tasks.html',
  '#advanced': 'advanced.html',
  '#creating-an-index': 'cloudant_query.html#creating-an-index',
  '#finding-documents-using-an-index': 'cloudant_query.html#finding-documents-using-an-index',
  '#monitoring': 'monitoring.html'
}
fragment = window.location.hash;
dest = fragments[fragment];
if (dest) {
  window.location = dest;
}
</script>



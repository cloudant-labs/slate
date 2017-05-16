---
title: Cloudant Documentation - Guides

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
  - guides/index

---

<script>
fragments = {
  '#json': 'json.html',
  '#monitoring-replication28': 'managing_tasks.html',
  '#managing-tasks': 'managing-tasks.html',
  '#document-versioning-and-mvcc': 'mvcc.html',
  '#transactions-in-cloudant': 'transactions.html',
  '#cap-theorem': 'cap_theorem.html',
  '#back-up-your-data': 'backup-guide.html',
  '#back-up-your-data-using-replication': 'backup-guide-using-replication.html',
  '#couchapps': 'couchapps.html',
  '#design-document-management': 'design_document_management.html',
  '#replication': 'replication_guide.html',
  '#cloudant-geospatial': 'geo.html',
  '#warehousing': 'warehousing.html'
}
fragment = window.location.hash;
dest = fragments[fragment];
if (dest) {
  window.location = dest;
}
</script>

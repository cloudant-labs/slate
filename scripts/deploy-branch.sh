#!/bin/bash

if [[ "$TRAVIS_PULL_REQUEST" == "false" ]]
then
  if [ -z "$1" ]
  then
    echo "No USERNAME provided. Skipping..."
  else
    rm -rf tmp
    mkdir tmp
    echo curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}" -X PUT
    curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}" -X PUT
    python scripts/upload_documentation_as_docs.py "$TRAVIS_BRANCH"
    for file in `ls tmp`; do
			rev=$(curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}/${file}" | jq -r '._rev')
			if [ $rev = null ]; then
			  echo curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}/${file}" -X PUT -H 'Content-Type: application/json' -d "@tmp/${file}"
				curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}/${file}" -X PUT -H 'Content-Type: application/json' -d "@tmp/${file}"
			else
			  echo curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}/${file}?rev=${rev}" -X PUT -H 'Content-Type: application/json' -d "@tmp/${file}"
				curl "https://$USERNAME:$PASSWORD@docs-testb.cloudant.com/${TRAVIS_BRANCH}/${file}?rev=${rev}" -X PUT -H 'Content-Type: application/json' -d "@tmp/${file}"
			fi
		done

    #deploy with db name == branch name
    couchapp push couchapp "https://$1:$2@docs-testb.cloudant.com/${TRAVIS_BRANCH}"
    #give people read access and docs-testb admin access
    security='
      {
        "cloudant": {
          "mgroenen": ["_reader"],
          "dbsgrl": ["_reader"],
		      "warmanaibm": ["_reader"],
		      "bradnoble": ["_reader"],
		      "reader": ["_reader"],
		      "bradley-holt": ["_reader"],
		      "ten-eleven": ["_reader"],
		      "elsmore": ["_reader"],
		      "rajsingh": ["_reader"],
          "kelepirstantoneatessolit":["_reader"],
          "docs-testb":["_reader","_writer","_admin","_replicator"]
		    }
		  }'
    curl -X PUT "https://$1:$2@docs-testb.cloudant.com/${TRAVIS_BRANCH}/_security" -d "${security}"
  fi
else
  echo "this is a pull request; not deploying."
fi

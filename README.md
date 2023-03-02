
Repository for backend-related code

## Introspect Graphql

```bash
docker-compose -f local.yml run django python manage.py graphql_schema --schema treeflow.schema.schema --out schema.graphql
```

or

```bash
docker-compose -f local.yml run --rm django python manage.py export_schema treeflow.schema > schema.graphql
```

## Import Data

```bash
docker-compose -f local.yml run --rm django python manage.py import_text /app_data/DMX-L19.csv L19  DMX "Greater Bundahisn or Iranian Bundahisn"
```

## Index Elastic Search

```bash
docker-compose -f local.yml run --rm django python manage.py  search_index --rebuild
```


Repository for backend-related code

## Introspect Graphql

```bash
docker-compose -f local.yml run django python manage.py graphql_schema --schema mpcd.schema.schema --out schema.graphql
```

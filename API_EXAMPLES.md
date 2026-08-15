# API Examples

Start:

```powershell
python -m uvicorn app.main:app --reload
```

## Health

```text
GET http://127.0.0.1:8000/health
```

## Upload Excel

```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/clients/ingest" `
  -F "file=@data/clients.xlsx"
```

## Get all

```text
GET http://127.0.0.1:8000/api/v1/clients
```

## Get chunk 1

```text
GET http://127.0.0.1:8000/api/v1/clients/chunks
```

Default page size is 4.

## Get chunk 2

```text
GET http://127.0.0.1:8000/api/v1/clients/chunks?chunk_number=2&chunk_size=4
```

## Custom filter

```text
GET http://127.0.0.1:8000/api/v1/clients/filter?city=Delhi&status=active
```

## Revenue filter

```text
GET http://127.0.0.1:8000/api/v1/clients/filter?min_revenue=50000&max_revenue=150000
```

## Date filter

```text
GET http://127.0.0.1:8000/api/v1/clients/filter?created_from=2026-01-10&created_to=2026-02-15
```

Swagger:
http://127.0.0.1:8000/docs

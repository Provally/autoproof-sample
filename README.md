# Ledgerly

A small invoicing service with deliberate security flaws, made for AutoProof demo accounts.
Do not deploy this code.

- `app/` is the Flask service. `Dockerfile` builds and runs it on port 8000.
- `attachments/` holds the invoice attachments the image publishes read only.
- `libs/ledger_import/` is a separate Python package that a nightly job uses to import the statement files
  bank partners upload (CSV statements with a YAML column mapping). The service does not use it.

## Running the service

```
docker build -t ledgerly .
docker run -p 8000:8000 ledgerly
```

`POST /signup` with a form field `email` opens an account and signs it in with a session cookie.

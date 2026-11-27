FROM python:3.12-slim

WORKDIR /srv/ledgerly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
# Attachments are published with the image and read only: the service account owns the database, not them.
COPY attachments ./data/attachments
RUN useradd --create-home ledgerly && chown ledgerly /srv/ledgerly/data
USER ledgerly

ENV LEDGERLY_DATA=/srv/ledgerly/data
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app.main:app"]

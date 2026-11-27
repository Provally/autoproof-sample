FROM python:3.12-slim

WORKDIR /srv/ledgerly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY attachments ./attachments
# The service account owns only the database directory. The code and the attachments stay root-owned and read only.
RUN useradd --create-home ledgerly && mkdir data && chown ledgerly data
USER ledgerly

ENV LEDGERLY_DATA=/srv/ledgerly/data
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app.main:app"]

FROM python:3.12-slim

WORKDIR /srv/ledgerly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN useradd --create-home ledgerly && mkdir -p /srv/ledgerly/data && chown -R ledgerly /srv/ledgerly
USER ledgerly

ENV LEDGERLY_DATA=/srv/ledgerly/data
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app.main:app"]

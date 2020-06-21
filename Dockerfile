# FROM kennethreitz/pipenv

# COPY . /app

# COPY yacrontab.yaml /etc/yacron.d/yacrontab.yaml

# # ENTRYPOINT ["/yacron/bin/yacron"]

# CMD yacron -c /etc/yacron.d/yacrontab.yaml
# # CMD scrapy crawl immoscout -o apartments.csv -a url=$URL  -L INFO

FROM selenium/standalone-chrome

WORKDIR /app

COPY run.py .
COPY crawler.py .
COPY google_sheets.py .
COPY credentials.json .
COPY requirements_docker.txt .

USER root

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3.7 python3.7-venv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN pip install -r requirements_docker.txt

# Run the application:
# COPY myapp.py .
CMD ["python", "run.py"]


FROM python:3.11

COPY ./backend /backend
COPY ./requirements /requirements
COPY ./scripts /scripts
RUN chmod +x /scripts/run_server.sh
RUN chmod +x /scripts/run_tests.sh
RUN chmod +x /scripts/run_prod.sh

WORKDIR /backend
RUN pip install --no-deps -r /requirements/requirements.txt

CMD ["bash", "/scripts/run_server.sh"]
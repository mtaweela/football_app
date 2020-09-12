FROM python:3.7

# python dependencies
RUN pip install --upgrade pip

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system

# expose port
EXPOSE 9000

# upload scripts
COPY ./scripts/start.sh /


CMD ["./scripts/start.sh"]
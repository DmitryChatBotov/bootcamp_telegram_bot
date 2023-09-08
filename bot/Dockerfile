FROM python:3.10

ENV USER custom_user
RUN adduser $USER

WORKDIR /app

RUN pip install "poetry==1.4.2"
COPY poetry.lock pyproject.toml ./

RUN poetry config installer.max-workers 4 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi --without dev
COPY ./ /app
RUN chown -R $USER:$USER /app
USER $USER
CMD ["python", "main.py"]

FROM python:3-alpine

# Argument for running
ARG SECRET_KEY
ARG ALLOWED_HOST=127.0.0.1,localhost

WORKDIR /app/ku-polls

ENV SECRET_KEY=${SECRET_KEY}
ENV ALLOWED_HOST=${ALLOWED_HOST}
ENV TIMEZONE=UTC
ENV DEBUG=False

# Test for secret key
RUN if [ -z "$SECRET_KEY" ]; then echo "No secret key specified in build-arg"; exit 1; fi

COPY ./requirements.txt .
# Install dependencies in docker container
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000
CMD [ "./entrypoint.sh" ]
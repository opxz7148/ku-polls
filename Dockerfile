FROM python:3-alpine

WORKDIR /app/ku-polls

ENV SECRET_KEY=${SECRET_KEY}
ENV ALLOWED_HOST=${ALLOWED_HOST}
ENV TIMEZONE=UTC
ENV DEBUG=${DEBUG}

# Copy project source code
COPY ./requirements.txt .

# Install dependencies in docker container
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000
CMD [ "./entrypoint.sh" ]
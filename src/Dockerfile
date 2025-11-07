# Minimal Dockerfile for the Flask app
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy requirements and install (requirements.txt is in the build context root)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# copy app source
COPY . /app

# expose port
EXPOSE 5000

# default command (docker-compose overrides this with `flask run`)
CMD ["flask", "run", "--host=0.0.0.0"]

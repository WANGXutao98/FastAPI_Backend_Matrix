# Pull official latest Python Docker image (Pulished with version 3.11.0)
FROM ..
ENV \

# Set the working directory
WORKDIR /data/app

# Copy all files
COPY /backend /data/app

# Install Python dependencies
RUN pip install --upgrade pip
RUN apt-get -y update && apt-get -y install cron && apt-get -y install systemctl && systemctl start cron;exit 0
COPY /backend/docker/requirements.txt /tmp/requirements.txt
RUN pip3 install -r  /tmp/requirements.txt --extra-index-url https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple --no-cache-dir

RUN python -m pip install protobuf==3.20
# Execute entrypoint.sh

ENTRYPOINT ["./docker/entrypoint.sh" ]

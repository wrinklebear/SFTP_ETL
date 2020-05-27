FROM jenkins/jenkins:lts
FROM python:3.6.1
USER root
ADD . /app
WORKDIR /app
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
 
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
 
WORKDIR /app
 
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt
 
COPY . /app
 
#EXPOSE 映射端口
EXPOSE 9000
EXPOSE 8080
EXPOSE 50000
EXPOSE 5000
EXPOSE 22

# 启动目标服务，并追加/bin/bash命令
CMD python /app/extractor.py && /bin/bash
# CMD python /app/extractor.py && python /app/downloader.py  && /bin/bash

#启动多个服务时，还可以用ENTRYPOINT执行一个脚本，在脚本中启动多个服务
ENTRYPOINT ["/app/entrypoint.sh"]




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
 
#EXPOSE ӳ��˿�
EXPOSE 9000
EXPOSE 8080
EXPOSE 50000
EXPOSE 5000
EXPOSE 22

# ����Ŀ����񣬲�׷��/bin/bash����
CMD python /app/extractor.py && /bin/bash
# CMD python /app/extractor.py && python /app/downloader.py  && /bin/bash

#�����������ʱ����������ENTRYPOINTִ��һ���ű����ڽű��������������
ENTRYPOINT ["/app/entrypoint.sh"]




FROM jenkins/jenkins:lts
USER root
ADD . /app
WORKDIR /app
RUN apt-get update -y

# remove several traces of debian python
RUN apt-get purge -y python.*

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# gpg: key F73C700D: public key "Larry Hastings <larry@hastings.org>" imported
# ENV GPG_KEY 97FC712E4C024BBEA48A61ED3A5CA953F73C700D

ENV PYTHON_VERSION 3.6.1

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 8.1.2

RUN apt-get install -y build-essential

RUN apt-get install -y zlib1g && apt-get install -y zlib1g.dev

RUN set -ex \
        && curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
        && curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
        # && export GNUPGHOME="$(mktemp -d)" \
        # && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
        # && gpg --batch --verify python.tar.xz.asc python.tar.xz \
        # && rm -r "$GNUPGHOME" python.tar.xz.asc \
        && mkdir -p /usr/src/python \
        && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
        && rm python.tar.xz \
        \
        && cd /usr/src/python \
        && ./configure --enable-shared --enable-unicode=ucs4 \
        && make -j$(nproc) \
        && make install \
        && ldconfig \
        && pip3 install --no-cache-dir --upgrade --ignore-installed pip==$PYTHON_PIP_VERSION \
        && find /usr/local -depth \
                \( \
                    \( -type d -a -name test -o -name tests \) \
                    -o \
                    \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
                \) -exec rm -rf '{}' + \
        && rm -rf /usr/src/python ~/.cache

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
        && ln -s easy_install-3.6 easy_install \
        && ln -s idle3 idle \
        && ln -s pydoc3 pydoc \
        && ln -s python3 python \
        && ln -s python3-config python-config


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




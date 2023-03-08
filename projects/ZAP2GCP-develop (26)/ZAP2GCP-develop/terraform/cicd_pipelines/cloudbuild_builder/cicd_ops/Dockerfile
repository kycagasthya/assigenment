FROM gcr.io/google.com/cloudsdktool/cloud-sdk:slim
WORKDIR /

RUN pip3 install virtualenv==16.6.1 && \
    virtualenv -p /usr/bin/python3.7 venv

RUN rm /bin/sh && ln -s /bin/bash /bin/sh && \
    echo "source /venv/bin/activate" > ~/.bashrc

COPY requirements.txt /

RUN source /venv/bin/activate && pip3 install -r requirements.txt

COPY cicd/* /cicd/



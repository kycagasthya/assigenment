FROM tensorflow/tensorflow:2.1.1-gpu

RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y git \
  && rm -rf /var/lib/apt/lists/*

RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    rm -rf /root/tools/google-cloud-sdk/.install/.backup

ENV PATH $PATH:/root/tools/google-cloud-sdk/bin

RUN pip install numpy==1.19.5
RUN pip install scipy==1.5.3
RUN pip install pandas==1.1.5
RUN pip install scikit-learn==0.24.1
RUN pip install ruamel.yaml==0.17.2
RUN pip install six==1.15.0
RUN pip install crcmod==1.7
RUN pip install future==0.18.2
RUN pip install google-cloud-storage==1.37.1
RUN pip install google-cloud-bigquery==2.15.0
RUN pip install google-cloud-bigquery-storage==2.4.0
RUN pip install tensorflow_datasets==1.3.0

COPY task.py .

RUN chmod +x ./task.py

ENTRYPOINT ["python", "task.py" ]

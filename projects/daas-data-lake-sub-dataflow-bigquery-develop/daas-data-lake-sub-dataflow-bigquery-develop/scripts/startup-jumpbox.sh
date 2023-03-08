apt update && apt install -y gnupg software-properties-common python3-pip wget git
pip3 install google-api-python-client google-cloud-storage google-cloud-build python-terraform PyYAML cerberus
ln -s /usr/bin/python3 /usr/bin/python
wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list
apt update && apt-get install terraform

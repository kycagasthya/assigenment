#!/bin/bash

set -e

if [[ -f "/opt/startup-flag" ]]; then
    exit 0
fi

##CLOUDSQL_CONN_STRING="its-managed-dbx-edlops-t:us-central1:csmy-zapdbx-usc1-t"
##BUCKET_NAME="its-managed-dbx-edlops-t-np-proxy-bucket"
CLOUDSQL_CONN_STRING="${cloudsql_conn_string}"
BUCKET_NAME="${bucket_name}"

SEC_AGENTS_LOC="--proxy http://10.3.0.65:8080 http://10.3.0.65/sec_agents"
NESSUS_RPM="Nessus-es8_64_latest.rpm"
CROWDSTRIKE_RPM="falcon-el8.x86-latest.rpm"
LOGRHYTHM_RPM="scsm-el8.x86_64-latest.rpm"
LOGRHYTHM_CONF="internal_scsm.ini"


function cleanup(){
  (rm -f cloud_sql_proxy || true) \
  && (rm -f /usr/local/bin/cloud_sql_proxy || true) \
  && (rm -f $NESSUS_RPM $CROWDSTRIKE_RPM $LOGRHYTHM_RPM $LOGRHYTHM_CONF || true)
}

function install_proxy(){
   gsutil cp gs://$${BUCKET_NAME}/cloud_sql_proxy .\
   && cp cloud_sql_proxy /usr/local/bin/cloud_sql_proxy \
   && chmod +x /usr/local/bin/cloud_sql_proxy
}

function configure_proxy(){
  cloud_sql_proxy -instances=$${CLOUDSQL_CONN_STRING}=tcp:0.0.0.0:3306 -ip_address_types=PRIVATE &> sql_log.txt &
}

function sql_proxy_main(){
  if [[ $BUCKET_NAME != "" || $CLOUDSQL_CONN_STRING != "" ]]; then
    cleanup \
    && install_proxy \
    && configure_proxy \
    && echo "Success . CloudSql proxy installed, and configured susccessfully." \
    # && touch /opt/startup-flag
  else
    echo "Failed . Missing values for LINUX_BIT or CLOUDSQL_CONN_STRING"
    exit 0
  fi
}

function install_nessus(){
   curl -s --output $${NESSUS_RPM} $${SEC_AGENTS_LOC}/$${NESSUS_RPM} \
   && echo "Downloading and installing Nessus Agent" \
   && (rpm -U $${NESSUS_RPM} || true)
}

function configure_nessus(){
   /opt/nessus_agent/sbin/nessuscli agent status |grep "[Nn]ot Linked"  \
   && /opt/nessus_agent/sbin/nessuscli agent link --groups="UNIX" --cloud --key=35af5754036d92200ffae190c9a9cfd5404617eb123bb134cef013326890c0aa \
   || true
}

function install_crowdstrike(){
   curl -s --output $${CROWDSTRIKE_RPM} $${SEC_AGENTS_LOC}/$${CROWDSTRIKE_RPM} \
   && echo "Downloading and installing Crowdstrike Agent" \
   && (rpm -U $${CROWDSTRIKE_RPM} || true) \
   && /opt/CrowdStrike/falconctl -f -s --cid=52EAD81E56174C408A7F4B2DE667D5D3-5F \
   && systemctl start falcon-sensor
}

function install_logrhythm(){
   curl -s --output $${LOGRHYTHM_RPM} $${SEC_AGENTS_LOC}/$${LOGRHYTHM_RPM} \
   && echo "Downloading and installing LogRhythm Agent" \
   && curl -s --output $${LOGRHYTHM_CONF} $${SEC_AGENTS_LOC}/$${LOGRHYTHM_CONF} \
   && (rpm -U $${LOGRHYTHM_RPM} || true) \
   && cp $${LOGRHYTHM_CONF} /opt/logrhythm/scsm/config/scsm.ini \
   && chmod 600 /opt/logrhythm/scsm/config/scsm.ini \
   && systemctl start scsm
}

function sec_agents_main(){
   ( install_nessus \
   && configure_nessus \
   && systemctl start nessusagent \
   && install_crowdstrike \
   && install_logrhythm \
   && touch /opt/startup-flag ) \
   || echo "Security Agents installation FAILED!"
}

sql_proxy_main \
&& sec_agents_main \
|| "Startup script FAILED!"
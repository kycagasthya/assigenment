CLIENT="$1"
ENV="$2"
USER_NAME="$3"
PASSWORD="$4"
DATALAKE_PROJECT_ID="$5"

DB_NAME=inventory-management

TABLE_NAME=address
FILE_NAME=${CLIENT}_${ENV}_address_dump.csv

file="config.${ENV}.json"

result=( $(cat "$file" | jq -r '. | keys[]') )

SOURCE_PROJECT_ID=$(cat "$file" | jq -r ".${CLIENT}.project_id")
NAMESPACE=$(cat "$file" | jq -r ".${CLIENT}.namespace")
echo "Client: $CLIENT, Project ID: $SOURCE_PROJECT_ID"

name_location=$(gcloud container clusters list --format="table[no-heading](name,location)" --project ${SOURCE_PROJECT_ID})
name_location_arr=($name_location)
cluster_name=${name_location_arr[0]}
location=${name_location_arr[1]}
echo "Cluster name: $cluster_name, Location: $location"

gcloud container clusters get-credentials $cluster_name --zone $location --project ${SOURCE_PROJECT_ID}
KUBERNETES_CONTEXT=$(kubectl config current-context)

echo "Kubernetes context: ${KUBERNETES_CONTEXT}"

kubectl "--context=${KUBERNETES_CONTEXT}" --namespace=$NAMESPACE port-forward service/cloudsql-postgres 5432:5432 &
sleep 10


psql "host=127.0.0.1 sslmode=disable dbname=${DB_NAME} user=${USER_NAME} password=${PASSWORD}" -c "\copy (SELECT address, area, temp_zone, aisle, bay, stack, shelf, overstock, dynamic, pickable, active, location_id as mfc_id FROM ${TABLE_NAME}) to '${FILE_NAME}' with csv"
pkill kubectl

python3  known_address_csv_to_bq.py $DATALAKE_PROJECT_ID $FILE_NAME $CLIENT
rm $FILE_NAME
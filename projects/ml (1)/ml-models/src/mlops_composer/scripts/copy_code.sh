DAG_BUCKET="gs://asia-south1-docai-mlops-com-e66f290f-bucket"

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit
DIR="$( pwd )"
SRC_DIR=$( dirname $DIR)
TGT_DIR=${DAG_BUCKET}/dags/$(basename $SRC_DIR)

# copy code to dag bucket
echo "Src:" ${SRC_DIR} 
echo "Target:" ${TGT_DIR}
gsutil rsync -r -x '^.ipynb_checkpoints/*' ${SRC_DIR}  ${TGT_DIR}
echo "Copy done"
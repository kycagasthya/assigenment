#!/bin/sh
echo "select DOCAI / VERTEX AI"
read $user_input
echo $user_input
echo user_input
case $user_input in
    docai)
        echo "you are inside ***DOCAI*** loop"
        echo "Enter Project Number"
        echo $project_number
        echo "Enter Processor_id"
        echo $processor_id
        echo "processor version id"
        echo $processor_Versions_ID
        echo "location"
        echo $location
        
        if [ -z "$project_number" ] || [ -z "$processor_id" ] || [ -z "$processor_Versions_ID" ] || [ -z "$location" ];
        then
            echo "\One of your input is null"
        else
    #token creation 
            TOKEN=$(gcloud auth print-access-token)
            echo "display_TOKEN: $TOKEN"
    #endpoint and host creation
            endpoint="$location-documentai.googleapis.com"
            host="https://$endpoint"
            echo $host
    #check for the default_id
            $sudo apt-get update -y 
            $sudo apt-get --yes install jq
            sleep 1
            output_default_id=$(curl -X GET -H "Authorization: Bearer ${TOKEN}"  "$host/uiv1beta3/projects/$project_number/locations/$location/processors/$processor_id" | jq -r '.defaultProcessorVersion')
            #read $output_default_id
            echo $output_default_id
            echo "default_processor_id : $output_default_id"
            a=$output_default_id
            default_version="${a##*/}"
            echo "current_default_version : $default_version"
    #check for default processor version with input processor version
            if [ "${a##*/}" = $processor_Versions_ID ]; then
                echo "String are equal"
            else
    #deploying the input processor version 
                url="$host/uiv1beta3/projects/$project_number/locations/$location/processors/$processor_id/processorVersions/$processor_Versions_ID:deploy"
                lro_name=$(curl -X POST $url -H "Authorization:Bearer ${TOKEN}"  | jq -r '.name') 
                echo $lro_name
                lro_url="$host/uiv1beta3/$lro_name"
                state="RUNNING"
                while  true;
                do
                    echo $lro_url
                    curl -X GET -H "Authorization:Bearer ${TOKEN}"  $lro_url > output.json
                    sleep 30
                    state=$(grep -o '"state": "[^"]*' output.json | grep -o '[^"]*$')
                    if [ "$state" = "SUCCEEDED" ];
                    then
                        echo $state
                        echo "deployed the user processor version "            
                        break
                    elif [ "$state" = "FAILED" ];
                    then
                        echo "FAILED"
                        break
                    elif [ "$state" = "RUNNING" ];
                    then
                        continue
                    fi
                 done
            fi
            echo "making the version id as default"
    #updating the bigquery table 
            sleep 2
            bq query --nouse_legacy_sql --project_id=$project_id 'update icici_docai_bq.training_model_metrics' set  is_deployed=True where "processor_version_id='$processor_Versions_ID' and model_id='$processor_id'"
    #make it as by default
            sleep 2
            file_name="request.json"
            create_file () {
                {
                    echo "{\"defaultProcessorVersion\":\"projects/$project_number/locations/$location/processors/$processor_id/processorVersions/$processor_Versions_ID\"}"
                } >"${file_name}"
            }
            create_file "request"
            sleep 5
    #setting the default processor version 
            curl -X POST -H "Authorization:Bearer ${TOKEN}" -H "Content-Type:application/json; charset=utf-8" -d @"${file_name}" "$host/uiv1beta3/projects/$project_number/locations/$location/processors/$processor_id:setDefaultProcessorVersion"
    #undeploying the previous version
            echo "undeploying the previous version"
            echo "previous_version : $default_version"
            url="$host/uiv1beta3/projects/$project_number/locations/$location/processors/$processor_id/processorVersions/$default_version:undeploy"
            curl -X POST $url -H "Authorization:Bearer ${TOKEN}"
            sleep 3
            bq query --nouse_legacy_sql --project_id=$project_id 'update icici_docai_bq.training_model_metrics' set  is_deployed=false where "processor_version_id='$default_version' and model_id='$processor_id'"
            echo "\Inputs are not null"
        fi
        ;;

    vertexai)
        echo "you are inside ***VERTEX AI*** loop"
        echo "Enter Model Name"
        echo $model_name
        echo "Enter gcs path"
        echo $gs_path
        echo "Enter endpoint id"
        echo $endpoint_id
        echo "Enter endpoint name"
        echo $endpoint_name
        echo "Enter Project Number"
        echo $project_number
        echo "Enter Project ID"
        echo $project_id
        echo "Enter location"
        echo $location
        
        if [ -z "$model_name" ] || [ -z "$gs_path" ] || [ -z "$project_number" ] || [ -z "$project_id" ] || [ -z "$location" ];
        then
            echo "\One of your input is null"
        else
            echo "\Inputs are not null"
    #token creation 
            TOKEN=$(gcloud auth print-access-token)
            endpoint="$location-aiplatform.googleapis.com"
            hostai="https://$endpoint"
    #import  the model 
            file_name="modelupload.json"
            create_file (){
                {
                    echo "{
                            \"model\": {
                                    \"displayName\": \"$model_name\",
                                    \"containerSpec\": 
                                    {
                                        \"imageUri\": \"us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-4:latest\"
                                    },
                                    \"artifactUri\": \"$gs_path\"
                                        }
                        }"
                }>"${file_name}"
            }
            create_file "modelupload"
            sleep 2
            curl -X POST -H "Authorization: Bearer ${TOKEN}" -H "Content-Type:application/json; charset=utf-8" -d @modelupload.json  "$hostai/v1/projects/$project_number/locations/$location/models:upload"
            sleep 1
            $sudo apt-get update -y 
            $sudo apt-get --yes install jq
    #fetching the model id 
            model=$(curl -X GET -H "Authorization: Bearer ${TOKEN}"  $hostai/v1/projects/$project_number/locations/$location/models?filter=displayName="$model_name" | jq -r '.models[0].name')
            echo $model
            model_id="${model##*/}"
            echo "modelid: $model_id"
            export model_id=$model_id
    #input endpoint_name  
            state=$endpoint_name
            if [ $state="$endpoint_name" ] && [ ! -z "$state" ];
            then
                echo "PRINT STATE",$state
                echo "print endpoint name",$endpoint_name
                echo "endpoint_name loop"
    #endpoint creation 
                gcloud ai endpoints create --project=$project_id --region=$location --display-name=$endpoint_name
                endpoint=$(curl -X GET -H "Authorization: Bearer ${TOKEN}"  $hostai/v1/projects/$project_number/locations/$location/endpoints?filter=displayName="$endpoint_name" | jq -r '.endpoints[0].name')
                echo $endpoint
                new_endpoint_id="${endpoint##*/}"
                echo "endpointid: $new_endpoint_id"
                export new_endpoint_id=$new_endpoint_id
                sleep 2
    #deploy model 
                file_name="deploymodel.json"
                create_file (){
                    {
                        echo "{
                            \"deployedModel\": {
                            \"model\": \"projects/$project_number/locations/$location/models/$model_id\",
                            \"displayName\": \"$model_name\",
                            \"dedicatedResources\": {
                                \"machineSpec\": {
                                \"machineType\": \"n1-standard-4\"
                                                },
                                \"minReplicaCount\": 1,
                                \"maxReplicaCount\": 1
                                                        }
                                                },
                            \"trafficSplit\": {
                            \"0\": 100
                            }
                        }"
                    }>"${file_name}"
                
                } 
            create_file "deploymodel"
            sleep 2
    #lro operation start 
            url="$hostai/v1/projects/$project_number/locations/$location/endpoints/$new_endpoint_id:deployModel"
            lro_name=$(curl -X POST $url -H "Authorization:Bearer ${TOKEN}" -H "Content-Type:application/json; charset=utf-8" -d @deploymodel.json | jq -r '.name') 
            echo $lro_name
            lro_url="$hostai/v1/$lro_name"
            if  [ "$lro_name" = "null" ];then   
                echo "lro_name is null : $lro_name"
            else
                done="false"
                while  true;
                do
                    echo $lro_url
                    curl -X GET -H "Authorization:Bearer ${TOKEN}"  $lro_url > outputmodel.json
                    sleep 30
                    cat outputmodel.json
                    done=$(jq -r '.done' outputmodel.json)
                    echo $done
                    if [ "$done" = "true" ];
                    then
                        echo $done
                        echo "deployed the user model to endpoint"            
                        break
                    fi
                done
            sleep 2 
    #updating to bigquery table 
            bq query --nouse_legacy_sql --project_id=$project_id 'update icici_docai_bq.training_model_metrics' set  is_deployed=True where "gcs_path_model='$gs_path'"
            fi
            fi
            state_id=$endpoint_id
            if [ $state_id="$endpoint_id" ] && [ ! -z "$state_id" ];
            then

                echo "state id",$state_id
                echo "ENDPOINT ID IS",$endpoint_id
                $sudo apt-get update -y 
                $sudo apt-get --yes install jq
                deployed_id=$(gcloud ai endpoints describe $endpoint_id --project=$project_id --region=asia-south1 --format=json | jq -r '.deployedModels[0].id')  
                echo $deployed_id
                echo $endpoint_id
                echo $location
                echo $model_name
                echo $model_id
                sleep 4
                file_name="deploymodelcase.json"
                create_file (){
                    {
                        echo "{
                            \"deployedModel\": {
                            \"model\": \"projects/$project_number/locations/$location/models/$model_id\",
                            \"displayName\": \"$model_name\",
                            \"dedicatedResources\": {
                                \"machineSpec\": {
                                \"machineType\": \"n1-standard-4\"
                                                },
                                \"minReplicaCount\": 1,
                                \"maxReplicaCount\": 1
                                                        }
                                                },
                            \"trafficSplit\": {
                            \"0\": 100
                            }
                        }"
                    }>"${file_name}"
                
                }
                create_file "deploymodelcase"
                cat deploymodelcase.json
                sleep 2
    #LRO operation on deployment of model
                url="$hostai/v1/projects/$project_number/locations/$location/endpoints/$endpoint_id:deployModel"
                lro_name=$(curl -X POST $url -H "Authorization:Bearer ${TOKEN}" -H "Content-Type:application/json; charset=utf-8" -d @deploymodelcase.json | jq -r '.name') 
                echo $lro_name
                lro_url="$hostai/v1/$lro_name"
                if  [ "$lro_name" = "null" ];then   
                    echo "lro_name is null : $lro_name"
                else
                    done="false"
                    while  true;
                    do
                        echo $lro_url
                        curl -X GET -H "Authorization:Bearer ${TOKEN}"  $lro_url > outputmodelcase.json
                        sleep 30
                        cat outputmodelcase.json
                        done=$(jq -r '.done' outputmodelcase.json)
                        echo $done
                        if [ "$done" = "true" ];
                        then
                            echo $done
                            echo "deployed the user model to endpoint"            
                            break
                        fi
                    done
                sleep 2
    #undeploy the pervious existing model from endpoint
                gcloud  ai endpoints undeploy-model $endpoint_id --project=$project_id --region=$location --deployed-model-id=$deployed_id
                sleep 4
                bq query --nouse_legacy_sql --project_id=$project_id 'update icici_docai_bq.training_model_metrics' set  is_deployed=True where "gcs_path_model='$gs_path'"
                #bq query --nouse_legacy_sql 'update icici_docai_bq.training_model_metrics' set  is_deployed=True where "job_id='custom-od-train-pipeline-20220608100745'"
                #bq query --nouse_legacy_sql 'update icici_docai_bq.training_model_metrics' set  is_deployed=True where "job_id='custom-od-train-pipeline-20220608100745'"
                fi
            fi
        fi
        ;;
  
    *)
        echo "User input invalid"
        ;;
esac


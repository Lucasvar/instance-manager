#!/bin/bash

OFF_STATE="stop"
ON_STATE="start"

aws configure set aws_access_key_id $ACCESS_KEY_ID
aws configure set aws_secret_access_key $SECRET_ACCESS_KEY
aws configure set default.region us-east-1

case "$PROJECT" in
    "crm")
        CRM_INSTANCEID=$(aws ec2 describe-instances  --filters "Name=tag-value,Values=CRM Development" | jq '.Reservations[0].Instances[0].InstanceId' | sed 's/"//g')
        if [ $STATE == $OFF_STATE ]; then
            aws ec2 stop-instances --instance-ids $CRM_INSTANCEID
        fi
        if [ $STATE == $ON_STATE ]; then
            aws ec2 start-instances --instance-ids $CRM_INSTANCEID
        fi
    ;;
    "webpj")
        WEBPJ_INSTANCEID=$(aws ec2 describe-instances  --filters "Name=tag-value,Values=PJ Development" | jq '.Reservations[0].Instances[0].InstanceId' | sed 's/"//g')
        if [ $STATE == $OFF_STATE ]; then
            aws ec2 stop-instances --instance-ids $WEBPJ_INSTANCEID
        fi
        if [ $STATE == $ON_STATE ]; then
            aws ec2 start-instances --instance-ids $WEBPJ_INSTANCEID
        fi
    ;;
    "folclass")
        FOLCLASS_INSTANCEID=$(aws ec2 describe-instances  --filters "Name=tag-value,Values=Folclass Development" | jq '.Reservations[0].Instances[0].InstanceId' | sed 's/"//g')
        if [ $STATE == $OFF_STATE ]; then
            aws ec2 stop-instances --instance-ids $FOLCLASS_INSTANCEID
        fi
        if [ $STATE == $ON_STATE ]; then
            aws ec2 start-instances --instance-ids $FOLCLASS_INSTANCEID
        fi
    ;;
    *)
    	exit 22
    ;;
esac
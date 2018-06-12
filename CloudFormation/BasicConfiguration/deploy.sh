#!/bin/sh

ZIP="emtconfig.zip"
ZIP_FOLDER="/tmp"
BUCKET="rodeolabz"
REGIONS="us-east-1"
PROFILE="default"

for REG in $REGIONS; do
    echo Uploading region $REG
    aws s3 cp $ZIP_FOLDER/$ZIP s3://$BUCKET-$REG/mediatailor/$ZIP --profile $PROFILE --region $REG
    for TEMPLATE in `ls -1 *.json`; do
        aws s3 cp $TEMPLATE s3://$BUCKET-$REG/mediatailor/$TEMPLATE --profile $PROFILE --region $REG
    done
done

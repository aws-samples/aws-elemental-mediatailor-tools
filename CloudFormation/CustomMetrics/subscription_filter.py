import boto3
import json
import os
from botocore.vendored import requests
import string

def lambda_handler(event, context):
    client = boto3.client('logs')

    print ("subscription filter event: " + json.dumps(event))

    # get environment variables
    filterName = "ADSErrors"
    destinationArn = os.environ['DestinationARN']
    filterPattern = os.environ['FilterPattern']
    logGroupNameList = event["ResourceProperties"]["LogGroupNames"]
    response = {}

    result = {
        'Status': 'SUCCESS',
        'Data': response,
        'ResourceId': event["LogicalResourceId"]
    }

    if event["RequestType"] == "Create" or event["RequestType"] == "Update":
        print ("destinationARN: " + destinationArn)
        print ("filterPattern: " + filterPattern)       
        #iterate over the list of log groups  and then put the subscription filter 
        try:
            for logGroup in logGroupNameList:
                print ("LogGroupName: " + logGroup)
                response = client.put_subscription_filter(
                    logGroupName=logGroup,
                    filterName=filterName,
                    filterPattern=filterPattern,
                    destinationArn=destinationArn
                )
        except Exception as exp:
            print("Exception: %s" % exp)
            response = {"Exception": str(exp)}
            result = {
                'Status': 'FAILED',
                'Data': response,
                'ResourceId': event["LogicalResourceId"]
            }
    elif event["RequestType"] == "Delete":
        #iterate over the list of log groups and then remove subscription filter
        try:
            print("Delete requested")
            for logGroup in logGroupNameList:
                response = client.delete_subscription_filter(
                    logGroupName=logGroup,
                    filterName=filterName
                )
        except Exception as exp:
            print("Exception: %s" % exp)
            response = {"Exception": str(exp)}
            result = {
                'Status': 'FAILED',
                'Data': response,
                'ResourceId': event["LogicalResourceId"]
            }
    send(event, context, result['Status'],
                        result['Data'], result['ResourceId'])
    return        


def send(event, context, responseStatus, responseData, physicalResourceId):
    responseUrl = event['ResponseURL']

    responseBody = {
        'Status': responseStatus,
        'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': physicalResourceId or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

    return

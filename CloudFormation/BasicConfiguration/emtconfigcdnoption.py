import boto3
import json
import os
from botocore.vendored import requests
import string
from urllib.parse import urlparse


def lambda_handler(event, context):
    emt = boto3.client("mediatailor")
    print("mediatailor event: " + json.dumps(event))
    session = boto3.session.Session()
    region = session.region_name

    # get environment variables
    configName = os.environ["ConfigName"]
    videoSource = os.environ["VideoSource"]
    adServer = os.environ["ADS"]
    adSlate = os.environ["SlateAdURL"]
    enableCF = os.environ["EnableCloudFront"]
    cdnPrefix = ""
    cdnSegmentPrefix = ""

    # all the info we need to set up a proper distribution
    parsedSourceURL = urlparse(videoSource)
    VideoSourceDomainName = parsedSourceURL.netloc
    VideoSourcePath = parsedSourceURL.path

    if "AdSegmentUrlPrefix" in event["ResourceProperties"]:
        cdnPrefix = event["ResourceProperties"]["AdSegmentUrlPrefix"]
        cdnSegmentPrefix = cdnPrefix + VideoSourcePath

    response = {}
    result = {
        "Status": "SUCCESS",
        "Data": response,
        "ResourceId": configName
    }
    if event["RequestType"] == "Create" or event["RequestType"] == "Update":
        print("configName: " + configName)
        print("videoSource: " + videoSource)
        print("ADS: " + adServer)
        print("Enable CloudFront: " + enableCF)
        try:
            if cdnPrefix != "":
                EMTData = emt.put_playback_configuration(
                    AdDecisionServerUrl=adServer,
                    Name=configName,
                    VideoContentSourceUrl=videoSource,
                    SlateAdUrl=adSlate,  # ok even if this is empty
                    CdnConfiguration={
                        "AdSegmentUrlPrefix": cdnPrefix,
                        "ContentSegmentUrlPrefix": cdnSegmentPrefix
                    }
                )
            else:
                EMTData = emt.put_playback_configuration(
                    AdDecisionServerUrl=adServer,
                    Name=configName,
                    VideoContentSourceUrl=videoSource,
                    SlateAdUrl=adSlate  # ok even if this is empty
                )
            print("emt data: " + json.dumps(EMTData))
            parsedEMTPlaybackURL = urlparse(EMTData["HlsConfiguration"]["ManifestEndpointPrefix"])
            MediaTailorDomainName = parsedEMTPlaybackURL.netloc
            HLSPlaybackPath = parsedEMTPlaybackURL.path
            MediaTailorAdsDomainName = "ads.mediatailor." + region + ".amazonaws.com"

            # add the DASH playback prefix to response when you update this with latest EMT model through Layers
            result["Data"] = {
                "OriginDomainName": VideoSourceDomainName,
                "VideoSourcePath": VideoSourcePath,
                "MediaTailorDomainName": MediaTailorDomainName,
                "HLSPlaybackPrefix": EMTData["HlsConfiguration"]["ManifestEndpointPrefix"],
                "HLSPlaybackPath": HLSPlaybackPath
            }
        except Exception as exp:
            print("Exception: %s" % exp)
            result["Status"] = "FAILED"
            result["Data"] = {"Exception": str(exp)}

    elif event["RequestType"] == "Delete":
        # iterate over the list of log groups and then remove subscription filter
        try:
            print("Delete requested")
            result["Data"] = emt.delete_playback_configuration(Name=configName)
        except Exception as exp:
            print("Exception: %s" % exp)
            result["Status"] = "FAILED",
            result["Data"] = {"Exception": str(exp)}
    send(event, context, result["Status"],
         result["Data"], result["ResourceId"])
    return


def send(event, context, responseStatus, responseData, physicalResourceId):
    responseUrl = event["ResponseURL"]

    responseBody = {
        "Status": responseStatus,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": physicalResourceId or context.log_stream_name,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        "content-type": "",
        "content-length": str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)

    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

    return

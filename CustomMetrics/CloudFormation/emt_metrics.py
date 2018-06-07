import boto3
import base64
import gzip
import json
from urllib.parse import urlparse
import os

def lambda_handler(event, context):
    cw_client = boto3.client('cloudwatch')
    print ("event: " + json.dumps(event))
    create_alarm = os.environ['CreateAlarm']
    metric_name = os.environ['MetricName']
    namespace = os.environ['Namespace']

    d = gzip.decompress(base64.b64decode(event['awslogs']['data']))
    dj = json.loads(d.decode())
    for logevent in dj['logEvents']:
        ads_log = json.loads(logevent['message'])
        event_type = ads_log['eventType']
        config_name = ads_log['originId']
        print ("event_type " + event_type)
        print ("config_name " + config_name)
        emit_metric(cw_client, metric_name, namespace, config_name, create_alarm)
    return

def emit_metric(cw_client, metric_name, namespace, config_name, create_alarm):
    print ("adding count to metric %s in namespace %s" % (metric_name, namespace))
    dimension_name = "Configuration Name"
    cw_client.put_metric_data(
        Namespace = namespace,
        MetricData = [
            {
                'MetricName': metric_name,
                'Dimensions': [
                    {
                        'Name' : dimension_name,
                        'Value' : config_name
                    },
                ],
                "Value": 1,
                "Unit": "Count"
            }
        ]
    )
    if create_alarm == "True":
        add_alarm(cw_client, metric_name, config_name, namespace, dimension_name)

def add_alarm(cw_client, metric_name, config_name, namespace, dimension_name):
    print ("adding alarm to metric %s in namespace %s" % (metric_name, namespace))
    cw_client.put_metric_alarm(
        AlarmName= config_name + "_Errors_Alarm",
        ActionsEnabled=False,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic='Sum',
        Dimensions=[
            {
                'Name': dimension_name,
                'Value': config_name
            },
        ],
        Period=900,
        Unit='Count',
        EvaluationPeriods=1,
        Threshold=3,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )
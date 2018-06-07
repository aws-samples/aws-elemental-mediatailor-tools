import json
import boto3
import datetime
from chalice import Chalice

app = Chalice(app_name='emt-cw-logs')


@app.route('/', methods=['GET'], cors=True)
def index():
    #for debug
    print (json.dumps(app.current_request.to_dict()))
    
    originId = event['query_params']['originId']    
     #filter parameters
    logGroupName = 'MediaTailor/AdDecisionServerInteractions'
   
    try:
        response = {}        
        # HTTP response
        response = get_logs(5, originId, logGroupName) # get logs from last 5 minutes

        if(len(response['events']) == 0): #empty list
            print ("no logs from last 5 minutes")
    except Exception as ex:
        response = ex
        print (ex)
    print (response)
    return response

#period in minutes
def get_logs(period, originId, logGroupName):
    logStreamNamesList = []
    # Create CloudWatchLogs client
    cloudwatch_logs = boto3.client('logs')
   
    #get all the appropriate log streams
    log_streams = cloudwatch_logs.describe_log_streams(
            logGroupName=logGroupName, 
            logStreamNamePrefix=originId)
    print(log_streams)
    if (len(log_streams['logStreams'])>0):
        for stream in log_streams['logStreams']:
            logStreamNamesList.append(stream['logStreamName'])
    print (logStreamNamesList)
    
    #delta min ago represented in timedelta
    delta = datetime.timedelta(minutes=period)
    #endtime is now
    end = datetime.datetime.now()
    #starttime is 60 min ago
    start = end - delta
    #in ms since epoch
    start = int(start.strftime("%s")) * 1000
    end = int(end.strftime("%s")) * 1000
        
    #only filter on originId, grab all event types
    loginfo = cloudwatch_logs.filter_log_events(
            logGroupName=logGroupName,
            logStreamNames=logStreamNamesList,
            filterPattern='{($.originId = ' + originId + ')}',
            startTime=start,
            endTime=end,
            limit=100
        )
    return loginfo
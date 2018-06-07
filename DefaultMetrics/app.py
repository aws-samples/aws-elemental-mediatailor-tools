from chalice import Chalice
import boto3
import json
import datetime

app = Chalice(app_name='cw-metrics')


@app.route('/', methods=['GET'], cors=True)
def index():
    #for debug
    print (json.dumps(app.current_request.to_dict()))
    try:
        # Create CloudWatchLogs client
        cwclient = boto3.client('cloudwatch')
        #filter parameters
        originId = app.current_request.query_params['originId']

        #60 min ago represented in timedelta
        delta = datetime.timedelta(minutes=60)
        #endtime is now
        end = datetime.datetime.now()
        #starttime is 60 min ago
        start = end - delta
        
        # HTTP response
        response = {}
        metricNames = ['AdDecisionServer.FillRate', 'Avail.FillRate', 'AdDecisionServer.Ads', 'Avail.FilledDuration', 'AdDecisionServer.Duration', 'Avail.Duration']
        #Value is for the specific MediaTailor configuration we want to get
        for metric in metricNames:
            label = metric
            try: 
                result = cwclient.get_metric_statistics(
                    Namespace = 'AWS/MediaTailor',
                    MetricName = metric,
                    Dimensions = [
                        {
                            'Name': 'ConfigurationName',
                            'Value': originId
                        }
                    ],
                    StartTime = start,
                    EndTime = end,
                    Period = 3600, 
                    Statistics = ['Average']
                )
                print (result)
                if 'Duration' in metric:
                    label = label + " (Milliseconds)"
                else:
                    label = label + " (Count)"
                response[label] = round(result['Datapoints'][0]['Average'], 2)
            except Exception as ex:
                print ("failed with metric " + metric)
                pass
        print (response)
    except Exception as ex:
        response = ex
        print (ex)
    
    return response



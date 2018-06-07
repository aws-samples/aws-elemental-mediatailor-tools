## AWS Elemental Mediatailor Logs

The code sample included here (app.py) was created using the [AWS Chalice](https://github.com/aws/chalice) tool. 
The code accepts one parameter, OriginId, which is the AWS Elemental MediaTailor configuration name of interest. This parameter would be passed through the API Gateway that has been created automatically by Chalice.

There are currently two AWS Elemental MediaTailor log groups available via Amazon CloudWatch: 'MediaTailor/AdDecisionServerInteractions' and 'MediaTailor/ManifestService'. This application queries the 'MediaTailor/AdDecisionServerInteractions' specifically. It first gets all the logStreamNames in this log group, then uses all those logStreamNames to extract the actual logs in the last 5 minutes. In addition, it only gets the log entries where the OriginId provided appears.  

The returned log entries can be passed along for further processing or simply displayed. 
## AWS Elemental Mediatailor Default Metrics

The code sample included here (app.py) was created using the [AWS Chalice](https://github.com/aws/chalice) tool. 
The code accepts one parameter, OriginId, which is the AWS Elemental MediaTailor configuration name of interest. This parameter would be passed through the API Gateway that has been created automatically by Chalice.

The AWS Elemental MediaTailor default metrics are queried for very specific metric names including: 'AdDecisionServer.FillRate', 'Avail.FillRate', 'AdDecisionServer.Ads', 'Avail.FilledDuration', 'AdDecisionServer.Duration', and 'Avail.Duration'. The query gets the average of these metrics in the last 60 minutes. 

The returned average values can be passed along to another function, like a script for UI display. 
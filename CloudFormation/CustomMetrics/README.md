The template will create the Lambda, IAM role needed by Lambda, subscription to Lambda, and the CloudWatch alarm. The template will **not** create the IAM role that give AWS Elemental MediaTailor access to CloudWatch (the first section in this tutorial). It assumes this step has been done previously. It takes the following parameters:

1. LogFilterPattern - (required) Log filter in CloudWatch filter and pattern syntax
1. LogGroupNames - (required) Comma delimited list of Log Groups to subscribe for metric generation
1. MetricName - (requied) Name of metric to be created
1. Namespace - (required) Namespace to put the metric in 
1. CreateAlarm - True of False, whether to create an alarm for each Metric dimension. If true, Alarm is created and will activate when 3 or more errors are detected in the last 15 minutes (the threshold and period are currently hardcoded and not being passed in as parameters)

This template will fail if:
1. One or both of the AWS Elemental MediaTailor log groups does not exist yet. You must generate logs in order for the log groups to exist.
1. Some service (like a Lambda) is already subscribed to one or both AWS Elemental MediaTailor log groups.
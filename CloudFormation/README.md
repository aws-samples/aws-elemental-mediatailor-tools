## CloudFormation Templates

###  [EMTConfig.json](BasicConfiguration)
This template creates an AWS Elemental MediaTailor configuration.  It takes the following parameters:

1. ConfigName - (required) MediaTailor configuration name
1. VideoSourceURL - (required) The URL prefix for the master playlist for the HLS source stream, minus the asset ID
1. ADS - (required) The URL for the ad decision server (ADS)
1. AdSegmentUrlPrefix - If configuring content delivery network  (CDN) like Amazon CloudFront, provide URL prefix for serving ad segments
1. ContentSegmentUrlPrefix - If configuring content delivery network  (CDN) like Amazon CloudFront, provide URL prefix for caching content segments
1. SlateAdURL -  The  URL for a high-quality video asset to transcode and use to fill in time that's not used by ads

If setting up CDN, make sure to provide both AdSegmentUrlPrefix and ContentSegmentUrlPrefix.

On its own, the template is not a big time saver as compared to creating a configuration manually via the AWS Elemental MediaTailor console. However, it can be used (with some edits) in conjunction with other templates to automate a more involved workflow. One example would be a workflow that creates an AWS Elemental MediaLive channel that pushes to AWS Elemental MediaPackage, then an AWS Elemental MediaTailor configuration using the MediaPackage channel as a video source.

### [EMTMetrics.json](CustomMetrics)
This template automates the [Custom Metrics tutorial](../CustomMetrics).  It will create the Lambda, IAM role needed by Lambda, subscription to Lambda, and the CloudWatch alarm. The template will **not** create the IAM role that give AWS Elemental MediaTailor access to CloudWatch (the first section in this tutorial). It assumes this step has been done previously. It takes the following parameters:

1. LogFilterPattern - (required) Log filter in CloudWatch filter and pattern syntax
1. LogGroupNames - (required) Comma delimited list of Log Groups to subscribe for metric generation
1. MetricName - (requied) Name of metric to be created
1. Namespace - (required) Namespace to put the metric in 
1. CreateAlarm - True of False, whether to create an alarm for each Metric dimension. If true, Alarm is created and will activate when 3 or more errors are detected in the last 15 minutes (the threshold and period are hardcoded)

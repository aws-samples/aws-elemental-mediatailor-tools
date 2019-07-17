This [template](EMTConfigCDNOption.json) automates the creation of a MediaTailor configuration. It takes the following parameters:

1. ConfigName - (required) MediaTailor configuration name
1. VideoSourceURL - (required) The URL prefix for the master playlist for the HLS source stream, minus the asset ID
1. ADS - (required) The URL for the ad decision server (ADS)
1. SlateAdURL -  The  URL for a high-quality video asset to transcode and use to fill in time that's not used by ads
1. EnableCloudFront - (False by default) If set to true, will create a CloudFront distribution for the MediaTailor configuration

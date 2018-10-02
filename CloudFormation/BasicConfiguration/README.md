This template automates the creation of a MediaTailor configuration. It takes the following parameters:

1. ConfigName - (required) MediaTailor configuration name
1. VideoSourceURL - (required) The URL prefix for the master playlist for the HLS source stream, minus the asset ID
1. ADS - (required) The URL for the ad decision server (ADS)
1. AdSegmentUrlPrefix - If configuring content delivery network  (CDN) like Amazon CloudFront, provide URL prefix for serving ad segments
1. ContentSegmentUrlPrefix - If configuring content delivery network  (CDN) like Amazon CloudFront, provide URL prefix for caching content segments
1. SlateAdURL -  The  URL for a high-quality video asset to transcode and use to fill in time that's not used by ads

If setting up CDN, make sure to provide both AdSegmentUrlPrefix and ContentSegmentUrlPrefix.
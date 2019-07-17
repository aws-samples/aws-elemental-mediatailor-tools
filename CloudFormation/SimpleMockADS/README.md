The [template](SimpleMockADS.json) deploys an API Gateway and Lambda that acts as a simple ADS. A CloudFront distribution is deployed in front of API Gateway. To personalize the ads, the gateway returns a different VAST XML response depending on the device used. The Lambda function keys off of the User-Agent header passed on by MediaTailor to determine which response to give back. A device running Linux will get a different set of ads than one running MacOS, for example.

The template requires no input parameters. 

It outputs the CloudFront URL for API Gateway, which can then be used as the URL for the ad decision server (ADS) when creating a MediaTailor configuration.

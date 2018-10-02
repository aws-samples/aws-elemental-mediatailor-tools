The template deploys an API Gateway and Lambda that acts as a simple ADS. To personalize the ads, the gateway returns a different VAST XML response depending on the device used. The Lambda function keys off of the User-Agent header passed on by MediaTailor to determine which response to give back.

The template requires no input parameters. It outputs the API gateway invoke URL which can then be used as the URL for the ad decision server (ADS) when creating a MediaTailor configuration.

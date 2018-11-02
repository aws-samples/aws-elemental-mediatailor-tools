## Mock Ad Decision Server (ADS)

In order to configure MediaTailor, an ad decision server must be provided. During testing you may use a simple VAST response XML as a static response to MediaTailor's request for an ad. A tutorial is available on [how to build simple VAST response XML](https://aws.amazon.com/blogs/media/build-your-own-vast-3-0-response-xml-to-test-with-aws-elemental-mediatailor/).

[Here](../CloudFormation/SimpleMockADS), we provide a template that deploys an API Gateway and Lambda with CloudFront, that acts as a simple ADS. The gateway returns a different VAST XML response depending on the device used for playback. 

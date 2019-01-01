# Why would you need this?

When you have tables and table schemas that are constantly in flux, but still want your LookML models to be kept up to date with the changing schemas, this article is for you. The following are basic instructions on how to deploy an AWS Lambda application and set up your Looker instance to poll an initiate changes to your LookML model through the Lambda function.

(Please check out this post)[https://discourse.looker.com/t/automating-frequently-changing-schemas-with-aws-lambda] for more information about installation on AWS Lambda. If you're looking adapt this or launch on another serverless platform, more details are coming soon.

![Image from looker](./img/frequently_changing_schemas.png)
      

# AWS-Cloudwatch-DashBoard-Text_Wdiget-Email-Report

In AWS CLoudwatch Dashbaord there are many different type of widgets possible to create a dashboard, however extracting the data from the dashbaord and publishing in an email might be tricky sometimes.
As for example when using Metric Widget, we can use getMetricWidgetImage -> https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricWidgetImage.html
However, in case of Text Widget, we don't have any such option so we need to update the script in order to get data from cloudwatch using boto3 method - get_dashboard

Using the get_dashbaord method, we'll get the output in following format : 

{"widgets": [{"type": "text", "width": 24, "height": 8, "x": 0, "y": 13, "properties": {"markdown": "# Azure Pipeline Status\n SERVICE | TOTAL|FINISHED| RUNNING| TOBERUN| NOTRUN| WARNING| ERROR| UNKNOWN\n-----------------------------------|--------|--------|--------|--------|--------|--------|--------|--------\nTEST_RNIV | 1 | 1 | | | | | | \nTEST_VAR | 3189 | 549 | 565 | 2071 | | 1 | | 3 \nTEST_PLExplain_T0 | 1421 | 1414 | 7 | | | | | \nTEST_PLExplain_T1 | 1077 | 1077 | | | | | | \nTEST_standard | 600 | 600 | | | | | | \nTEST_RTHTPL | 557 | 556 | 1 | | | | |"}}]}

However, this format won't be ideal one to send over email using smtp, so we update this format using python to represent it in html format, so that the final output somewhat looks like : 

![image](https://github.com/deepc594/AWS-Cloudwatch-DashBoard-Text_Wdiget-Email-Report/assets/69808468/b9c9e65b-d87e-4f88-ab3d-d22f68cad3c5)

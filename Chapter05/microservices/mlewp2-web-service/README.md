# mleip-web-service


# Made already changes to make this work

This code gave errors in aws. I already included the changes to make it work. I found these instructions here:

https://github.com/PacktPublishing/Machine-Learning-Engineering-with-Python-Second-Edition/issues/85


For a microservice with load balancer to be host on AWS it has to have healthcheck endpoints. This application did not have them. 

In order for this section to work, you need to do changes in  code, in how you configure the load balancer, and in the security group assigned to the service. All this changes can be seen here:
https://github.com/PacktPublishing/Machine-Learning-Engineering-with-Python-Second-Edition/issues/85

### Issue 1:
When creating the service, the load balancer checks if it receives a 200 (succeeded) when trying to access the health path of the app. The problem is that the app provided does not have such health path.

Solution: we implement in the code the health path like this:

* in resources folder -> forecast.py, add the following class at the end of the file:
class HealthCheck(Resource):
    def get(self):
        return {"status": "healthy"}, 200
* then in app.py, add HealthCheck to:
from resources.forecast import ForecastHandler, Forecaster, HealthCheck
* and then add api.add_resource(HealthCheck, '/health') after the line api.add_resource(ForecastHandler, '/forecast', resource_class_kwargs={'forecaster': forecaster})

and when building the load balancer,  in health check path, make sure you type '/health'

### Issue 2:
After the service finishes creating and everything seems fine, if you request POST to the DNS provided by the loadbalancer, you might face issue where you don't receive or the request times out... this issue is related to security groups

Solution:

Go to Clusters->Services->
and then click on "Configuration and networking" then scroll down to "Network configuration" you'll see the associated security group, click on it, it will redirect you to the security group that the service is using, then at the bottom you will see "Inbound rules" to the right there is button "Edit inbound rules" click on it then do the following:

Click "Add rule".
Set Type to HTTP.
Set Protocol to TCP.
Set Port range to 80 (or whatever port your service runs on).
Set Source to 0.0.0.0/0 (allows public access) or restrict it to your IP (My IP).
Click "Save rules".

and try sending post request to the DNS again, it should work.



All the details are present in my drive, in the AWS notes regarding deploying with ecs. 
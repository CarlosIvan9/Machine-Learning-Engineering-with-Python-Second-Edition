#This already includes changes to make the deployment work (added health path)

#  Main application file app.py. This web service is a very simple one for returning basic requests that can be built
# upon later.
from flask import Flask
from flask_restful import Api, Resource
from resources.forecast import ForecastHandler, Forecaster, HealthCheck
import logging

app = Flask(__name__)
api = Api(app)

forecaster = Forecaster()
api.add_resource(ForecastHandler, '/forecast', resource_class_kwargs={'forecaster': forecaster})
api.add_resource(HealthCheck, '/health')

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    logging.info('Main app sequence begun')
    app.run(debug=True, host='0.0.0.0', port=5000) # change debug=False in production
    logging.info('App finished')

# **IMPORTANT:when you reach the load balancing section, in health check path, make sure you type '/health' and then wait 
# for creation to finish. You should have healthy checks passed.
# **IMPORTANT: After the service finishes creating and everything seems fine, if you go to Postman and request POST to the 
# DNS provided by the loadbalancer, you might face issue where you don't receive or the request times out... this issue is
#  related to security groups. To fix this:
#Go to Clusters->Services->
#and then click on "Configuration and networking" then scroll down to "Network configuration" you'll see the associated 
# security group, click on it, it will redirect you to the security group that the service is using, then at the bottom you 
# will see "Inbound rules" to the right there is button "Edit inbound rules" click on it then do the following:

#Click "Add rule".
#Set Type to HTTP.
#Set Protocol to TCP.
#Set Port range to 80 (or whatever port your service runs on).
#Set Source to 0.0.0.0/0 (allows public access) or restrict it to your IP (My IP).
#Click "Save rules".

#and try sending post request to the DNS again, it should work.


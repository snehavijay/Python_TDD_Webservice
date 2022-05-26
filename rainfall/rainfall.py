'''
Author: Sneha Vijay
This app is designed to fetch live rain fall data for specific location from https://api.data.gov.sg/v1/environment/rainfall
'''

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger('__name__')

class RainfallData(object):
    def __init__(self, data, location):
        logger.info("Is it raining in %s? Let's find out." % location)
        self.data = data
        self.location = location

    def get_rainfall_data(self):
        ''' get live raining info from given data '''

        try:
            data = self.data
            location = self.location
            # define local variables with default
            found_data = { 'name': "Raining details for '%s', is not found!" % location}
            station_data = data['metadata']['stations']
            readings_data = data['items'][0]['readings']
            station_id = None

            # Loop in data dict to find details for given location
            for i in range(len(station_data)):
                for k, v in station_data[i].items():
                    if k == 'name':
                       if ((location).replace(" ", "") == v.replace(" ", "")):
                            found_data['name'] = v
                            found_data['time'] = (data['items'][0]['timestamp']).split("+")[0].split("T")[1]
                            station_id = station_data[i]['id']

            # If station id is still 'None' then location is not found in given dict
            if station_id != None:
                for j in range(len(readings_data)):
                    for k1, v1 in readings_data[j].items():
                        if k1 == 'station_id' and v1 == station_id :
                           raining_value = readings_data[j]['value']
                           found_data['mm'] = str(raining_value) +"mm"
                           if float(raining_value) == 0.0:
                               found_data['is_raining'] = "Not Raining"
                           else:
                               found_data['is_raining'] = "Raining"
        except:
            logger.error('Something went wrong! Inputs were location:%s, url:%s' %(self.location, self.data))
            return ("Site is in maintenance mode, and will get back soon !")
        logger.info(found_data)
        return (', '.join(found_data.values()))


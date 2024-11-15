import logging
#from Sensors.AmperometerSensor import AmperometerSensor
from Sensors.SensorMock import SensorMock

logger = logging.getLogger(__name__)


class SensorFactory:
    @staticmethod
    def create(sensor_type, sensor_config):
        match sensor_type:
            case 'amperometer':
                logger.info('Creating Amperometer sensor')
                instance = AmperometerSensor()
                if not instance.setup(sensor_config):
                    return None
                return instance
            
            case 'mock':
                logger.info('Creating Mocked sensor')
                instance = SensorMock()
                if not instance.setup(sensor_config):
                    return None
                return instance
            
            case _:
                return None 

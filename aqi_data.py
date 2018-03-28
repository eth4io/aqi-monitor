LEVEL_GOOD = "Good"
LEVEL_MODERATE = "Moderate"
LEVEL_UNHEALTHY_FOR_SENSITIVE_GROUPS = "Unhealthy for Sensitive Groups"
LEVEL_UNHEALTHY = "Unhealthy"
LEVEL_VERY_UNHEALTHY = "Very Unhealthy"
LEVEL_HAZARDOUS = "Hazardous"
LEVEL_BEYOND_INDEX = "Beyond Index"


class AqiData(object):
    def __init__(self, time, aqi, pm25, pm10):
        self.time = time
        self.aqi = aqi
        self.pm10 = pm10
        self.pm25 = pm25
        if aqi <= 50 & aqi > 0:
            self.level = LEVEL_GOOD
        elif aqi <= 100:
            self.level = LEVEL_MODERATE
        elif aqi <= 150:
            self.level = LEVEL_UNHEALTHY_FOR_SENSITIVE_GROUPS
        elif aqi <= 200:
            self.level = LEVEL_UNHEALTHY
        elif aqi <= 300:
            self.level = LEVEL_VERY_UNHEALTHY
        elif aqi <= 500:
            self.level = LEVEL_HAZARDOUS
        else:
            self.level = LEVEL_BEYOND_INDEX

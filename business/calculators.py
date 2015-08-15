import math

class StravaActivityCalculator(object):
    DEFAULT_POINT = 1
    COEFFICIENT = {
        'default': 0.01,
        'ride': 0.05,         # y = sqrt([(5)^2/500)]*x)
        'run': 0.2,           # y = sqrt([(10]^2/500]*x)
        'swim': 0.2,
    }

    def calculate(self, activity):
        type = activity['type']
        power = self.DEFAULT_POINT if 'average_watts' not in activity else activity['average_watts']
        scale = self.COEFFICIENT['default'] if type not in self.COEFFICIENT else self.COEFFICIENT[type]
        return math.sqrt(scale * power)

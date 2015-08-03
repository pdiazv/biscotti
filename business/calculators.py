

class StravaActivityCalculator(object):

    def calculate(self, activity):
        if 'average_watts' not in activity:
            return 50

        return activity['average_watts']


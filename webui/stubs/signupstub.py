from webui.viewsrc import strava


class SignupViewStub(strava.SignupView):

    def __init__(self, sv_client):
        self.sv_client = sv_client


    def getStravaClient(self):
        return self.sv_client

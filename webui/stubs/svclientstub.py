from stravalib.client import Client

class SvClientStub(Client):

    def set_auth_url(self, url):
        self.auth_url = url

    def authorization_url(self, client_id, redirect_uri, approval_prompt='auto', scope=None, state=None):
        self.params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'approval_promt': approval_prompt,
            'scope': scope,
            'state': state
        }

        return self.auth_url if self.auth_url else ''
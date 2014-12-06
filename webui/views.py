from webui.viewsrc import general, auth, simple

default = general.DefaultView.as_view()
main_employee = general.MainEmployeeView.as_view()
google_login = auth.GoogleLoginView.as_view()
trackers = general.TrackersView.as_view()

strava_auth = auth.StravaTokenExchangeView.as_view()
tracker_view = general.SimpleTrackerView.as_view()


simple_signup = simple.SimpleSignupView.as_view()
add_user = simple.SimpleAddUserView.as_view()
add_activity = simple.SimpleAddActivityView.as_view()


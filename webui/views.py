from webui.viewsrc import general, auth, simple, demo_view

default = general.DefaultView.as_view()
main_employee = general.MainEmployeeView.as_view()
google_login = auth.GoogleLoginView.as_view()
trackers = general.TrackersView.as_view()

strava_auth = auth.StravaTokenExchangeView.as_view()
tracker_view = general.SimpleTrackerView.as_view()
user_view = general.MainUserView.as_view()

simple_signup = simple.SimpleSignupView.as_view()
add_user = simple.SimpleAddUserView.as_view()
add_activity = simple.SimpleAddActivityView.as_view()


load_data = demo_view.LoadDataView.as_view()
stats = demo_view.StatsTemplateView.as_view()
stats_data = demo_view.StatsDataView.as_view()

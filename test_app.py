from dash.testing.application_runners import import_app


def test_header_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("h1")
    header = dash_duo.find_element("h1")

    assert "Pink Morsel Sales Visualiser" in header.text, "Header title should be visible"


def test_visualisation_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#sales-chart")
    chart = dash_duo.find_element("#sales-chart")

    assert chart.is_displayed(), "Sales chart should be visible on the page"


def test_region_picker_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter")
    region_picker = dash_duo.find_element("#region-filter")

    assert region_picker.is_displayed(), "Region picker should be visible on the page"

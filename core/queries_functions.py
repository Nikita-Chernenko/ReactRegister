import datetime


def get_query_dates(request):
    date_from = datetime.datetime.strptime(request.request.query_params.get("data_from", "8.09.2017").strip(),
                                           "%d.%m.%Y").date()
    date_to = datetime.datetime.strptime(request.request.query_params.get("data_to", "12.09.2017").strip(),
                                         "%d.%m.%Y").date()
    return date_from, date_to

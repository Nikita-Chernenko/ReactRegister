import datetime


def get_query_dates(request):
    date_from = datetime.datetime.strptime(request.request.query_params.get("date_from", "2017-09-8").strip(),
                                           "%Y-%m-%d").date()
    date_to = datetime.datetime.strptime(request.request.query_params.get("date_to", "2017-09-12").strip(),
                                         "%Y-%m-%d").date()
    return date_from, date_to

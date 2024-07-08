from datetime import datetime

from DateInfo import DateInfo

def get_datetime(params: DateInfo):
  return datetime.now(tz=params.timezone).isoformat()

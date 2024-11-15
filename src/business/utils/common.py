import datetime
from typing import Tuple


class Common:

    @staticmethod
    def get_utc_start_and_end_date() -> Tuple[datetime, datetime]:
        now_utc = datetime.datetime.now(datetime.timezone.utc)

        start_date_utc = datetime.datetime(now_utc.year, now_utc.month, now_utc.day)

        end_date_utc = start_date_utc + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

        return start_date_utc, end_date_utc
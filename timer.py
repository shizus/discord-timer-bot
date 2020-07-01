import asyncio
from datetime import datetime, timedelta


class Timer:

    def __init__(self, end_time, callback=None, sleep=1):
        """
        :param end_time: string with the format hh:mm:ss representing the total time of the timer
        :param callback: if it's not none it will be called passing the timer as a parameter
        """
        self._end_time = end_time
        self._remaining_time = end_time
        self._callback = callback
        self._sleep = sleep

    def get_remaining_time(self):
        return self._remaining_time

    def get_remaining_time_string(self):
        return self.time_delta_to_string(self._remaining_time)

    def time_delta_to_string(self, time_delta):
        """
        datetime to string
        :param time_delta: datetime instance
        :return: datetime as a string with format hh:mm:ss
        """
        str_time_delta = str(time_delta)
        hours, minutes, seconds = str_time_delta.split(':')
        try:
            time_in_str = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(float(seconds)))
        except ValueError as err:
            print("Time delta:", time_delta)
            print(err)
            time_in_str = '00:00:00'
        return time_in_str

    async def run(self):
        now = datetime.now()

        time_string = self._end_time

        hours, mins, seconds = time_string.split(':')

        delta = timedelta(hours=int(hours), minutes=int(mins), seconds=int(seconds))
        end = now + delta
        while end > now:
            await asyncio.sleep(self._sleep)
            now = datetime.now()
            self._remaining_time = end - now
            print("Remaining time {remaining}".format(remaining=self.time_delta_to_string(self._remaining_time)))
            if self._callback is not None:
                try:
                   await self._callback(self)
                except Exception as e:
                    print("callback is supposed to be a function that receives timer as a parameter. Error: ", e)
                    break


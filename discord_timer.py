from timer import Timer


class DiscordTimer(Timer):

    def __init__(self, end_time, callback, guild, sleep=60*5):
        super(DiscordTimer, self).__init__(end_time, callback, sleep)
        self._guild = guild

    def get_guild(self):
        return self._guild
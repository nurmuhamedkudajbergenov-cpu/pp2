from datetime import datetime 

class Clock:
    def currently_time(self):
        now = datetime.now()

        seconds = now.second
        minutes = now.minute

        seconds = now.second + now.microsecond / 1_000_000
        minutes = now.minute + seconds / 60

        seconds_angles = seconds * 6
        minutes_angles = minutes * 6

        return minutes_angles,seconds_angles

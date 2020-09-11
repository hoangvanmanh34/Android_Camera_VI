from threading import Event, Lock, Thread
from time import monotonic  # use time.time or monotonic.monotonic on Python 2
#Hoang Van Manh
#Danny TE-NPI
#hoangvanmanhpc@gmail.com
#https://www.youtube.com/c/StevenHCode
class WatchdogTimer(Thread):
    """Run *callback* in *timeout* seconds unless the timer is restarted."""

    def __init__(self, timeout, callback, *args, timer=monotonic, **kwargs):
        super().__init__(**kwargs)
        self.timeout = timeout
        self.callback = callback
        self.args = args
        self.timer = timer
        self.cancelled = Event()
        self.blocked = Lock()

    def run(self):
        self.restart() # don't start timer until `.start()` is called
        # wait until timeout happens or the timer is canceled
        while not self.cancelled.wait(self.deadline - self.timer()):
            # don't test the timeout while something else holds the lock
            # allow the timer to be restarted while blocked
            with self.blocked:
                if self.deadline <= self.timer() and not self.cancelled.is_set():
                    return self.callback(*self.args)  # on timeout

    def restart(self):
        """Restart the watchdog timer."""
        self.deadline = self.timer() + self.timeout

    def cancel(self):
        self.cancelled.set()

import time

class BaseEngine(object):
    """
    The base engine that defines the interface.
    """
    def __init__(self, runner):
        self.runner = runner
    
    def run(self):
        """
        Executes the runner.
        """
        self.runner()

class SingleProcessEngine(BaseEngine):
    """
    An engine that ensures only one process can run at the same time. Useful
    when being fired off by a cron and you need to ensure a lock is made so
    other processes won't handle a queue at the same time.
    """
    def __init__(self, *args, **kwargs):
        self._lock_wait_timeout = kwargs.pop("lock_wait_timeout", -1)
        super(CronEngine, self).__init__(self, *args, **kwargs)
    
    def run(self):
        """
        Executes the runner using a lock file to prevent race conditions.
        """
        self._create_lock()
        if not self._acquire_lock():
            raise SystemExit
        try:
            super(SingleProcessEngine, self).run()
        finally:
            self._release_lock()
    
    def _create_lock(self):
        """
        Create the lock.
        """
        from lockfile import FileLock
        self._lock = FileLock("%d.lock" % os.getpid())
    
    def _acquire_lock(self):
        """
        Attempt to acquire a lock. Returns False on failure or True on
        success.
        """
        from lockfile import AlreadyLocked, LockTimeout
        logging.debug("acquiring lock...")
        try:
            self._lock.acquire(self._lock_wait_timeout)
        except AlreadyLocked:
            logging.debug("lock already in place. quitting.")
            return False
        except LockTimeout:
            logging.debug("waiting for the lock timed out. quitting.")
            return False
        logging.debug("lock acquired.")
        return True
    
    def _release_lock(self):
        """
        Release the lock.
        """
        logging.debug("releasing lock...")
        self._lock.release()
        logging.debug("lock released.")

class PersistentProcessEngine(BaseEngine):
    """
    An engine that will execute the runner every X seconds.
    """
    def __init__(self, *args, **kwargs):
        self._sleep_duration = kwargs.pop("sleep_duration", 30)
        super(PersistentProcessEngine, self).__init__(self, *args, **kwargs)
    
    def run(self):
        """
        Execute the runner in a persistent process and is called every
        _sleep_duration seconds.
        """
        while True:
            super(PersistentProcessEngine, self).run()
            time.sleep(self._sleep_duration)

import random, thread, time

class ttimer():
    """Threading callback timer - threading timer will callback your function periodically.
	interval - interval callback periodically, in sec
	retry    - execute how many times? -1 is infinity
	cbfunc   - callback function
	cbparam  - parameter in list

	i.e t=ttimer(1,10,myfunc,["myparam"])"""

    def __init__(self, interval, retry, cbfunc, cbparam=[]):
        self.is_start=False
        self.is_end=False

        # doing my thread stuff now.
        thread.start_new_thread(self._callback,(interval,retry,cbfunc,cbparam,))

    def Start(self):
        "start the thread"
        self.mytime=time.time()
        self.is_start=True
	self.is_end=False

    def Stop(self):
        "stop the thread."
        self.mytime=time.time()
        self.is_start=False
        self.is_end=True

    def IsStop(self):
        "Is the thread already end? return True if yes."
        if self.is_end:
            return True
        else:
            return False

    def _callback(self,interval,retry,cbfunc,cbparam=[]):
        """ This is the private thread loop, call start() to start the threading timer."""
        self.retry=retry
        retry=0

        if self.is_end:
            return None

        while True:
            if self.is_end:
                break
            if self.retry==-1:
                pass
            elif retry>=self.retry:
                break

            if self.is_start:
                #check time
                tmptime=time.time()
                if tmptime >=(self.mytime + interval):
                    cbfunc(cbparam) # callback your function
                    self.mytime=time.time()
                    retry+=1
                else:
                    pass
            time.sleep(0.01)

        self.is_end=True

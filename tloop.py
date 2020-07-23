import time

from timeloop import Timeloop
from datetime import timedelta
from togoogle import set_to_sheet

tl = Timeloop()

@tl.job(interval=timedelta(seconds=120))
def sample_job_every_120s():
    set_to_sheet()

tl.start(block=True)
import pbs
import sys 
try:
    if pbs.event().job.group_list == None :
        pbs.event().reject("Job rejected as group list has not been defined")
except SystemExit:
    pass
except:
    pbs.event().reject("Job rejected as group list has not been defined")

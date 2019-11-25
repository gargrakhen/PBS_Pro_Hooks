#qmgr -c 'create hook TakeNodeOffline event="exechost_periodic",freq=10'
#qmgr -c 'import hook TakeNodeOffline application/x-python default TakeNodeOffline.py'

import os
import sys
import pbs

pbs.logmsg(pbs.LOG_DEBUG,"START EXECHOST PERIODIC HOOK ")
local_node = pbs.get_local_nodename()
pbs.logmsg(pbs.LOG_DEBUG, "END EXECHOST PERIODIC HOST HOOK local node hostname %s  " % str(local_node))

vnl = pbs.event().vnode_list
txt_files = [f for f in os.listdir('/tmp') if f.endswith('_remove.txt')]
for file in txt_files:
    full_file_path=os.path.join('/tmp', file)
    pbs.logmsg(pbs.LOG_DEBUG, "END EXECHOST PERIODIC HOST HOOK filename in tmp is  %s  " % str(full_file_path))
    f = open(full_file_path, 'r').read()
    pbs.logmsg(pbs.LOG_DEBUG, "END EXECHOST PERIODIC HOST HOOK contents of file are %s  " % str(f))
    if local_node in f:
        pbs.logmsg(pbs.LOG_DEBUG, "END EXECHOST I am here")
        vnl[local_node].state = pbs.ND_OFFLINE
        vnl[local_node].comment = "offlined node as it is heavily loaded"
        pbs.logmsg(pbs.LOG_DEBUG, "END EXECHOST PERIODIC HOST HOOK offline node %s  " % str(local_node))
pbs.logmsg(pbs.LOG_DEBUG, "END EXECHOST PERIODIC HOST HOOK")

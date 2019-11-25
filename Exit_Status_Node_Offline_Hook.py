import pbs
import os
import re
import sys

e = pbs.event()
try:
    if e.job.in_ms_mom():
        exit_code = str(e.job.Exit_status)

        local_node = pbs.get_local_nodename()
        vnl = e.vnode_list
        current_state = pbs.server().vnode(local_node).state

        if (int(exit_code) != 0) and ((current_state == pbs.ND_OFFLINE) == 0):
            vnl[local_node].state = pbs.ND_OFFLINE
            vnl[local_node].comment = "offlined node as it is heavily loaded"

            report_file1 = str("/home/centos/pqr.txt")
            pbs.logmsg(pbs.LOG_DEBUG, "report_usage file1 is %s" % report_file1)

            fd_out1 = open(report_file1, 'w+')
            print >> fd_out1, 'To: rakhen.garg@ndsu.edu'
            print >> fd_out1, 'From: rakhen.garg@ndsu.edu'
            print >> fd_out1, 'Subject: Node Taken offline'
            print >> fd_out1, 'Node Name: = ' + pbs.server().vnode(local_node).name
            fd_out1.close()

            mail_cmd="/usr/sbin/sendmail -t \"PBS OSS\" < /home/centos/pqr.txt"
            pbs.logmsg(pbs.LOG_DEBUG, "mail_command  is %s" % mail_cmd)
            os.popen(mail_cmd)
            os.unlink("/home/centos/pqr.txt")
        else:
            vnl[local_node].comment = "exit status of the job is not negative"
except SystemExit:
    pass
except:
    pbs.logmsg(pbs.LOG_DEBUG, "report_usage: failed with %s" % str(sys.exc_info()))
    pass
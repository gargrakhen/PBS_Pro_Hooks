import sys
import os
import pbs

e = pbs.event()
try:
    def get_sec(time_str):
        h, m, s = time_str.split(':')
        return str(int(h)*3600 + int(m)*60 + int(s))
    if e.job.in_ms_mom():
        exit_code = str(e.job.Exit_status)
        job_id = str(e.job.id)
        user_name = str(e.job.Job_Owner)

        walltime_used = str(e.job.resources_used["walltime"])
        walltime_req = str(e.job.Resource_List["walltime"])
        walltime_used_hrs = str(round((float(get_sec(str(e.job.resources_used["walltime"])))/3600),2))
        walltime_req_hrs = str(round((float(get_sec(str(e.job.Resource_List["walltime"])))/3600),2))
        walltime_per = str(round((float(walltime_used_hrs)*100/float(walltime_req_hrs)),2))

        mem_req = str(e.job.Resource_List["mem"])
        mem_used = str(e.job.resources_used["mem"])
        mem_used1 = str(round((float(mem_used[:-2])/1048576),2))
        mem_per = str(round((float(mem_used1)*100/float(mem_req[:-2])),2))

        cput_time = str(round((float(get_sec(str(e.job.resources_used["cput"])))/3600),2))
        cpus_cores = str(e.job.resources_used["ncpus"])
        cpus_used = str(round((float(walltime_used_hrs)*float(cpus_cores)),2))
        cpu_per = str(round((float(cpus_used)*100/float(cput_time)),2))

        execution_vnode = str(e.job.exec_vnode)
        execution_vnode1 = execution_vnode.split(':')
        execution_vnode2 = execution_vnode1[0]

        report_file1 = str("/home/centos/abc.txt")
        report_file2 = str("/home/centos/bcd.txt")

        pbs.logmsg(pbs.LOG_DEBUG, "report_usage file1 is %s" % report_file1)
        pbs.logmsg(pbs.LOG_DEBUG, "report_usage file1 is %s" % report_file2)

        if int(exit_code) == 0:
            fd_out1 = open(report_file1, 'w+')
            print >> fd_out1, 'To: rakhen.garg@ndsu.edu'
            print >> fd_out1, 'From: rakhen.garg@ndsu.edu'
            print >> fd_out1, 'Subject: Resource Utilization Details'

            print >> fd_out1, '------------------------------------------START MESSAGE-------------------------------------------'
            print >> fd_out1, 'The following job ran successfully but could probably be run more efficiently:'

            print >> fd_out1, 'Job#: = ' + job_id
            print >> fd_out1, 'User: = ' + user_name
            print >> fd_out1, 'Walltime Stats: Requested: ' + walltime_req_hrs +'Hrs',
            print >> fd_out1, ', Actual Use: ' + walltime_used_hrs +'Hrs',
            print >> fd_out1, ', % of Requested Used: ' + walltime_per +'%'

            print >> fd_out1, 'Memory Stats: Requested: ' + mem_req,
            print >> fd_out1, ', Actual Use: ' + mem_used1 +'gb',
            print >> fd_out1, ', % of Requested Used: ' + mem_per +'%'

            print >> fd_out1, 'CPU Stats: Requested (CPU-Hrs): ' + cput_time +'core hours',
            print >> fd_out1, ', Actual Use: ' + cpus_used +'core hours',
            print >> fd_out1, ', % of Requested Used: ' + cpu_per +'%'
            
            print >> fd_out1, '---------------------------------------------END MESSAGE--------------------------------------------'
            fd_out1.close()

            mail_cmd="/usr/sbin/sendmail -t \"PBS OSS\" < /home/centos/abc.txt"
            pbs.logmsg(pbs.LOG_DEBUG, "mail_command  is %s" % mail_cmd)
            os.popen(mail_cmd)
        else:
            fd_out2 = open(report_file2, 'w+')
            print >> fd_out2, 'To: rakhen.garg@ndsu.edu'
            print >> fd_out2, 'From: rakhen.garg@ndsu.edu'
            print >> fd_out2, 'Subject: Failed Job Details'

            print >> fd_out2, '------------------START MESSAGE------------------'
            try:
                if int(exit_code) > 0 and int(exit_code) < 128:
                    print >> fd_out2, 'Job Failed with Exit status = ' + exit_code,
                elif int(exit_code) >= 128:
                    signal = str(int(exit_code)%128)
                    print >> fd_out2, 'Job Failed with Exit Status = ' + signal,
                else:
                    print >> fd_out2, 'Job Failed with Exit Status = ' + exit_code,
            except Exception as ex:
                print >> fd_out2,+ ex.message,
            print >> fd_out2, 'when submitted'
            print >> fd_out2, 'Job#: = ' + job_id
            print >> fd_out2, 'User: = ' + user_name
            print >> fd_out2, 'Execution vnode is = ' + execution_vnode2[1:]
            print >> fd_out2, '-------------------END MESSAGE-------------------'
            fd_out2.close()

            mail_cmd="/usr/sbin/sendmail -t \"PBS OSS\" < /home/centos/bcd.txt"
            pbs.logmsg(pbs.LOG_DEBUG, "mail_command  is %s" % mail_cmd)
            os.popen(mail_cmd)

except SystemExit:
    pass
except:
    pbs.logmsg(pbs.LOG_DEBUG, "report_usage: failed with %s" % str(sys.exc_info()))
    pass

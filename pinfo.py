#!/usr/bin/env python
from __future__ import division
# from subprocess import PIPE, Popen
import psutil

class Pifo:

    @property
    def cpu_info(self):
        #     process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        #     output, _error = process.communicate()
        #     temp = float(output[output.index('=') + 1:output.rindex("'")])
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp = f.read()
            f.close()
        cpu_percent = psutil.cpu_percent(interval=1,percpu=False)
        return {"CPU_Workload":"{}%".format(cpu_percent),
                "CPU_Temperature": "{0:.1f}'C".format(int(temp) / 10 ** 3)}

    @property
    def disk_info(self):
        disk = psutil.disk_usage('/')
        disk_total = disk.total / 2 ** 30
        disk_used = disk.used / 2 ** 30
        disk_free = disk.free / 2 ** 30
        disk_percent_used = disk.percent
        return {"Disk_Total":str("{0:.2f}GB".format(disk_total)),
                "Disk_Used":str("{0:.2f}GB".format(disk_used)),
                "Disk_Used_Persents":str("{0:.2f}%".format(disk_percent_used)),
                "Disk_Free":str("{0:.2f}GB".format(disk_free))}
    @property
    def mem_info(self):
        mem = psutil.virtual_memory()
        mem_total = mem.total / 2 ** 20
        mem_avail = mem.available / 2 ** 20
        mem_percent_used = mem.percent
        mem_used = mem.used / 2 ** 20
        mem_free = mem.free / 2 ** 20
        return {"Memory_Total":str("{0:.2f}MB".format(mem_total)),
                "Memory_Available":str("{0:.2f}MB".format(mem_avail)),
                "Memory_Used_Persents":str("{0:.2f}%".format(mem_percent_used)),
                "Memory_Used":str("{0:.2f}MB".format(mem_used)),
                "Memory_Free":str("{0:.2f}MB".format(mem_free))}
    @property
    def net_info(self):
        IP = []
        for card in ["eth0", "wlan0"]:
            for addr in psutil.net_if_addrs()[card]:
                if addr.family == 2:
                    IP.append(addr.address)
                else:
                    address = None
        net = psutil.net_io_counters()
        eth = psutil.net_if_addrs()["eth0"][0]
        wlan = psutil.net_if_addrs()["wlan0"][0]
        net_bytes_sent = net.bytes_sent / 2**20
        net_bytes_recv = net.bytes_recv / 2**20

        # net_errin = net.errin
        # net_errout = net.errout
        # net_dropin = net.dropin
        # net_dropout = net.dropout
        # return {"Network MB Sent":str("{0:.2f}MB".format(net_bytes_sent)),
        #         "Network MB Received":str("{0:.2f}MB".format(net_bytes_recv)),
        #         "Network Errors Receiving":str(net_errin),
        #         "Network Errors Sending":str(net_errout),
        #         "Incoming Packets Dropped":str(net_dropin),
        #         "Outgoing Packets Dropped":str(net_dropout)}
        return {"Network_Sent":str("{0:.2f}MB".format(net_bytes_sent)),
                "Network_Received":str("{0:.2f}MB".format(net_bytes_recv)),
                "IP_Address":IP}
    @property
    def uptime(self):
        with open('/proc/uptime') as f:
            t = f.read()
            f.close()
        ut = int(float(t.split(" ")[0])/60)
        return {"uptime": "{} day {} hours {} minutes".format(ut//60//24,ut//60,ut%60)}

    @property
    def piall(self):
        return

if __name__ == '__main__':
    pi = Pifo()
    data = {"status": "ok",
            'data': {"model": "Raspberry Pi 3B",
                     "cpu": pi.cpu_info,
                     "disk": pi.disk_info,
                     "mem": pi.mem_info,
                     "net": pi.net_info,
                     "uptime": pi.uptime}}
    import pprint
    pprint.pprint(data)
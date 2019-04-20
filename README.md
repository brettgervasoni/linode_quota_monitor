Linode Qouta Monitor
--------------------

Monitor your Linode network transfer pool, and shutdown if threshold exceeds limit

```
usage: linode_qouta_monitor.py [-h] [-t THRESHOLD] [linode_id]

positional arguments:
  linode_id             the ID of the Linode to shutdown

optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        threshold percentage

examples:
        ./linode_qouta_monitor.py 12345678
        ./linode_qouta_monitor.py 12345678 -t 90
```

#### Sample Output

```
$ ./linode_quota_monitor.py 13672302 --threshold 50
used: 0.08% billable: 0 actual used: 2 quota: 2369 threshold: 50.0%
```

#### Suggest Using with Crontab

```
#run every 5 minutes
5 * * * * ./linode_quota_monitor.py 12345678 --threshold 90 >/dev/null 2>&1
```
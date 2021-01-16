# A simple network monitor

I need to know if my ISP is behaving.

Speedtest has a very simple package that will allow me to test my ISP's
speed. It's a prerequisite:

```
sudo apt install speedtest-cli
```

I want to quickly visualize what my network bandwidth looks like.

I auditioned Adafruit.io's visualization service: the Python API did not
work for me, and forum help was entirely unforthcoming. I might come back
to it, but that's where it is.

I tried ThingBoard, and it worked. However, it's excruciatingly complicated
to use their cloud service. That's OK - it's intended for monitoring
fleets and fleets of IOT things, not a single thing, which is what I'm doing.
The cloud service seems to start at $10/month.

DataDog seems to have a service too. I think it starts at $5/device/month,
which is cheaper. Wading through their doc was also a little tough.

I've considered a means to post to a google docs spreadsheet. In some sense
that would be perfect, I can visualize the doc however I want.

Looking forward to other ideas. 

## Bandwidth

It appears each Speedtest takes 5MB, and I don't think I can change it.

My Comcast bandwidth cap is currently 1.5TB/month.

Let's say I'm willing to spend 50GB/month in testing. That means 10,000 data
points per month. There are 720 hours in a month, which means I can test about 10 times
an hour and stay within the rough limit. 10 times per hour is about 6 minutes,
so 5 minutes should be about OK.

## Todos

It would be better to configure the frequency instead of editing the python file.

It would be better to have different providers.

It would be better to also log the data points with metadata like the speedtest
server, so one could go back and see if there's a correlation between the 
speedtest server and poor results.

## Cookbook

Make sure the repo is at /home/pi/netmon. If it isn't, then go in and
edit netmon.service to point to the right place.

Copy the credential into the python file.


Since we're going to try to log and not be root, make the log file
writable.

```
sudo touch /var/log/netmon.log
sudo chmod a+w /var/log/netmon.log
```

Copy netmon.service to /etc/systemd/system

```
sudo systemctl start netmon.service
sudo systemctl enable netmon.service
```


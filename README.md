
# Table of Contents
[[_TOC_]]

# Contributors
David R. Trask @firewallzer0

Ryan Chen @ryanscodebay

# Pre-requisites:
* pip install discord
* pip install influxdb

# Task List
- [x] Basic Discord Bot that response to users and commands
- [ ] Poll Basic Server Stats
  - [ ] TrueNAS Basic Stats
  - [x] VMware Basic Stats
    - [ ] Number of powered on VMs
    - [x] Uptime
    - [x] Cluster CPU utilization
    - [x] Cluster RAM utilization
    - [x] Cluster Power usage  
  - [ ] pfSense Basic Stats
    - [ ] CPU utilization
    - [ ] Memory utilization
    - [ ] Bandwidth utilization
    - [x] (Run Speed Test and return results) OR (Get the latest results from scheduled script)
- [x] Write InfluxDB poller
- [x] Write webhook caller
- [ ] Re-write to include json config file
# Process Utilities

*I wrote this as part of an Azure Functions app for a client project. I found the modules to be useful (particularly kill_process), so I have changed logging.info() to print() and saved for personal use.*

**```kill_process``` Notes**


kill_process takes 3 arguments:

1. process_name: string, required
2. kill -> boolean, required
3. time_limit-> integer (minutes0, optional (default: 60)

Syntax examples:

```process_utilities.kill_process('chromedriver', True)```

- kills active 'chromedriver' processes with uptime > 60 minutes (default is 60 minutes)```

```process_utilities.kill_process('chromedriver', True, 15)```

- kills active 'chromedriver' processes with uptime > 15 minutes

```process_utilities.kill_process('chromedriver', False)```

- produces logging statements to give info on 'chromedriver' proceses

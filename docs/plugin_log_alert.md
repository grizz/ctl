# Sending log alerts

Use the `log_alert` plugin to send alert notifications on specific logging levels.

```yaml
ctl:
  plugins:

    # we will use an instance of the `email` plugin to
    # handle our alerts
    - name: email_errors
      type: email
      config:
        subject: "Error Alert"
        sender: vegu@dev2.20c.com
        recipients:
          - vegu@vegui.org


    # The `log_alert` plugin can attach to one or more python
    # loggers we have set up and collect messages from it according
    # to the levels we specify
    - name: log_error_alert
      type: log_alert
      config:
        # attach to these loggers
        loggers:
          - logger: ctl
      events:
        # on CTL exit event we want to trigger the alert
        exit:
          alert:
            # trigger if any of these levels were logged
            - levels:
                - critical
                - error
              # we want to use the `email_errors` plugin instance
              # to send the alert message
              plugin: email_errors
```

## Output levels different than trigger levels

In some cases it may be useful to include other log levels in the output log while still only triggering the alert on other log levels.

In the next example we trigger on `error` logs, but will include `debug` level logging in our output message


```yaml
    # The `log_alert` plugin can attach to one or more python
    # loggers we have set up and collect messages from it according
    # to the levels we specify
    - name: log_error_alert
      type: log_alert
      config:
        # attach to these loggers
        loggers:
          - logger: ctl
      events:
        # on CTL exit event we want to trigger the alert
        exit:
          alert:
            # trigger if any of these levels were logged
            - levels:
                - critical
                - error
            - output_levels:
                - critical
                - error
                - debug
              # we want to use the `email_errors` plugin instance
              # to send the alert message
              plugin: email_errors
```



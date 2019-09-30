# Configuring the email plugin

The email plugin can be setup like this

It allows configuration of default values for subject, sender and recipients as well as SMTP configuration.

Emails can be sent on CTL events

```yaml
ctl:
  plugins:
    - name: email_test
      type: email
      config:
        subject: "Test email"
        sender: vegu@dev2.20c.com
        recipients:
          - vegu@vegui.org
      events:
        # on ctl exit
        exit:
          # send this email
          send:
            - body: "test"
```

In `send` values for `subject`, `sender` and `recipients` can be overwritten as well

```yaml
ctl:
  plugins:
    - name: email_test
      type: email
      config:
        subject: "Test email"
        sender: vegu@dev2.20c.com
        recipients:
          - vegu@vegui.org
      events:
        # on ctl exit
        exit:
          # send this email
          send:
            - body: "test"
              subject: "Something else"
              recipients:
                - "john.smith@localhost"
```

Provide SMTP configuration

```yaml
ctl:
  plugins:
    - name: email_test
      type: email
      config:
        subject: "Test email"
        sender: vegu@dev2.20c.com
        recipients:
          - vegu@vegui.org
        smtp:
          host: mail.myhost.com
```


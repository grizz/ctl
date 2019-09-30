from __future__ import absolute_import

import ctl
import confu.schema
import smtplib

from ctl.plugins import PluginBase
from ctl.config import SMTPConfigSchema

from email.mime.text import MIMEText


class EmailPluginConfig(confu.schema.Schema):
    subject = confu.schema.Str()
    sender = confu.schema.Email()
    recipients = confu.schema.List(item=confu.schema.Email(),
                                   help="list of recipient addresses")
    smtp = SMTPConfigSchema


@ctl.plugin.register("email")
class EmailPlugin(PluginBase):
    class ConfigSchema(PluginBase.ConfigSchema):
        config = EmailPluginConfig

    #XXX smtp default config exists in here, but doesnt
    #end up in self.config for some reason?
    defaults = confu.generator.generate(ConfigSchema)

    def init(self):
        #XXX need to do it like this until the defaults issue
        # is resolved
        smtp_host = self.config.get("smtp",{}).get("host","localhost")
        self.smtp = smtplib.SMTP(smtp_host)

    def alert(self, message):
        return self.send(message)

    def send(self, body, **kwargs):
        subject = kwargs.get("subject", self.config.get("subject"))
        recipients = kwargs.get("recipients", self.config.get("recipients",[]))
        sender = kwargs.get("sender", self.config.get("sender"))
        for recipient in recipients:
            self._send(body, subject, sender, recipient)


    def _send(self, body, subject, sender, recipient, **kwargs):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        self.log.debug("SENDING {} from {} to {}".format(subject,
                                                         sender,
                                                         recipient))
        if kwargs.get("test_mode"):
            return msg

        self.smtp.sendmail(sender, recipient, msg.as_string())


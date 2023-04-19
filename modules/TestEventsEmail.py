"""
eventu su email json nuskaitymas
# Eventai su el. pastu yra netestuoti
            if (test["event-data"]["email-config"]["email-acc"] != ""):
                data = json.dumps({
                    ".type": "rule",
                    "enable": "1",
                    "event": test["event-data"]["event-type"],
                    "eventMark": subtype,
                    "message": test["event-data"]["message"][index],
                    "action": "sendEmail",
                    "subject": test["event-data"]["email-config"]["subject"],
                    "recipEmail": test["event-data"]["email-config"]["recievers"],
                    "emailgroup": test["event-data"]["email-config"]["email-acc"]
                })
"""
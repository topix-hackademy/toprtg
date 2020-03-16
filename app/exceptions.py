
class SNMPException(Exception):
    def __init__(self, message, *errors):
        base_err = "SNMP Exception"
        message = [base_err, message]
        if errors is not None:
            message += [str(x) for x in errors]
        self.message = " | ".join(message)

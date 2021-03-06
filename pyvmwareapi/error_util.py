# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Exception classes and SOAP response error checking module.
"""

FAULT_NOT_AUTHENTICATED = "NotAuthenticated"
FAULT_ALREADY_EXISTS = "AlreadyExists"


class VimException(Exception):
    """The VIM Exception class."""

    def __init__(self, exception_summary, excep):
        Exception.__init__(self)
        self.exception_summary = exception_summary
        self.exception_obj = excep

    def __str__(self):
        return self.exception_summary + str(self.exception_obj)


class SessionOverLoadException(VimException):
    """Session Overload Exception."""
    pass


class VimAttributeError(VimException):
    """VI Attribute Error."""
    pass


class VimFaultException(Exception):
    """The VIM Fault exception class."""

    def __init__(self, fault_list, excep):
        Exception.__init__(self)
        self.fault_list = fault_list
        self.exception_obj = excep

    def __str__(self):
        return str(self.exception_obj)


class FaultCheckers(object):
    """
    Methods for fault checking of SOAP response. Per Method error handlers
    for which we desire error checking are defined. SOAP faults are
    embedded in the SOAP messages as properties and not as SOAP faults.
    """

    def retrieveproperties_fault_checker(resp_obj):
        """
        Checks the RetrieveProperties response for errors. Certain faults
        are sent as part of the SOAP body as property of missingSet.
        For example NotAuthenticated fault.
        """
        fault_list = []
        if not resp_obj:
            # This is the case when the session has timed out. ESX SOAP server
            # sends an empty RetrievePropertiesResponse. Normally missingSet in
            # the returnval field has the specifics about the error, but that's
            # not the case with a timed out idle session. It is as bad as a
            # terminated session for we cannot use the session. So setting
            # fault to NotAuthenticated fault.
            fault_list = ["NotAuthenticated"]
        else:
            for obj_cont in resp_obj:
                if hasattr(obj_cont, "missingSet"):
                    for missing_elem in obj_cont.missingSet:
                        fault_type = missing_elem.fault.fault.__class__
                        # Fault needs to be added to the type of fault for
                        # uniformity in error checking as SOAP faults define
                        fault_list.append(fault_type.__name__)
        if fault_list:
            exc_msg_list = ', '.join(fault_list)
            raise VimFaultException(fault_list, Exception(_("Error(s) %s "
                    "occurred in the call to RetrieveProperties") %
                    exc_msg_list))

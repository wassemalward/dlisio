from .basicobject import BasicObject
from .valuetypes import scalar, vector
from .utils import describe_array, describe_dict

from collections import OrderedDict

class Message(BasicObject):
    """
    Textual messages tied to other data by means of time and/or position of
    tool zero point when the message was recorded

    Attributes
    ----------

    message_type : str
        source and purpose of the message.

    time
        time the message was issued. |crtime|

    borehole_drift
        borehole drift of the tool zero point when message was issued.

    vertical_depth
        vertical depth of the tool zero point when message was issued.

    radial_drift
        radial drift of the tool zero point when message was issued.

    angular_drift
        angular drift of the tool zero point when message was issued.

    text : list(str)
        message(s).

    See also
    --------

    BasicObject : The basic object that Message is derived from

    Notes
    -----

    The Message object reflects the logical record type MESSAGE, described in
    rp66. MESSAGE objects are defined in Appendix A.2 - Logical Record Types,
    described in detail in Chapter 6.1.1 - Transient Data, message objects.
    """
    attributes = {
        'TYPE'           : scalar,
        'TIME'           : scalar,
        'BOREHOLE-DRIFT' : scalar,
        'VERTICAL-DEPTH' : scalar,
        'RADIAL-DRIFT'   : scalar,
        'ANGULAR-DRIFT'  : scalar,
        'TEXT'           : vector,
    }

    def __init__(self, obj = None, name = None, lf = None):
        super().__init__(obj, name = name, type = 'MESSAGE', lf = lf)

    @property
    def message_type(self):
        return self['TYPE']

    @property
    def time(self):
        return self['TIME']

    @property
    def borehole_drift(self):
        return self['BOREHOLE-DRIFT']

    @property
    def vertical_depth(self):
        return self['VERTICAL-DEPTH']

    @property
    def radial_drift(self):
        return self['RADIAL-DRIFT']

    @property
    def angular_drift(self):
        return self['ANGULAR-DRIFT']

    @property
    def text(self):
        return self['TEXT']

    def describe_attr(self, buf, width, indent, exclude):
        d = OrderedDict()
        d['Message type'] = self.message_type
        d['Time of recording'] = self.time

        d['Borehole drift'] = self.borehole_drift
        d['Vertical depth'] = self.vertical_depth
        d['Radial drift']   = self.radial_drift
        d['Angular drift']  = self.angular_drift

        describe_dict(buf, d, width, indent, exclude)
        describe_array(buf, self.text, width, indent)

from .basicobject import BasicObject
from .valuetypes import scalar, vector, reverse, skip
from .linkage import obname, objref
from .utils import *

import logging
import numpy as np


class Computation(BasicObject):
    """
    Results of computations that are more appropriately expressed as static
    information rather than as channels.

    The computation value(s) may be scalars or an array. In
    the later case, the structure of the array is defined in the dimension
    attribute. The zones attribute specifies which zones the computations is
    defined. If there are no zones the computation is defined everywhere.

    The axis attribute, if present, defines axis labels for multidimensional
    value(s).

    See also
    --------

    BasicObject : The basic object that Computation is derived from

    Notes
    -----

    The Computation object reflects the logical record type COMPUTATION,
    defined in rp66.  COMPUTATION objects are listed in Appendix A.2 - Logical
    Record Types, and described in detail in Chapter 5.8.6 - Static and Frame
    Data, COMPUTATION objects.
    """

    attributes = {
        'LONG-NAME' : scalar('long_name'),
        'PROPERTIES': vector('properties'),
        'DIMENSION' : reverse('dimension'),
        'AXIS'      : reverse('axis'),
        'ZONES'     : vector('zones'),
        'SOURCE'    : scalar('source'),
        'VALUES'    : skip()
    }

    linkage = {
        'long-name' : obname('LONG-NAME'),
        'axis'      : obname('AXIS'),
        'zones'     : obname('ZONE'),
        'source'    : objref
    }

    def __init__(self, obj = None, name = None):
        super().__init__(obj, name = name, type = 'COMPUTATION')
        #: Descriptive name of the computation
        self.long_name   = None

        #:Property indicators that summarizes the characteristics of the computation
        #: and the processing that has occurred to produce it
        self.properties  = []

        #: Array structure of a single value
        self.dimension   = []

        #: Coordinate axes of the values
        self.axis        = []

        #: Mutually disjoint zones over which the value of the current
        #: computation is constant
        self.zones       = []

        #: The immediate source of the Computation
        self.source = None

    @property
    def values(self):
        """ Computation values

        Computation value(s) may be scalar or array's. The size/dimensionallity
        of each value is defined in the dimensions attribute.

        Each value may or may not be zoned, i.e. it is only defined in a
        certain zone. If this is the case the first zone, computation.zones[0],
        will correspond to the first value, computation.values[0] and so on.
        If there is no zones, there should only be one value, which is said to
        be unzoned, i.e. it is defined everywere.

        Raises
        ------

        ValueError
            Unable to structure the values based on the information available.

        Returns
        -------

        values : structured np.ndarray

        Notes
        -----

        If dlisio is unable to structure the values due to insufficient or
        contradictory information in the object, an ValueError is raised.  The
        raw array can still be accessed through attic, but note that in this
        case, the semantic meaning of the array is undefined.

        Examples
        --------

        First value:

        >>> computation.values[0]
        [10, 20, 30]

        Zone (if any) where that parameter value is valid:

        >>> computation.zones[0]
        Zone('ZONE-A')
        """
        try:
            values = self.attic['VALUES']
        except KeyError:
            return np.empty(0)

        shape = validshape(values, self.dimension, samplecount=len(self.zones))
        return sampling(values, shape)

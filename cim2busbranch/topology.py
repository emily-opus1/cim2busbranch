import collections


bus_type = collections.namedtuple('BusType', 'PQ, PV, REF, ISOLATED')(
    PQ=1,
    PV=2,
    REF=3,
    ISOLATED=4,
)

Point = collections.namedtuple('Point', 'x, y')


class Bus(object):
    """
    A *Bus* represents a node in a bus/branch network graph.

    """
    def __init__(self, name='', btype=bus_type.PQ, pd=0., qd=0.,
                base_kv=100., vm=1., va=0., vm_max=1.1, vm_min=0.9,
                gs=0., bs=0., area=1, zone=1, cim_classes=None, pos=None):

        self.name = name if name else str(id(self))
        """Bus name"""

        self.btype = btype
        """Bus type (One of these attributes of :obj:`bus_type`:
           *PQ*, *PV*, *REF*, *ISOLATED*)"""

        self.pd = pd
        """Active power demand (MW)"""

        self.qd = qd
        """Reactive power demand (MVAr)"""

        self.base_kv = base_kv
        """Base voltage (kV)"""

        self.vm = vm
        """Voltage magnitude (p.u.)"""

        self.va = va
        """Voltage angle (degrees)"""

        self.vm_max = vm_max
        """maximum voltage magnitude (p.u.)"""

        self.vm_min = vm_min
        """minimum voltage magnitude (p.u.)"""

        self.gs = gs
        """Shunt conductance (MVAr injected at V = 1. p.u.)"""

        self.bs = bs
        """Shunt susceptance (MVAr injected at V = 1. p.u.)"""

        self.area = area
        """Area number (positive integer)"""

        self.zone = zone
        """Loss zone (positive integer)"""

        self.cim_classes = cim_classes if cim_classes else []
        """Classes of CIM components that were connected to this bus."""

        self.pos = pos
        """Set of position points (x, y) of that bus."""

        self._pd_orig = pd
        self._qd_orig = qd

    @property
    def pd_orig(self):
        """The value of ``self.pd`` when the instance was created."""
        return self._pd_orig

    @property
    def qd_orig(self):
        """The value of ``self.qd`` when the instance was created."""
        return self._qd_orig

    def reset(self):
        """
        Resets ``self.pd`` and ``self.qd`` to their original values (that they
        had when the instance was created).

        """
        self.pd = self._pd_orig
        self.qd = self._qd_orig

    def __repr__(self):
        return ('%s(name=%-6s, btype=%d, pd=%7.3f, qd=%7.3f, '
                'vm=%.3f, va=%+.3f)') % (
            type(self).__name__,
            "'%s'" % self.name,
            self.btype,
            self.pd,
            self.qd,
            self.vm,
            self.va,
        )


class Generator(object):
    """
    A *Generator* can be attached to a :class:`Bus`.

    """
    def __init__(self, bus, name='', pg=0., qg=0., pg_min=0., pg_max=0.,
            qg_min=0., qg_max=0., vg=1., base_mva=0., online=True,
            pc1=0., pc2=0., qc1_min=0., qc1_max=0., qc2_min=0., qc2_max=0.,
            ramp_agc=0., ramp_10=0., ramp_30=0., ramp_q=0., apf=0.):

        self.bus = bus
        """Reference to the bus the generator is connected to"""

        self.name = name if name else str(id(self))
        """Generator name"""

        self.pg = pg
        """Real power output (MW)"""

        self.qg = qg
        """Reactive power output (MVAr)"""

        self.pg_min = pg_min
        """Minimum real power output (MW)"""

        # Only raise an error if pg_max was provided by the user
        if 0.0 < pg_max < pg:
            raise ValueError('pg_max must be >= pg, but %f < %f' %
                    (pg_max, pg))
        self.pg_max = max(pg_max, pg)  # enforce pg_max >= pg
        """Maximum real power output (MW)"""

        self.qg_min = qg_min
        """Minimum reactive power output at Pc1 (MVAr)"""

        # Only raise an error if qg_max was provided by the user
        if 0.0 < qg_max < qg:
            raise ValueError('qg_max must be >= qg, but %f < %f' %
                    (qg_max, qg))
        self.qg_max = max(qg_max, qg)  # enforce qg_max >= qg
        """Maximum reactive power output at Pc1 (MVAr)"""

        self.vg = vg
        """Voltage magnitude setpoint (p.u.)"""

        self.base_mva = base_mva
        """Total MVA base of this machine, defaults to baseMVA"""

        self.online = online
        """Status (machine in service (True) or out of service (False))"""

        self.pc1 = pc1
        """Lower real power output of PQ capability curve (MW)"""

        self.pc2 = pc2
        """Upper real power output of PQ capability curve (MW)"""

        self.qc1_min = qc1_min
        """Minimum reactive power output at Pc1 (MVAr)"""

        self.qc1_max = qc1_max
        """Maximum reactive power output at Pc1 (MVAr)"""

        self.qc2_min = qc2_min
        """Minimum reactive power output at Pc2 (MVAr)"""

        self.qc2_max = qc2_max
        """Maximum reactive power output at Pc2 (MVAr)"""

        self.ramp_agc = ramp_agc
        """Ramp rate for load following/AGC (MW/min)"""

        self.ramp_10 = ramp_10
        """Ramp rate for 10 minute reserves (MW)"""

        self.ramp_30 = ramp_30
        """Ramp rate for 30 minute reserves (MW)"""

        self.ramp_q = ramp_q
        """Ramp rate for reactive power (2 sec timescale) (MVAr/min)"""

        self.apf = apf
        """APF, area participation factor"""

        self._pg_orig = pg
        self._qg_orig = qg

    @property
    def pg_orig(self):
        """The value of ``self.pg`` when the instance was created."""
        return self._pg_orig

    @property
    def qg_orig(self):
        """The value of ``self.qg`` when the instance was created."""
        return self._qg_orig

    def reset(self):
        """
        Resets ``self.pg`` and ``self.qg`` to their original values (that they
        had when the instance was created).

        """
        self.pg = self._pg_orig
        self.qg = self._qg_orig

    def __repr__(self):
        return ('%s(name=%-6s, bus=%-6s, pg=%7.3f, qg=%7.3f)') % (
            type(self).__name__,
            "'%s'" % self.name,
            "'%s'" % self.bus.name,
            self.pg,
            self.qg,
        )


class Branch(object):
    """
    A *Branch* represents a vertex in a Bus/Branch network.

    """
    def __init__(self, from_bus, to_bus, name='', r=0., x=0., b=0.,
            rate_a=999., rate_b=999., rate_c=999., ratio=0., angle=0.,
            angle_min=-360., angle_max=360., online=True,
            p_from=0., q_from=0., p_to=0., q_to=0.):

        self.from_bus = from_bus
        """Reference to the bus on the from-side"""

        self.to_bus = to_bus
        """Reference to the bus on the to-side"""

        self.name = name if name else str(id(self))
        """Branch name"""

        self.r = r
        """Resistance (p.u.)"""

        self.x = x
        """Reactance (p.u.)"""

        self.b = b
        """Total line charging susceptance (p.u.)"""

        self.rate_a = rate_a
        """MVA rating A (long term rating)"""

        self.rate_b = rate_b
        """MVA rating B (short term rating)"""

        self.rate_c = rate_c
        """MVA rating C (emergency rating)"""

        self.ratio = ratio
        """Transformer off nominal turns ratio (=0 for lines)"""

        self.angle = angle
        """Transformer phase shift angle (degree, positive => delay)"""

        self.angle_min = angle_min
        """Minimum angle difference between both ends
           (from_bus.va - to_bus.va) (degree)"""

        self.angle_max = angle_max
        """Maximum angle difference between both ends
           (from_bus.va - to_bus.va) (degree)"""

        self.online = online
        """Initial branch status (in service (True) or
           out of service (False))"""

        self.p_from = p_from
        """Real power injected at "from" bus end (MW)"""

        self.q_from = q_from
        """Reactive power injected at "from" bus end (MVAr)"""

        self.p_to = p_to
        """Real power injected at "to" bus end (MW)"""

        self.q_to = q_to
        """Reactive power injected at "to" bus end (MVAr)"""

    def __repr__(self):
        return ('%s(name=%-6s, from_bus=%-6s, to_bus=%-6s, p_from=%+8.3f, '
                'q_from=%+8.3f, p_to=%+8.3f, q_to=%+8.3f)') % (
            type(self).__name__,
            "'%s'" % self.name,
            "'%s'" % self.from_bus.name,
            "'%s'" % self.to_bus.name,
            self.p_from,
            self.q_from,
            self.p_to,
            self.q_to,
        )


class Case(object):
    """
    *Case* is a container for :class:`Bus`es, :class:`Generator`s and
    :class:`Branch`es.

    It also holds the global *base_mva* attribute for the case.

    """
    def __init__(self, base_mva, buses, generators, branches):
        self.base_mva = base_mva
        self.buses = buses
        self.generators = generators
        self.branches = branches

        self.bus_ids = {}  # Gets updated whenever a pypower case is created

    def reset(self):
        """
        Resets all buses and generators.

        """
        for item in self.buses + self.generators:
            item.reset()

    def __repr__(self):
        lists = [self.buses, self.generators, self.branches]
        reprs = ['\n'.join(['    %s,' % i for i in li]) for li in lists]
        reprs = ['[\n%s\n]' % rep for rep in reprs]

        return ('<%s object \n  base_mva=%s,\n  buses=%s,\n generators=%s,\n'
                '  branches=%s>') % (
            type(self).__name__,
            self.base_mva,
            reprs[0],
            reprs[1],
            reprs[2],
        )
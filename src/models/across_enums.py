from enum import IntEnum
from sqlalchemy import Enum

class PSQLTableEnum:

    @classmethod
    def table_name(cls):
        return cls.__name__

    @classmethod
    def to_psql_enum(cls, nullable=False):
        val = tuple([x.name for x in cls])
        e = Enum(
            *val,
            name = cls.table_name(),
            nullable = nullable
        )
        return e


class MissionType(PSQLTableEnum, IntEnum):
    pointed = 1
    survey = 2

    def table_name():
        return "mission_type"


class ObservatoryType(PSQLTableEnum, IntEnum):
    space_based = 1
    ground_based = 2

    def table_name():
        return "observatory_type"
    

class ScheduleStatus(PSQLTableEnum, IntEnum):
    planned = 1
    completed = 2
    canceled = 3

    def table_name():
        return "schedule_status"


class ScheduleType(PSQLTableEnum, IntEnum):
    low_fidelity = 1
    high_fidelity = 2
    as_executed = 3

    def table_name():
        return "schedule_type"

class ObservationStatus(PSQLTableEnum, IntEnum):
    planned = 1
    completed = 2
    canceled = 3

    def table_name():
        return "observation_status"

class ObservationType(PSQLTableEnum, IntEnum):
    photometric = 1
    spectroscopic = 2

    def table_name():
        return "observation_type"

class DepthUnit(PSQLTableEnum, IntEnum):
    ab_mag = 1
    vega_mag = 2
    flux_erg = 3
    flux_jy = 4


    def table_name():
        return "depth_unit"
    
    def __str__(self):
        split_name = str(self.name).split('_')
        return str.upper(split_name[0]) + ' ' + split_name[1]


class wavelength_units(IntEnum):
    nanometer = 1
    angstrom = 2
    micron = 3

    @staticmethod
    def get_scale(unit):
        if unit == wavelength_units.nanometer:
            return 10.0
        if unit == wavelength_units.angstrom:
            return 1.0
        if unit == wavelength_units.micron:
            return 10000.0


class energy_units(IntEnum):
    eV = 1
    keV = 2
    MeV = 3
    GeV = 4
    TeV = 5

    @staticmethod
    def get_scale(unit):
        if unit == energy_units.eV:
            return 1.0
        if unit == energy_units.keV:
            return 1000.0
        if unit == energy_units.MeV:
            return 1000000.0
        if unit == energy_units.GeV:
            return 1000000000.0
        if unit == energy_units.TeV:
            return 1000000000000.0


class frequency_units(IntEnum):
    Hz = 1
    kHz = 2
    GHz = 3
    MHz = 4
    THz = 5

    @staticmethod
    def get_scale(unit):
        if unit == frequency_units.Hz:
            return 1.0
        if unit == frequency_units.kHz:
            return 1000.0
        if unit == frequency_units.MHz:
            return 1000000.0
        if unit == frequency_units.GHz:
            return 1000000000.0
        if unit == frequency_units.THz:
            return 1000000000000.0

from enum import IntEnum

class mission_type(IntEnum):
    pointed = 1
    survey = 2


class observatory_type(IntEnum):
    space_based = 1
    ground_based = 2


class schedule_status(IntEnum):
    planned = 1
    completed = 2
    canceled = 3


class schedule_type(IntEnum):
    low_fidelity = 1
    high_fidelity = 2
    as_executed = 3


class observation_status(IntEnum):
    planned = 1
    completed = 2
    canceled = 3


class observation_type(IntEnum):
    photometric = 1
    spectroscopic = 2


class depth_unit(IntEnum):
    ab_mag = 1
    vega_mag = 2
    flux_erg = 3
    flux_jy = 4

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

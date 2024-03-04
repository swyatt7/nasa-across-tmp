from typing import List
from sqlalchemy import (
    Column, String, Integer, Date, Enum, ForeignKey, Float, JSON
)
from sqlalchemy.orm import Mapped, relationship, mapped_column
from geoalchemy2 import Geography

from .db_base import Base
from .across_enums import (
    ObservatoryType,
    ScheduleStatus,
    ScheduleType,
    ObservationStatus,
    ObservationType,
    DepthUnit
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)
    name = Column(String)


class Observatory(Base):
    __tablename__ = "observatory"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)
    name = Column(String)
    observatory_type = Column(ObservationType.to_psql_enum())
    telescopes: Mapped[List["Telescope"]] = relationship(back_populates="observatory")


class Telescope(Base):
    __tablename__ = "telescope"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)
    name = Column(String)
    observatory_id: Mapped[int] = mapped_column(ForeignKey(Observatory.id))
    observatory: Mapped["Observatory"] = relationship(back_populates="telescopes")
    instruments: Mapped[List["Instrument"]] = relationship(back_populates="telescope")


class Instrument(Base):
    __tablename__ = "instrument"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)
    name = Column(String)
    telescope_id: Mapped[int] = mapped_column(ForeignKey(Telescope.id))
    telescope: Mapped["Telescope"] = relationship(back_populates="instruments")
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="instrument")


class Footprint(Base):
    __tablename__ = "footprint"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)
    name = Column(String)
    schedule_status = Column(ScheduleStatus.to_psql_enum())
    schedule_type = Column(ScheduleType.to_psql_enum())
    instrument_id = mapped_column(ForeignKey(Instrument.id))
    instrument: Mapped["Instrument"] = relationship(back_populates="schedules")
    observations: Mapped[List["Observation"]] = relationship(back_populates="schedule")


class Observation(Base):
    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)
    datecreated = Column(Date)
    object_name = Column(String)
    object_position = Column(Geography("POINT", srid=4326))
    object_observation_reasion = Column(String)
    proposal_reference = Column(String)
    pointed_position = Column(Geography("POINT", srid=4326))
    obstime_start = Column(Date)
    obstime_end = Column(Date)
    exposure_time = Column(Float)
    observation_status = Column(ObservationStatus.to_psql_enum())
    schedule_id: Mapped[int] = mapped_column(ForeignKey(Schedule.id))
    schedule: Mapped["Schedule"] = relationship(back_populates="observations")
    observation_type = Column(ObservationType.to_psql_enum())
    photometric_observation: Mapped["PhotometricObservation"] = relationship(back_populates="observation")
    spectroscopic_observation: Mapped["SpectroscopicObservation"] = relationship(back_populates="observation")


class PhotometricObservation(Observation, Base):
    __tablename__ = "photometric_observavation"

    id = Column(Integer, primary_key=True)
    depth = Column(Float, nullable=True)
    depth_error = Column(Float, nullable=True)
    depth_unit = Column(DepthUnit.to_psql_enum(nullable=True))
    position_angle = Column(Float)
    central_wavelength = Column(Float)
    bandwidth = Column(Float)
    filter_name = Column(String)
    other_information = Column(JSON)
    observation_id: Mapped[int] = mapped_column(ForeignKey(Observation.id))
    observation: Mapped["Observation"] = relationship(back_populates="photometric_observation")


class SpectroscopicObservation(Observation, Base):
    __tablename__ = "spectroscopic_observation"

    id = Column(Integer, primary_key=True)
    observation_id: Mapped[int] = mapped_column(ForeignKey(Observation.id))
    observation: Mapped["Observation"] = relationship(back_populates="spectroscopic_observation")
    other_information = Column(JSON)

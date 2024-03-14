from typing import List
from sqlalchemy import (
    Column, Table, Boolean, String, Integer, DateTime, ForeignKey, Float, JSON
)
from sqlalchemy.orm import Mapped, relationship, mapped_column
from geoalchemy2 import Geography
import secrets
import hashlib
import jwt
from time import time

from ...across_config import config
from .db_base import Base, session
from .across_enums import (
    UserRoleType,
    ObservatoryType,
    ScheduleStatus,
    ScheduleType,
    ObservationStatus,
    ObservationType,
    DepthUnit
)

user_role_association_table = Table(
    "user_role_association_table",
    Base.metadata,
    Column("userid", ForeignKey("users.id"), primary_key=True),
    Column("roleid", ForeignKey("userrole.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    firstname = Column(String(25))
    lastname = Column(String(25))
    email = Column(String(100))
    password_hash = Column(String(128))
    api_token = Column(String(128))
    verification_key = Column(String(128))
    verified = Column(Boolean)
    roles: Mapped[List["UserRole"]] = relationship(
        secondary=user_role_association_table, back_populates="users"
    )


    def set_password(self, password):
        self.password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()


    def check_password(self, password):
        input_password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()
        return self.password_hash == input_password_hash


    def set_apitoken(self):
        self.api_token = secrets.token_urlsafe(28)


    def check_apitoken(self, token):
        return token == self.api_token


    def set_verification_key(self):
        self.verification_key = secrets.token_urlsafe(28)
    

    def check_verification_key(self, verification_key):
        return verification_key == self.verification_key


    def get_reset_password_token(self, expires_in=3600):
        jwt_package = {'reset_password': self.id, 'exp': time() + expires_in}
        return jwt.encode(
            jwt_package,
            config['SECRET_KEY'],
            algorithm='HS256'
        )


    @staticmethod
    def verify_reset_password_token(token):
        try:
            package = jwt.decode(
                token, 
                config['SECRET_KEY'],
                algorithms=['HS256']
            )
            _id = package['reset_password']
        except:  # noqa: E722
            return
        return session.query(User).filter(User.id == _id).first()


    @staticmethod
    def api_scope_validate(api_token: str, scope: UserRoleType):
        role = session.query(UserRole).filter(
            UserRole.name == scope.name
        ).first()

        user = session.query(
            User
        ).filter(
            User.api_token == api_token,
            User.roles.any(
                UserRole.name.in_(
                    [role.name, UserRoleType.admin.name]
                )
            )
        ).first()
        
        return user is not None
    

class UserRole(Base):
    __tablename__ = "userrole"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    name = Column(UserRoleType.to_psql_enum())
    users: Mapped[List["User"]] = relationship(
        secondary=user_role_association_table, back_populates="roles"
    )


class Observatory(Base):
    __tablename__ = "observatory"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    name = Column(String)
    observatory_type = Column(ObservatoryType.to_psql_enum())
    telescopes: Mapped[List["Telescope"]] = relationship(back_populates="observatory")


class Telescope(Base):
    __tablename__ = "telescope"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    name = Column(String)
    observatory_id: Mapped[int] = mapped_column(ForeignKey(Observatory.id))
    observatory: Mapped["Observatory"] = relationship(back_populates="telescopes")
    instruments: Mapped[List["Instrument"]] = relationship(back_populates="telescope")


class Instrument(Base):
    __tablename__ = "instrument"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    name = Column(String)
    telescope_id: Mapped[int] = mapped_column(ForeignKey(Telescope.id))
    telescope: Mapped["Telescope"] = relationship(back_populates="instruments")
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="instrument")


class Footprint(Base):
    __tablename__ = "footprint"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    name = Column(String)
    schedule_status = Column(ScheduleStatus.to_psql_enum())
    schedule_type = Column(ScheduleType.to_psql_enum())
    instrument_id = mapped_column(ForeignKey(Instrument.id))
    instrument: Mapped["Instrument"] = relationship(back_populates="schedules")
    observations: Mapped[List["Observation"]] = relationship(back_populates="schedule")


class Observation(Base):
    __tablename__ = "observation"

    id = Column(Integer, primary_key=True)
    datecreated = Column(DateTime)
    object_name = Column(String)
    object_position = Column(Geography("POINT", srid=4326))
    object_observation_reasion = Column(String)
    proposal_reference = Column(String)
    pointed_position = Column(Geography("POINT", srid=4326))
    obstime_start = Column(DateTime)
    obstime_end = Column(DateTime)
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

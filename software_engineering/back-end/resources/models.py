from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects import mysql
from resources.config import FREE_QUOTA_PER_MINUTE

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    max_quota = db.Column(db.Integer, nullable=False, default=FREE_QUOTA_PER_MINUTE)
    current_quota = db.Column(db.Integer, nullable=False, default=FREE_QUOTA_PER_MINUTE)
    access_time = db.Column(db.Integer, nullable=False)

    userBillingPlan = db.relationship('UserBillingPlan', passive_deletes=True, backref=db.backref('User', lazy='joined'))

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, text):
        self.password_hash = bcrypt.generate_password_hash(text)

    def is_correct_password(self, text):
        return bcrypt.check_password_hash(self.password, text)


class AggregatedGenerationPerType(db.Model):
    __tablename__ = 'aggreggatedGenerationPerType'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    ActionTaskID = db.Column(db.BigInteger, nullable=False)
    Status = db.Column(db.String(2))
    Year = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Integer, nullable=False)
    Day = db.Column(db.Integer, nullable=False)
    DateTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    AreaName = db.Column(db.String(200))
    UpdateTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    ActualGenerationOutput = db.Column(db.Numeric(24, 2), nullable=False)
    ActualConsuption = db.Column(db.Numeric(24, 2), nullable=False)
    AreaTypeCodeId = db.Column(db.Integer, db.ForeignKey('areaTypeCode.Id'))
    AreaCodeId = db.Column(db.Integer, db.ForeignKey('allocatedEICDetail.Id'), nullable=False)
    ResolutionCodeId = db.Column(db.Integer, db.ForeignKey('resolutionCode.Id'))
    MapCodeId = db.Column(db.Integer, db.ForeignKey('mapCode.Id'))
    ProductionTypeId = db.Column(db.Integer, db.ForeignKey('productionType.Id'))
    RowHash = db.Column(db.String(255))


class DayAheadTotalLoadForecast(db.Model):
    __tablename__ = 'dayAheadTotalLoadForecast'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    ActionTaskID = db.Column(db.BigInteger, nullable=False)
    Status = db.Column(db.String(2))
    Year = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Integer, nullable=False)
    Day = db.Column(db.Integer, nullable=False)
    DateTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    AreaName = db.Column(db.String(200))
    UpdateTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    TotalLoadValue = db.Column(db.Numeric(24, 2), nullable=False)
    AreaTypeCodeId = db.Column(db.Integer, db.ForeignKey('areaTypeCode.Id'))
    AreaCodeId = db.Column(db.Integer, db.ForeignKey('allocatedEICDetail.Id'), nullable=False)
    ResolutionCodeId = db.Column(db.Integer, db.ForeignKey('resolutionCode.Id'))
    MapCodeId = db.Column(db.Integer, db.ForeignKey('mapCode.Id'))
    RowHash = db.Column(db.String(255))


class ActualTotalLoad(db.Model):
    __tablename__ = 'actualTotalLoad'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    ActionTaskID = db.Column(db.BigInteger, nullable=False)
    Status = db.Column(db.String(2))
    Year = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Integer, nullable=False)
    Day = db.Column(db.Integer, nullable=False)
    DateTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    AreaName = db.Column(db.String(200))
    UpdateTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    TotalLoadValue = db.Column(db.Numeric(24, 2), nullable=False)
    AreaTypeCodeId = db.Column(db.Integer, db.ForeignKey('areaTypeCode.Id'))
    AreaCodeId = db.Column(db.Integer, db.ForeignKey('allocatedEICDetail.Id'), nullable=False)
    ResolutionCodeId = db.Column(db.Integer, db.ForeignKey('resolutionCode.Id'))
    MapCodeId = db.Column(db.Integer, db.ForeignKey('mapCode.Id'))
    RowHash = db.Column(db.String(255))

class MapCode(db.Model):
    __tablename__ = 'mapCode'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    MapCodeText = db.Column(db.String(255), nullable=False, unique=True)
    MapCodeNote = db.Column(db.String(255))

    aggreggatedGenerationsPerType = db.relationship('AggregatedGenerationPerType', backref='MapCode')
    dayAheadTotalLoadsForecast = db.relationship('DayAheadTotalLoadForecast', backref='MapCode')
    actualTotalLoads = db.relationship('ActualTotalLoad', backref='MapCode')


class ResolutionCode(db.Model):
    __tablename__ = 'resolutionCode'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    ResolutionCodeText = db.Column(db.String(255), nullable=False, unique=True)
    ResolutionCodeNote = db.Column(db.String(255))

    aggreggatedGenerationsPerType = db.relationship('AggregatedGenerationPerType', backref='ResolutionCode')
    dayAheadTotalLoadsForecast = db.relationship('DayAheadTotalLoadForecast', backref='ResolutionCode')
    actualTotalLoads = db.relationship('ActualTotalLoad', backref='ResolutionCode')


class AreaTypeCode(db.Model):
    __tablename__ = 'areaTypeCode'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    AreaTypeCodeText = db.Column(db.String(255), nullable=False, unique=True)
    AreaTypeCodeNote = db.Column(db.String(255))

    aggreggatedGenerationsPerType = db.relationship('AggregatedGenerationPerType', backref='AreaTypeCode')
    dayAheadTotalLoadsForecast = db.relationship('DayAheadTotalLoadForecast', backref='AreaTypeCode')
    actualTotalLoads = db.relationship('ActualTotalLoad', backref='AreaTypeCode')


class ProductionType(db.Model):
    __tablename__ = 'productionType'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    ProductionTypeText = db.Column(db.String(255), nullable=False, unique=True)
    ProductionTypeNote = db.Column(db.String(255))

    aggreggatedGenerationsPerType = db.relationship('AggregatedGenerationPerType', backref='ProductionType')


class AllocatedEICDetail(db.Model):
    __tablename__ = 'allocatedEICDetail'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntityCreatedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    EntityModifiedAt = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    MRID = db.Column(db.String(250))
    DocStatusValue = db.Column(db.String(250))
    AttributeInstanceComponent = db.Column(db.String(250))
    LongNames = db.Column(db.String(250))
    DisplayNames = db.Column(db.String(250))
    LastRequestDateAndOrTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    DeactivateRequestDateAndOrTime = db.Column(mysql.TIMESTAMP(fsp=6), nullable=True)
    MarketParticipantStreetAddressCountry = db.Column(db.String(250))
    MarketParticipantACERCode = db.Column(db.String(250))
    MarketParticipantVATCode = db.Column(db.String(250))
    Description = db.Column(db.String(255))
    EICParentMarketDocumentMRID = db.Column(db.String(250))
    ELCResponsibleMarketParticipantMRID = db.Column(db.String(250))
    IsDeleted = db.Column(db.Boolean, nullable=False)

    aggreggatedGenerationsPerType = db.relationship('AggregatedGenerationPerType', backref='AllocatedEICDetail')
    dayAheadTotalLoadsForecast = db.relationship('DayAheadTotalLoadForecast', backref='AllocatedEICDetail')
    actualTotalLoads = db.relationship('ActualTotalLoad', backref='AllocatedEICDetail')


class LoggedOutTokens(db.Model):
    __tablename__ = 'loggedOutTokens'

    jti = db.Column(db.String(128), primary_key=True, autoincrement=False)
    exp = db.Column(db.Integer, nullable=False)


class BillingPlan(db.Model):
    __tablename__ = 'billingPlan'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    plan = db.Column(db.String(16), nullable=False, unique=True)
    description = db.Column(db.Text)
    max_quota = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    userBillingPlan = db.relationship('UserBillingPlan', backref='BillingPlan')


class UserBillingPlan(db.Model):
    __tablename__ = 'userBillingPlan'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchasedAt = db.Column(db.Integer, nullable=False) # number of seconds since the Epoch
    userId = db.Column(db.Integer, db.ForeignKey('user.Id', ondelete='CASCADE'), nullable=False)
    billingPlanId = db.Column(db.Integer, db.ForeignKey('billingPlan.Id'), nullable=False)

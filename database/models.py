# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 30, 2025 22:42:39
# Database: sqlite:////tmp/tmp.qpnLTAs2c6-01JJWP0GZZ5H52J80TYT7MAXS0/Auto_Insurance_System_Model/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class Agent(Base):  # type: ignore
    """
    description: Represents an insurance agent who manages applications and policies.
    """
    __tablename__ = 'agent'
    _s_collection_name = 'Agent'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    AgentAssignmentList : Mapped[List["AgentAssignment"]] = relationship(back_populates="agent")



class Customer(Base):  # type: ignore
    """
    description: Represents a customer who can apply for auto insurance.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(Date)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    IncidentReportList : Mapped[List["IncidentReport"]] = relationship(back_populates="claimant")
    InsuranceApplicationList : Mapped[List["InsuranceApplication"]] = relationship(back_populates="customer")
    VehicleList : Mapped[List["Vehicle"]] = relationship(back_populates="customer")



class Incident(Base):  # type: ignore
    """
    description: Represents an incident for which an insurance claim can be made.
    """
    __tablename__ = 'incident'
    _s_collection_name = 'Incident'  # type: ignore

    id = Column(Integer, primary_key=True)
    incident_date = Column(Date, nullable=False)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    IncidentReportList : Mapped[List["IncidentReport"]] = relationship(back_populates="incident")



class IncidentReport(Base):  # type: ignore
    """
    description: A report filed for an associated incident.
    """
    __tablename__ = 'incident_report'
    _s_collection_name = 'IncidentReport'  # type: ignore

    id = Column(Integer, primary_key=True)
    report_date = Column(Date, nullable=False)
    incident_id = Column(ForeignKey('incident.id'))
    claimant_id = Column(ForeignKey('customer.id'))

    # parent relationships (access parent)
    claimant : Mapped["Customer"] = relationship(back_populates=("IncidentReportList"))
    incident : Mapped["Incident"] = relationship(back_populates=("IncidentReportList"))

    # child relationships (access children)



class InsuranceApplication(Base):  # type: ignore
    """
    description: Represents the auto insurance application submitted by customers.
    """
    __tablename__ = 'insurance_application'
    _s_collection_name = 'InsuranceApplication'  # type: ignore

    id = Column(Integer, primary_key=True)
    application_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    customer_id = Column(ForeignKey('customer.id'))

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("InsuranceApplicationList"))

    # child relationships (access children)
    AgentAssignmentList : Mapped[List["AgentAssignment"]] = relationship(back_populates="insurance_application")
    PolicyList : Mapped[List["Policy"]] = relationship(back_populates="insurance_application")



class Vehicle(Base):  # type: ignore
    """
    description: Represents a vehicle owned by a customer eligible for insurance.
    """
    __tablename__ = 'vehicle'
    _s_collection_name = 'Vehicle'  # type: ignore

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    customer_id = Column(ForeignKey('customer.id'))

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("VehicleList"))

    # child relationships (access children)



class AgentAssignment(Base):  # type: ignore
    """
    description: Represents the assignment of agents to specific insurance applications.
    """
    __tablename__ = 'agent_assignment'
    _s_collection_name = 'AgentAssignment'  # type: ignore

    id = Column(Integer, primary_key=True)
    assignment_date = Column(Date, nullable=False)
    agent_id = Column(ForeignKey('agent.id'))
    insurance_application_id = Column(ForeignKey('insurance_application.id'))

    # parent relationships (access parent)
    agent : Mapped["Agent"] = relationship(back_populates=("AgentAssignmentList"))
    insurance_application : Mapped["InsuranceApplication"] = relationship(back_populates=("AgentAssignmentList"))

    # child relationships (access children)



class Policy(Base):  # type: ignore
    """
    description: Represents an insurance policy associated with an application.
    """
    __tablename__ = 'policy'
    _s_collection_name = 'Policy'  # type: ignore

    id = Column(Integer, primary_key=True)
    policy_number = Column(String)
    effective_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    insurance_application_id = Column(ForeignKey('insurance_application.id'))

    # parent relationships (access parent)
    insurance_application : Mapped["InsuranceApplication"] = relationship(back_populates=("PolicyList"))

    # child relationships (access children)
    ClaimList : Mapped[List["Claim"]] = relationship(back_populates="policy")
    CoverageList : Mapped[List["Coverage"]] = relationship(back_populates="policy")
    PremiumList : Mapped[List["Premium"]] = relationship(back_populates="policy")



class Claim(Base):  # type: ignore
    """
    description: Represents a claim made against a policy.
    """
    __tablename__ = 'claim'
    _s_collection_name = 'Claim'  # type: ignore

    id = Column(Integer, primary_key=True)
    claim_date = Column(Date, nullable=False)
    description = Column(String)
    status = Column(String, nullable=False)
    policy_id = Column(ForeignKey('policy.id'))

    # parent relationships (access parent)
    policy : Mapped["Policy"] = relationship(back_populates=("ClaimList"))

    # child relationships (access children)



class Coverage(Base):  # type: ignore
    """
    description: Represents insurance coverage details included in a policy.
    """
    __tablename__ = 'coverage'
    _s_collection_name = 'Coverage'  # type: ignore

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    limit = Column(Integer, nullable=False)
    deductible = Column(Integer)
    policy_id = Column(ForeignKey('policy.id'))

    # parent relationships (access parent)
    policy : Mapped["Policy"] = relationship(back_populates=("CoverageList"))

    # child relationships (access children)



class Premium(Base):  # type: ignore
    """
    description: Represents the premium details associated with a policy.
    """
    __tablename__ = 'premium'
    _s_collection_name = 'Premium'  # type: ignore

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    policy_id = Column(ForeignKey('policy.id'))

    # parent relationships (access parent)
    policy : Mapped["Policy"] = relationship(back_populates=("PremiumList"))

    # child relationships (access children)
    BillingList : Mapped[List["Billing"]] = relationship(back_populates="premium")



class Billing(Base):  # type: ignore
    """
    description: Details regarding billing associated with a premium.
    """
    __tablename__ = 'billing'
    _s_collection_name = 'Billing'  # type: ignore

    id = Column(Integer, primary_key=True)
    billing_date = Column(Date, nullable=False)
    amount_due = Column(Integer, nullable=False)
    premium_id = Column(ForeignKey('premium.id'))

    # parent relationships (access parent)
    premium : Mapped["Premium"] = relationship(back_populates=("BillingList"))

    # child relationships (access children)

# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class InsuranceApplication(Base):
    """description: Represents the auto insurance application submitted by customers."""
    __tablename__ = 'insurance_application'
    id = Column(Integer, primary_key=True, autoincrement=True)
    application_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))

class Customer(Base):
    """description: Represents a customer who can apply for auto insurance."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthdate = Column(Date, nullable=True)
    email = Column(String, nullable=True)

class Vehicle(Base):
    """description: Represents a vehicle owned by a customer eligible for insurance."""
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))

class Policy(Base):
    """description: Represents an insurance policy associated with an application."""
    __tablename__ = 'policy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(String, nullable=True)
    effective_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    insurance_application_id = Column(Integer, ForeignKey(
        'insurance_application.id'))

class Premium(Base):
    """description: Represents the premium details associated with a policy."""
    __tablename__ = 'premium'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    due_date = Column(Date, nullable=False)
    policy_id = Column(Integer, ForeignKey('policy.id'))

class Claim(Base):
    """description: Represents a claim made against a policy."""
    __tablename__ = 'claim'
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_date = Column(Date, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)
    policy_id = Column(Integer, ForeignKey('policy.id'))

class Agent(Base):
    """description: Represents an insurance agent who manages applications and policies."""
    __tablename__ = 'agent'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

class AgentAssignment(Base):
    """description: Represents the assignment of agents to specific insurance applications."""
    __tablename__ = 'agent_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_date = Column(Date, nullable=False)
    agent_id = Column(Integer, ForeignKey('agent.id'))
    insurance_application_id = Column(Integer, ForeignKey(
        'insurance_application.id'))

class Coverage(Base):
    """description: Represents insurance coverage details included in a policy."""
    __tablename__ = 'coverage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    limit = Column(Integer, nullable=False)
    deductible = Column(Integer, nullable=True)
    policy_id = Column(Integer, ForeignKey('policy.id'))

class Incident(Base):
    """description: Represents an incident for which an insurance claim can be made."""
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_date = Column(Date, nullable=False)
    description = Column(String, nullable=True)

class IncidentReport(Base):
    """description: A report filed for an associated incident."""
    __tablename__ = 'incident_report'
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_date = Column(Date, nullable=False)
    incident_id = Column(Integer, ForeignKey('incident.id'))
    claimant_id = Column(Integer, ForeignKey('customer.id'))

class Billing(Base):
    """description: Details regarding billing associated with a premium."""
    __tablename__ = 'billing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    billing_date = Column(Date, nullable=False)
    amount_due = Column(Integer, nullable=False)
    premium_id = Column(Integer, ForeignKey('premium.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    InsuranceApplication(id=1, application_date=date(2023, 1, 15), status="Pending", customer_id=1)
    InsuranceApplication(id=2, application_date=date(2023, 2, 18), status="Approved", customer_id=2)
    InsuranceApplication(id=3, application_date=date(2023, 3, 20), status="Denied", customer_id=3)
    InsuranceApplication(id=4, application_date=date(2023, 4, 25), status="Pending", customer_id=4)
    Customer(id=1, first_name="John", last_name="Doe", birthdate=date(1985, 5, 20), email="johndoe@example.com")
    Customer(id=2, first_name="Jane", last_name="Smith", birthdate=date(1990, 12, 10), email="janesmith@example.com")
    Customer(id=3, first_name="Bill", last_name="Jones", birthdate=date(1975, 3, 5), email="billjones@example.com")
    Customer(id=4, first_name="Susan", last_name="Anderson", birthdate=date(1982, 7, 22), email="susananderson@example.com")
    Vehicle(id=1, make='Toyota', model='Camry', year=2018, customer_id=1)
    Vehicle(id=2, make='Ford', model='Fusion', year=2020, customer_id=2)
    Vehicle(id=3, make='Honda', model='Civic', year=2019, customer_id=3)
    Vehicle(id=4, make='Chevy', model='Malibu', year=2022, customer_id=1)
    Policy(id=1, policy_number="POL1234", effective_date=date(2023, 5, 1), expiration_date=date(2024, 5, 1), insurance_application_id=1)
    Policy(id=2, policy_number="POL5678", effective_date=date(2023, 6, 1), expiration_date=date(2024, 6, 1), insurance_application_id=2)
    Policy(id=3, policy_number="POL9101", effective_date=date(2023, 7, 1), expiration_date=date(2024, 7, 1), insurance_application_id=3)
    Policy(id=4, policy_number="POL1121", effective_date=date(2023, 8, 1), expiration_date=date(2024, 8, 1), insurance_application_id=4)
    Premium(id=1, amount=500, due_date=date(2023, 5, 31), policy_id=1)
    Premium(id=2, amount=550, due_date=date(2023, 6, 30), policy_id=2)
    Premium(id=3, amount=600, due_date=date(2023, 7, 31), policy_id=3)
    Premium(id=4, amount=580, due_date=date(2023, 8, 31), policy_id=4)
    Claim(id=1, claim_date=date(2023, 5, 15), description="Rear-end collision", status="Open", policy_id=1)
    Claim(id=2, claim_date=date(2023, 6, 10), description="Windshield damage", status="Closed", policy_id=2)
    Claim(id=3, claim_date=date(2023, 7, 5), description="Theft", status="Open", policy_id=3)
    Claim(id=4, claim_date=date(2023, 8, 1), description="Vandalism", status="Open", policy_id=1)
    Agent(id=1, first_name="Tom", last_name="Harris")
    Agent(id=2, first_name="Amy", last_name="Johnson")
    Agent(id=3, first_name="Steve", last_name="Baker")
    Agent(id=4, first_name="Laura", last_name="Hill")
    AgentAssignment(id=1, assignment_date=date(2023, 1, 16), agent_id=1, insurance_application_id=1)
    AgentAssignment(id=2, assignment_date=date(2023, 2, 19), agent_id=2, insurance_application_id=2)
    AgentAssignment(id=3, assignment_date=date(2023, 3, 21), agent_id=3, insurance_application_id=3)
    AgentAssignment(id=4, assignment_date=date(2023, 4, 26), agent_id=4, insurance_application_id=4)
    Coverage(id=1, type="Collision", limit=5000, deductible=500, policy_id=1)
    Coverage(id=2, type="Comprehensive", limit=6000, deductible=500, policy_id=2)
    Coverage(id=3, type="Liability", limit=10000, deductible=1000, policy_id=3)
    Coverage(id=4, type="Uninsured Motorist", limit=7500, deductible=750, policy_id=4)
    Incident(id=1, incident_date=date(2023, 5, 9), description="Minor accident")
    Incident(id=2, incident_date=date(2023, 6, 11), description="Major accident")
    Incident(id=3, incident_date=date(2023, 7, 14), description="Natural disaster")
    Incident(id=4, incident_date=date(2023, 8, 18), description="Fender bender")
    IncidentReport(id=1, report_date=date(2023, 5, 10), incident_id=1, claimant_id=1)
    IncidentReport(id=2, report_date=date(2023, 6, 12), incident_id=2, claimant_id=2)
    IncidentReport(id=3, report_date=date(2023, 7, 15), incident_id=3, claimant_id=3)
    IncidentReport(id=4, report_date=date(2023, 8, 19), incident_id=4, claimant_id=4)
    Billing(id=1, billing_date=date(2023, 5, 1), amount_due=495, premium_id=1)
    Billing(id=2, billing_date=date(2023, 6, 1), amount_due=540, premium_id=2)
    Billing(id=3, billing_date=date(2023, 7, 1), amount_due=590, premium_id=3)
    Billing(id=4, billing_date=date(2023, 8, 1), amount_due=570, premium_id=4)
    
    
    
    session.add_all([insurance_application_1, insurance_application_2, insurance_application_3, insurance_application_4, customer_1, customer_2, customer_3, customer_4, vehicle_1, vehicle_2, vehicle_3, vehicle_4, policy_1, policy_2, policy_3, policy_4, premium_1, premium_2, premium_3, premium_4, claim_1, claim_2, claim_3, claim_4, agent_1, agent_2, agent_3, agent_4, agent_assignment_1, agent_assignment_2, agent_assignment_3, agent_assignment_4, coverage_1, coverage_2, coverage_3, coverage_4, incident_1, incident_2, incident_3, incident_4, incident_report_1, incident_report_2, incident_report_3, incident_report_4, billing_1, billing_2, billing_3, billing_4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')

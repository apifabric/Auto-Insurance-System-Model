import logging
import logging.config
import json
import os
import sys

os.environ["APILOGICPROJECT_NO_FLASK"] = "1"  # must be present before importing models

import traceback
import yaml
from datetime import date, datetime
from pathlib import Path
from decimal import Decimal
from sqlalchemy import (Boolean, Column, Date, DateTime, DECIMAL, Float, ForeignKey, Integer, Numeric, String, Text, create_engine)
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

current_path = Path(__file__)
project_path = (current_path.parent.parent.parent).resolve()
sys.path.append(str(project_path))

from logic_bank.logic_bank import LogicBank, Rule
from logic import declare_logic
from database.models import *
from database.models import Base

project_dir = Path(os.getenv("PROJECT_DIR",'./')).resolve()

assert str(os.getcwd()) == str(project_dir), f"Current directory must be {project_dir}"

data_log : list[str] = []

logging_config = project_dir / 'config/logging.yml'
if logging_config.is_file():
    with open(logging_config,'rt') as f:  
        config=yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logic_logger = logging.getLogger('logic_logger')
logic_logger.setLevel(logging.DEBUG)
logic_logger.info(f'..  logic_logger: {logic_logger}')

db_url_path = project_dir.joinpath('database/test_data/db.sqlite')
db_url = f'sqlite:///{db_url_path.resolve()}'
logging.info(f'..  db_url: {db_url}')
logging.info(f'..  cwd: {os.getcwd()}')
logging.info(f'..  python_loc: {sys.executable}')
logging.info(f'..  test_data_loader version: 1.1')
data_log.append(f'..  db_url: {db_url}')
data_log.append(f'..  cwd: {os.getcwd()}')
data_log.append(f'..  python_loc: {sys.executable}')
data_log.append(f'..  test_data_loader version: 1.1')

if db_url_path.is_file():
    db_url_path.unlink()

try:
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)  # note: LogicBank activated for this session only
    session = Session()
    LogicBank.activate(session=session, activator=declare_logic.declare_logic)
except Exception as e: 
    logging.error(f'Error creating engine: {e}')
    data_log.append(f'Error creating engine: {e}')
    print('\n'.join(data_log))
    with open(project_dir / 'database/test_data/test_data_code_log.txt', 'w') as log_file:
        log_file.write('\n'.join(data_log))
    print('\n'.join(data_log))
    raise

logging.info(f'..  LogicBank activated')
data_log.append(f'..  LogicBank activated')

restart_count = 0
has_errors = True
succeeded_hashes = set()

while restart_count < 5 and has_errors:
    has_errors = False
    restart_count += 1
    data_log.append("print(Pass: " + str(restart_count) + ")" )
    try:
        if not -2480615153594714478 in succeeded_hashes:  # avoid duplicate inserts
            instance = InsuranceApplication(id=1, application_date=date(2023, 1, 15), status="Pending", customer_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-2480615153594714478)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 4764574343532907501 in succeeded_hashes:  # avoid duplicate inserts
            instance = InsuranceApplication(id=2, application_date=date(2023, 2, 18), status="Approved", customer_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(4764574343532907501)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 869598135462928255 in succeeded_hashes:  # avoid duplicate inserts
            instance = InsuranceApplication(id=3, application_date=date(2023, 3, 20), status="Denied", customer_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(869598135462928255)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -6183133471313208994 in succeeded_hashes:  # avoid duplicate inserts
            instance = InsuranceApplication(id=4, application_date=date(2023, 4, 25), status="Pending", customer_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-6183133471313208994)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -1371757230561176405 in succeeded_hashes:  # avoid duplicate inserts
            instance = Customer(id=1, first_name="John", last_name="Doe", birthdate=date(1985, 5, 20), email="johndoe@example.com")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-1371757230561176405)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -3119165886336770632 in succeeded_hashes:  # avoid duplicate inserts
            instance = Customer(id=2, first_name="Jane", last_name="Smith", birthdate=date(1990, 12, 10), email="janesmith@example.com")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-3119165886336770632)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -8630804320968175550 in succeeded_hashes:  # avoid duplicate inserts
            instance = Customer(id=3, first_name="Bill", last_name="Jones", birthdate=date(1975, 3, 5), email="billjones@example.com")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-8630804320968175550)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -3297816641507542322 in succeeded_hashes:  # avoid duplicate inserts
            instance = Customer(id=4, first_name="Susan", last_name="Anderson", birthdate=date(1982, 7, 22), email="susananderson@example.com")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-3297816641507542322)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -8655464993321104878 in succeeded_hashes:  # avoid duplicate inserts
            instance = Vehicle(id=1, make='Toyota', model='Camry', year=2018, customer_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-8655464993321104878)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -7784969860009592256 in succeeded_hashes:  # avoid duplicate inserts
            instance = Vehicle(id=2, make='Ford', model='Fusion', year=2020, customer_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-7784969860009592256)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -4764358661554871604 in succeeded_hashes:  # avoid duplicate inserts
            instance = Vehicle(id=3, make='Honda', model='Civic', year=2019, customer_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-4764358661554871604)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 5696377750194700790 in succeeded_hashes:  # avoid duplicate inserts
            instance = Vehicle(id=4, make='Chevy', model='Malibu', year=2022, customer_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(5696377750194700790)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -6638344619241543285 in succeeded_hashes:  # avoid duplicate inserts
            instance = Policy(id=1, policy_number="POL1234", effective_date=date(2023, 5, 1), expiration_date=date(2024, 5, 1), insurance_application_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-6638344619241543285)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 3150195156520031810 in succeeded_hashes:  # avoid duplicate inserts
            instance = Policy(id=2, policy_number="POL5678", effective_date=date(2023, 6, 1), expiration_date=date(2024, 6, 1), insurance_application_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(3150195156520031810)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 8627682260447814539 in succeeded_hashes:  # avoid duplicate inserts
            instance = Policy(id=3, policy_number="POL9101", effective_date=date(2023, 7, 1), expiration_date=date(2024, 7, 1), insurance_application_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(8627682260447814539)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 6367951613279637931 in succeeded_hashes:  # avoid duplicate inserts
            instance = Policy(id=4, policy_number="POL1121", effective_date=date(2023, 8, 1), expiration_date=date(2024, 8, 1), insurance_application_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(6367951613279637931)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 5142175468067521971 in succeeded_hashes:  # avoid duplicate inserts
            instance = Premium(id=1, amount=500, due_date=date(2023, 5, 31), policy_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(5142175468067521971)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -4912718672074372124 in succeeded_hashes:  # avoid duplicate inserts
            instance = Premium(id=2, amount=550, due_date=date(2023, 6, 30), policy_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-4912718672074372124)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 4710551846606535371 in succeeded_hashes:  # avoid duplicate inserts
            instance = Premium(id=3, amount=600, due_date=date(2023, 7, 31), policy_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(4710551846606535371)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 6761174569532923253 in succeeded_hashes:  # avoid duplicate inserts
            instance = Premium(id=4, amount=580, due_date=date(2023, 8, 31), policy_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(6761174569532923253)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -2703545397788908659 in succeeded_hashes:  # avoid duplicate inserts
            instance = Claim(id=1, claim_date=date(2023, 5, 15), description="Rear-end collision", status="Open", policy_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-2703545397788908659)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 2865994682467109194 in succeeded_hashes:  # avoid duplicate inserts
            instance = Claim(id=2, claim_date=date(2023, 6, 10), description="Windshield damage", status="Closed", policy_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(2865994682467109194)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 3216379626231412990 in succeeded_hashes:  # avoid duplicate inserts
            instance = Claim(id=3, claim_date=date(2023, 7, 5), description="Theft", status="Open", policy_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(3216379626231412990)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 5875610227343374008 in succeeded_hashes:  # avoid duplicate inserts
            instance = Claim(id=4, claim_date=date(2023, 8, 1), description="Vandalism", status="Open", policy_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(5875610227343374008)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 5816583017742797184 in succeeded_hashes:  # avoid duplicate inserts
            instance = Agent(id=1, first_name="Tom", last_name="Harris")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(5816583017742797184)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 4988631901545034382 in succeeded_hashes:  # avoid duplicate inserts
            instance = Agent(id=2, first_name="Amy", last_name="Johnson")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(4988631901545034382)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 7539998784669101516 in succeeded_hashes:  # avoid duplicate inserts
            instance = Agent(id=3, first_name="Steve", last_name="Baker")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(7539998784669101516)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 3710888006293056669 in succeeded_hashes:  # avoid duplicate inserts
            instance = Agent(id=4, first_name="Laura", last_name="Hill")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(3710888006293056669)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 388806788178172957 in succeeded_hashes:  # avoid duplicate inserts
            instance = AgentAssignment(id=1, assignment_date=date(2023, 1, 16), agent_id=1, insurance_application_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(388806788178172957)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 3161625115468029714 in succeeded_hashes:  # avoid duplicate inserts
            instance = AgentAssignment(id=2, assignment_date=date(2023, 2, 19), agent_id=2, insurance_application_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(3161625115468029714)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 4298381288370446819 in succeeded_hashes:  # avoid duplicate inserts
            instance = AgentAssignment(id=3, assignment_date=date(2023, 3, 21), agent_id=3, insurance_application_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(4298381288370446819)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -3312938404766558577 in succeeded_hashes:  # avoid duplicate inserts
            instance = AgentAssignment(id=4, assignment_date=date(2023, 4, 26), agent_id=4, insurance_application_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-3312938404766558577)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 7266398882026785425 in succeeded_hashes:  # avoid duplicate inserts
            instance = Coverage(id=1, type="Collision", limit=5000, deductible=500, policy_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(7266398882026785425)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 4190637005411317210 in succeeded_hashes:  # avoid duplicate inserts
            instance = Coverage(id=2, type="Comprehensive", limit=6000, deductible=500, policy_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(4190637005411317210)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 110614474563112720 in succeeded_hashes:  # avoid duplicate inserts
            instance = Coverage(id=3, type="Liability", limit=10000, deductible=1000, policy_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(110614474563112720)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 8187656944274901523 in succeeded_hashes:  # avoid duplicate inserts
            instance = Coverage(id=4, type="Uninsured Motorist", limit=7500, deductible=750, policy_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(8187656944274901523)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -1191244255667484642 in succeeded_hashes:  # avoid duplicate inserts
            instance = Incident(id=1, incident_date=date(2023, 5, 9), description="Minor accident")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-1191244255667484642)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -4435986884309884404 in succeeded_hashes:  # avoid duplicate inserts
            instance = Incident(id=2, incident_date=date(2023, 6, 11), description="Major accident")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-4435986884309884404)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -9222550043945875767 in succeeded_hashes:  # avoid duplicate inserts
            instance = Incident(id=3, incident_date=date(2023, 7, 14), description="Natural disaster")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-9222550043945875767)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -3995001403142016531 in succeeded_hashes:  # avoid duplicate inserts
            instance = Incident(id=4, incident_date=date(2023, 8, 18), description="Fender bender")
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-3995001403142016531)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -1189634737511803300 in succeeded_hashes:  # avoid duplicate inserts
            instance = IncidentReport(id=1, report_date=date(2023, 5, 10), incident_id=1, claimant_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-1189634737511803300)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -166892696430588439 in succeeded_hashes:  # avoid duplicate inserts
            instance = IncidentReport(id=2, report_date=date(2023, 6, 12), incident_id=2, claimant_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-166892696430588439)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 1668845259615710925 in succeeded_hashes:  # avoid duplicate inserts
            instance = IncidentReport(id=3, report_date=date(2023, 7, 15), incident_id=3, claimant_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(1668845259615710925)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 4263378460870344271 in succeeded_hashes:  # avoid duplicate inserts
            instance = IncidentReport(id=4, report_date=date(2023, 8, 19), incident_id=4, claimant_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(4263378460870344271)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 7142817005176633527 in succeeded_hashes:  # avoid duplicate inserts
            instance = Billing(id=1, billing_date=date(2023, 5, 1), amount_due=495, premium_id=1)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(7142817005176633527)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not -344001992808601796 in succeeded_hashes:  # avoid duplicate inserts
            instance = Billing(id=2, billing_date=date(2023, 6, 1), amount_due=540, premium_id=2)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(-344001992808601796)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 6916425052952097401 in succeeded_hashes:  # avoid duplicate inserts
            instance = Billing(id=3, billing_date=date(2023, 7, 1), amount_due=590, premium_id=3)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(6916425052952097401)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()

    try:
        if not 5000091123604951608 in succeeded_hashes:  # avoid duplicate inserts
            instance = Billing(id=4, billing_date=date(2023, 8, 1), amount_due=570, premium_id=4)
            session.add(instance)
            session.commit()
            succeeded_hashes.add(5000091123604951608)
    except Exception as e:
        has_errors = True
        if 'UNIQUE' in str(e) and restart_count > 1:
            pass
        else:
            error_str = f"Error adding variable to session: {e}"
            if not error_str in data_log:
                data_log.append(error_str)
        if not restart_count in [2,3]:
            session.rollback()
print('\n'.join(data_log))
with open(project_dir / 'database/test_data/test_data_code_log.txt', 'w') as log_file:
    log_file.write('\n'.join(data_log))
print('\n'.join(data_log))

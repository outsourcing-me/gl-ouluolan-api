from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship

from . import database


class Department(database.Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))


class Role(database.Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(32))


class Employee(database.Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto
    # its Employees
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))
    role = relationship(
        Role,
        backref=backref('roles',
                        uselist=True,
                        cascade='delete,all'))

from sqlalchemy import Boolean, Column, String, Integer, Float, ForeignKey, Date, TIMESTAMP, Text, Numeric
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from ..config.database import Base

class Company(Base):
    __tablename__ = "company"
    
    nit = Column(String(20), primary_key=True)
    name = Column(String(100), nullable=False)
    industry = Column(String(50))
    address = Column(String(255))
    phone = Column(String(20))
    email = Column(String(100))
    country = Column(String(50))
    state = Column(String(50))
    creation_date = Column(Date, server_default=text('CURRENT_DATE'))

    # Relaciones
    contacts = relationship("Contact", back_populates="company", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="company", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="company", cascade="all, delete-orphan")
    user_accounts = relationship("UserAccount", back_populates="company", cascade="all, delete-orphan")

class Contact(Base):
    __tablename__ = "contact"
    
    contact_id = Column(String(20), primary_key=True)
    nit = Column(String(20), ForeignKey('company.nit', ondelete='CASCADE'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    last_interaction_date = Column(Date)

    # Relaciones
    company = relationship("Company", back_populates="contacts")
    departments = relationship("Department", secondary="contact_department", back_populates="contacts")
    interactions = relationship("Interaction", back_populates="contact", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="contact")

class Department(Base):
    __tablename__ = "department"
    
    department_id = Column(String(20), primary_key=True)
    department_name = Column(String(50), nullable=False)
    description = Column(Text)

    # Relaciones
    contacts = relationship("Contact", secondary="contact_department", back_populates="departments")

class ContactDepartment(Base):
    __tablename__ = "contact_department"
    
    contact_id = Column(String(20), ForeignKey('contact.contact_id', ondelete='CASCADE'), primary_key=True)
    department_id = Column(String(20), ForeignKey('department.department_id', ondelete='CASCADE'), primary_key=True)
    assignment_date = Column(Date, server_default=text('CURRENT_DATE'))

class Interaction(Base):
    __tablename__ = "interaction"
    
    interaction_id = Column(String(20), primary_key=True)
    contact_id = Column(String(20), ForeignKey('contact.contact_id', ondelete='CASCADE'))
    interaction_date = Column(Date, server_default=text('CURRENT_DATE'))
    interaction_type = Column(String(50))
    notes = Column(Text)

    # Relaciones
    contact = relationship("Contact", back_populates="interactions")

class Opportunity(Base):
    __tablename__ = "opportunity"
    
    opportunity_id = Column(String(20), primary_key=True)
    nit = Column(String(20), ForeignKey('company.nit', ondelete='CASCADE'))
    contact_id = Column(String(20), ForeignKey('contact.contact_id'))
    opportunity_name = Column(String(100), nullable=False)
    description = Column(Text)
    estimated_value = Column(Numeric(15, 2))
    creation_date = Column(Date, server_default=text('CURRENT_DATE'))
    estimated_close_date = Column(Date)
    status = Column(String(20), server_default=text("'open'"))
    success_probability = Column(Numeric(5, 2))

    # Relaciones
    company = relationship("Company", back_populates="opportunities")
    contact = relationship("Contact", back_populates="opportunities")
    stages = relationship("OpportunityStage", secondary="opportunity_stage_history", back_populates="opportunities")
    products = relationship("ProductService", secondary="opportunity_product_service", back_populates="opportunities")

class OpportunityStage(Base):
    __tablename__ = "opportunity_stage"
    
    stage_id = Column(String(20), primary_key=True)
    stage_name = Column(String(50), nullable=False)
    description = Column(Text)

    # Relaciones
    opportunities = relationship("Opportunity", secondary="opportunity_stage_history", back_populates="stages")

class OpportunityStageHistory(Base):
    __tablename__ = "opportunity_stage_history"
    
    opportunity_id = Column(String(20), ForeignKey('opportunity.opportunity_id', ondelete='CASCADE'), primary_key=True)
    stage_id = Column(String(20), ForeignKey('opportunity_stage.stage_id', ondelete='CASCADE'), primary_key=True)
    change_date = Column(Date, server_default=text('CURRENT_DATE'))
    notes = Column(Text)

class ProductService(Base):
    __tablename__ = "product_service"
    
    product_service_id = Column(String(20), primary_key=True)
    product_service_name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(15, 2))

    # Relaciones
    opportunities = relationship("Opportunity", secondary="opportunity_product_service", back_populates="products")

class OpportunityProductService(Base):
    __tablename__ = "opportunity_product_service"
    
    opportunity_id = Column(String(20), ForeignKey('opportunity.opportunity_id', ondelete='CASCADE'), primary_key=True)
    product_service_id = Column(String(20), ForeignKey('product_service.product_service_id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, server_default=text('1'))
    negotiated_price = Column(Numeric(15, 2))

class Role(Base):
    __tablename__ = "role"
    
    role_id = Column(String(20), primary_key=True)
    role_name = Column(String(50), nullable=False)
    description = Column(Text)

    # Relaciones
    users = relationship("UserAccount", secondary="user_role", back_populates="roles")

class UserAccount(Base):
    __tablename__ = "user_account"
    
    user_id = Column(String(20), primary_key=True)
    nit = Column(String(20), ForeignKey('company.nit', ondelete='CASCADE'))
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    last_login = Column(TIMESTAMP)

    # Relaciones
    company = relationship("Company", back_populates="user_accounts")
    roles = relationship("Role", secondary="user_role", back_populates="users")

class UserRole(Base):
    __tablename__ = "user_role"
    
    user_id = Column(String(20), ForeignKey('user_account.user_id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(String(20), ForeignKey('role.role_id', ondelete='CASCADE'), primary_key=True)

class Contract(Base):
    __tablename__ = "contract"
    
    contract_id = Column(String(20), primary_key=True)
    nit = Column(String(20), ForeignKey('company.nit'))
    contract_number = Column(String(50), unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_value = Column(Numeric(15, 2), nullable=False)

    # Relaciones
    company = relationship("Company", back_populates="contracts")
    delivery_certificates = relationship("DeliveryCertificate", back_populates="contract")

class DeliveryCertificate(Base):
    __tablename__ = "delivery_certificate"
    
    certificate_id = Column(String(20), primary_key=True)
    contract_id = Column(String(20), ForeignKey('contract.contract_id'))
    delivery_date = Column(Date, nullable=False)
    notes = Column(Text)
    nit = Column(String(20), ForeignKey('company.nit'))

    # Relaciones
    contract = relationship("Contract", back_populates="delivery_certificates")
    equipment = relationship("Equipment", back_populates="certificate")

class Category(Base):
    __tablename__ = "category"
    
    category_id = Column(String(20), primary_key=True)
    category_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    # Relaciones
    equipment = relationship("Equipment", back_populates="category")

class Equipment(Base):
    __tablename__ = "equipment"
    
    equipment_id = Column(String(20), primary_key=True)
    certificate_id = Column(String(20), ForeignKey('delivery_certificate.certificate_id', ondelete='CASCADE'))
    inventory_code = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    active = Column(Boolean, server_default=text('true'))
    category_id = Column(String(20), ForeignKey('category.category_id', ondelete='SET NULL'))

    # Relaciones
    certificate = relationship("DeliveryCertificate", back_populates="equipment")
    category = relationship("Category", back_populates="equipment")
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# Company Schemas
class CompanyBase(BaseModel):
    name: str
    industry: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    country: Optional[str]
    state: Optional[str]

class CompanyCreate(CompanyBase):
    nit: str

class Company(CompanyBase):
    nit: str
    creation_date: Optional[date]

    class Config:
        from_attributes = True

# Contact Schemas
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    position: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]

class ContactCreate(ContactBase):
    nit: str

class Contact(ContactBase):
    contact_id: str
    nit: str
    last_interaction_date: Optional[date]

    class Config:
        from_attributes = True

# Department Schemas
class DepartmentBase(BaseModel):
    department_name: str
    description: Optional[str]

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    department_id: str

    class Config:
        from_attributes = True

# Contact Department Schemas
class ContactDepartmentBase(BaseModel):
    contact_id: str
    department_id: str
    assignment_date: Optional[date]

class ContactDepartmentCreate(ContactDepartmentBase):
    pass

class ContactDepartment(ContactDepartmentBase):
    class Config:
        from_attributes = True

# Interaction Schemas
class InteractionBase(BaseModel):
    interaction_type: str
    notes: Optional[str]

class InteractionCreate(InteractionBase):
    contact_id: str

class Interaction(InteractionBase):
    interaction_id: str
    contact_id: str
    interaction_date: date

    class Config:
        from_attributes = True

# Opportunity Schemas
class OpportunityBase(BaseModel):
    opportunity_name: str
    description: Optional[str]
    estimated_value: Optional[Decimal]
    estimated_close_date: Optional[date]
    status: Optional[str] = "open"
    success_probability: Optional[Decimal]

class OpportunityCreate(OpportunityBase):
    nit: str
    contact_id: Optional[str]

class Opportunity(OpportunityBase):
    opportunity_id: str
    nit: str
    contact_id: Optional[str]
    creation_date: date

    class Config:
        from_attributes = True

# Opportunity Stage Schemas
class OpportunityStageBase(BaseModel):
    stage_name: str
    description: Optional[str]

class OpportunityStageCreate(OpportunityStageBase):
    pass

class OpportunityStage(OpportunityStageBase):
    stage_id: str

    class Config:
        from_attributes = True

# Opportunity Stage History Schemas
class OpportunityStageHistoryBase(BaseModel):
    opportunity_id: str
    stage_id: str
    notes: Optional[str]

class OpportunityStageHistoryCreate(OpportunityStageHistoryBase):
    pass

class OpportunityStageHistory(OpportunityStageHistoryBase):
    change_date: date

    class Config:
        from_attributes = True

# Product Service Schemas
class ProductServiceBase(BaseModel):
    product_service_name: str
    description: Optional[str]
    price: Decimal

class ProductServiceCreate(ProductServiceBase):
    pass

class ProductService(ProductServiceBase):
    product_service_id: str

    class Config:
        from_attributes = True

# Opportunity Product Service Schemas
class OpportunityProductServiceBase(BaseModel):
    opportunity_id: str
    product_service_id: str
    quantity: int
    negotiated_price: Optional[Decimal]

class OpportunityProductServiceCreate(OpportunityProductServiceBase):
    pass

class OpportunityProductService(OpportunityProductServiceBase):
    class Config:
        from_attributes = True

# Role Schemas
class RoleBase(BaseModel):
    role_name: str
    description: Optional[str]

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    role_id: str

    class Config:
        from_attributes = True

# User Account Schemas
class UserAccountBase(BaseModel):
    username: str
    email: EmailStr

class UserAccountCreate(UserAccountBase):
    password: str
    nit: str

class UserAccount(UserAccountBase):
    user_id: str
    nit: str
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

# User Role Schemas
class UserRoleBase(BaseModel):
    user_id: str
    role_id: str

class UserRoleCreate(UserRoleBase):
    pass

class UserRole(UserRoleBase):
    class Config:
        from_attributes = True

# Contract Schemas
class ContractBase(BaseModel):
    contract_number: str
    start_date: date
    end_date: date
    monthly_value: Decimal

class ContractCreate(ContractBase):
    nit: str

class Contract(ContractBase):
    contract_id: str
    nit: str

    class Config:
        from_attributes = True

# Delivery Certificate Schemas
class DeliveryCertificateBase(BaseModel):
    delivery_date: date
    notes: Optional[str]

class DeliveryCertificateCreate(DeliveryCertificateBase):
    delivery_date: date
    notes: Optional[str]
    nit: str

class DeliveryCertificate(DeliveryCertificateBase):
    certificate_id: str
    contract_id: str
    nit: str

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    category_name: str
    description: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: str

    class Config:
        from_attributes = True

# Equipment Schemas
class EquipmentBase(BaseModel):
    inventory_code: str
    description: str
    active: bool = True

class EquipmentCreate(EquipmentBase):
    certificate_id: str
    category_id: str

class Equipment(EquipmentBase):
    equipment_id: str
    certificate_id: str
    category_id: str

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
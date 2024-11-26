from ..config.database import Base

from .postgres_models import (
    Company,
    Contact,
    Department,
    ContactDepartment,
    Interaction,
    Opportunity,
    OpportunityStage,
    OpportunityStageHistory,
    ProductService,
    OpportunityProductService,
    Role,
    UserAccount,
    UserRole,
    Contract,
    DeliveryCertificate,
    Category,
    Equipment
)

__all__ = [
    'Base',
    'Company',
    'Contact',
    'Department',
    'ContactDepartment',
    'Interaction',
    'Opportunity',
    'OpportunityStage',
    'OpportunityStageHistory',
    'ProductService',
    'OpportunityProductService',
    'Role',
    'UserAccount',
    'UserRole',
    'Contract',
    'DeliveryCertificate',
    'Category',
    'Equipment'
]
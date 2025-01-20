from enum import Enum


class UserRoles(str, Enum):
    super_admin = 'Super Admin'
    insurance_company_admin = 'Insurance Company Admin'
    insurance_agent = 'Insurance Agent'
    prospect = 'Prospect'
    policyholder = 'Policyholder'

from base_element.Role import CRole

class CRoleUtil:
    @staticmethod
    def get_next_role(current_role):
        NEXT_ROLE_MAP = {
            CRole.LANDLORD: CRole.LANDLORD_DOWN,
            CRole.LANDLORD_DOWN: CRole.LANDLORD_UP,
            CRole.LANDLORD_UP: CRole.LANDLORD
        }
        return NEXT_ROLE_MAP.get(current_role, CRole.LANDLORD)


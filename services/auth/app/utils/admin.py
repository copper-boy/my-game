from app.orm.user import AdminModel, UserModel


async def create_admin(user: UserModel) -> tuple[AdminModel, bool]:
    admin = await AdminModel.get_or_create(user=user)
    return admin

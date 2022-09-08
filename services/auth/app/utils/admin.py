from orm.user import AdminModel, UserModel


async def create_admin(user: UserModel) -> AdminModel:
    admin = await AdminModel.get_or_create(user=user)
    return admin


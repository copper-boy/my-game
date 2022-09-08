from orm.user import UserModel, AdminModel


async def create_admin(user: UserModel) -> AdminModel:
    return await AdminModel.get_or_create(user=user)

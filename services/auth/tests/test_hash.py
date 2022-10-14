from app.utils.auth import get_password_hash, verify_password


class TestHash:
    async def test_hash_create(self):
        password = 'some_strong_password'
        hashed_password = await get_password_hash(password)

        assert password != hashed_password

    async def test_successfully_verify_hash(self):
        password = 'some_strong_password'
        posted_password = 'some_strong_password'

        hashed_password = await get_password_hash(password)

        is_verified = await verify_password(posted_password, hashed_password)
        assert is_verified

    async def test_bad_verify_hash(self):
        password = 'some_strong_password'
        posted_password = 'invalid_password'

        hashed_password = await get_password_hash(password)

        is_verified = await verify_password(posted_password, hashed_password)
        assert not is_verified

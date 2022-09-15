class TestRegistration:
    async def test_bad_registration(self, cli):
        resp = await cli.post(url='/api/v1/auth/registration',
                              json={
                                  'email': 'not-a-valid-email',
                                  'password': 'strong_password'
                              })

        assert resp.status_code == 422

    async def test_successfully_registration(self, cli):
        resp = await cli.post(url='/api/v1/auth/registration',
                              json={
                                  'email': 'good@email.com',
                                  'password': 'very_strong_password'
                              })
        resp_json = resp.json()['detail']['user']
        assert resp.status_code == 200
        assert resp_json['email'] == 'good@email.com'

    async def test_register_an_existing_user(self, cli):
        resp = await cli.post(url='/api/v1/auth/registration',
                              json={
                                  'email': 'good@email.com',
                                  'password': 'very_strong_password'
                              })
        resp_json = resp.json()

        assert resp.status_code == 409
        assert resp_json['detail'] == 'current user exists'


class TestLogin:
    async def test_bad_login(self, cli):
        resp = await cli.post(url='/api/v1/auth/login',
                              json={
                                  'email': 'non-existing-user@not.found',
                                  'password': 'strong_password'
                              })
        assert resp.status_code == 404


class TestCurrent:
    async def test_unauthorized_current(self, cli):
        resp = await cli.get(url='/api/v1/auth/current')
        resp_json = resp.json()['detail']

        assert resp.status_code == 401
        assert resp_json.lower() == 'missing authorization header'

    async def test_invalid_header(self, cli):
        resp = await cli.get(url='/api/v1/auth/current',
                             headers={
                                 'Authorization': 'Bearer invalid_access_token'
                             })
        assert resp.status_code == 422

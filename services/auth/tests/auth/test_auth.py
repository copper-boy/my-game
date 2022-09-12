class TestRegistration:
    async def test_bad_registration(self, cli):
        resp = await cli.post(url='/api/v1/auth/registration',
                              json={
                                  'email': 'not-a-valid-email',
                                  'password': 'strong_password'
                              })

        assert resp.status_code == 422

    async def test_successfully_registration(self, cli, config):
        resp = await cli.post(url='/api/v1/auth/registration',
                              json={
                                  'email': config.ADMIN_LOGIN,
                                  'password': config.ADMIN_PASSWORD
                              })
        resp_json = resp.json()

        assert resp.status_code == 200
        assert resp_json['detail']['user']['email'] == config.ADMIN_LOGIN

    async def test_register_an_existing_user(self, cli, config):
        resp = await cli.post(url='/api/v1/auth/registration',
                              json={
                                  'email': config.ADMIN_LOGIN,
                                  'password': config.ADMIN_PASSWORD
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

    async def test_bad_login_password(self, cli, config):
        resp = await cli.post(url='/api/v1/auth/login',
                              json={
                                  'email': config.ADMIN_LOGIN,
                                  'password': 'strong_password'
                              })
        resp_json = resp.json()

        assert resp.status_code == 403
        assert resp_json['detail'] == 'incorrect login data posted'

    async def test_successfully_login(self, cli, config):
        resp = await cli.post(url='/api/v1/auth/login',
                              json={
                                  'email': config.ADMIN_LOGIN,
                                  'password': config.ADMIN_PASSWORD
                              })
        resp_json = resp.json()

        assert resp.status_code == 200
        assert resp_json['detail'].get('access_token', None) is not None


class TestCurrent:
    async def test_unauthorized_current(self, cli):
        resp = await cli.get(url='/api/v1/auth/current')
        resp_json = resp.json()

        assert resp.status_code == 401
        assert resp_json['detail'].lower() == 'missing authorization header'

    async def test_authorized_current(self, config, authed_cli):
        resp = await authed_cli.get(url='/api/v1/auth/current')
        resp_json = resp.json()

        assert resp.status_code == 200
        assert resp_json['detail']['user']['email'] == config.ADMIN_LOGIN

    async def test_invalid_header(self, cli):
        resp = await cli.get(url='/api/v1/auth/current',
                             headers={
                                 'Authorization': 'Bearer invalid_access_token'
                             })
        assert resp.status_code == 422

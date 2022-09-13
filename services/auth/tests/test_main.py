class TestMain:
    async def test_root(self, cli):
        resp = await cli.get(url='/')
        resp_json = resp.json()

        assert resp.status_code == 200
        assert resp_json == {'ping': 'pong'}

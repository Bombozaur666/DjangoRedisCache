import pytest
from django import urls


@pytest.mark.parametrize('param', [
    ('ping')
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 400 and resp.content == b'{"error": "Please give url"}'


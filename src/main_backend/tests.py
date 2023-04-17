import pytest
from django.urls import reverse


@pytest.mark.parametrize('param', [('ping')])
def test_no_content(client, param):
    temp_url = reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 400 and resp.content == b'{"error": "Please give url"}'

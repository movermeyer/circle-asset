from nose.tools import eq_
from unittest.mock import patch

from circle_asset.circle_api import get_latest_build, get_artifact_list
from circle_asset.project import Project

PROJECT = Project(username='pony',
                  project='bees',
                  api_root='http://example.com',
                  token=None)

class FakeResponse(object):
    def __init__(self, json_content):
        self._json = json_content

    def json(self):
        return self._json

@patch('requests.get')
def test_get_latest_build_pattern(rq_get):
    rq_get.configure_mock(return_value=FakeResponse([{'build_num': 10}]))
    build = get_latest_build(PROJECT, 'master')
    rq_get.assert_called_with('http://example.com/project/pony/bees/tree/master?limit=1&filter=successful', headers={'Accept': 'application/json'})
    eq_(build, 10)

@patch('requests.get')
def test_get_artifacts_pattern(rq_get):
    rq_get.configure_mock(return_value=FakeResponse([{'pretty_path': '$CIRCLE_ARTIFACTS/bees', 'url': 'http://example.com/bees'}]))
    artifacts = get_artifact_list(PROJECT, 12)
    rq_get.assert_called_with('http://example.com/project/pony/bees/12/artifacts', headers={'Accept': 'application/json'})
    eq_(artifacts, {'bees': 'http://example.com/bees'})


#!/bin/env python
from flask import url_for

from app.components import logger  # type: ignore
from tests.conftest import http_req, project_id

log = logger.get_logger(__name__)


class TestEdcVisit(object):
    """edc_visit相关单元测试"""
    def test_edc_visit_add(self, client):
        payload = {"project_id": project_id, "visit_name": "v1", "visit_number": "V01"}
        resp_json = http_req(client, url_for('edc.visit-add'), method='POST', payload=payload)
        resp_json2 = http_req(client, url_for('edc.visit-add'), method='POST', payload={'project_id': project_id, 'visit_name': 'v2', 'visit_number': 'V02'})
        log.info(str(resp_json) + str(resp_json2))
        assert resp_json['code'] == 0 and resp_json2['code'] == 0

    def test_edc_visit_list(self, client):
        resp_json = http_req(client, url_for('edc.visit-list'), method='GET', payload={'project_id': project_id})
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_visit_update(self, client):
        payload = {'visit_id': 2, 'visit_name': 'v22', 'visit_number': 'V0202'}
        resp_json = http_req(client, url_for('edc.visit-update'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_visit_sort(self, client):
        payload = {'project_id': project_id, 'visit_ids': [1, 2, 3]}
        resp_json = http_req(client, url_for('edc.visit-sort'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_visit_delete(self, client):
        payload = {'visit_id': 2}
        resp_json = http_req(client, url_for('edc.visit-delete'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0





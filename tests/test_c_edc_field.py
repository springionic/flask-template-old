# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/19

from flask import url_for

from app.components.logger import get_logger
from tests.conftest import http_req

log = get_logger(__name__)


class TestEdcField(object):
    """edc_field相关单元测试"""
    def test_edc_field_add(self, client):
        payload = {'form_id': 1, 'field_name': '字段1', 'field_name_en': 'field_one', 'field_format': '单选'}
        payload2 = {'form_id': 2, 'field_name': '字段2', 'field_name_en': 'field_two', 'field_format': '多选'}
        resp_json = http_req(client, url_for('edc.field-add'), method='POST', payload=payload)
        resp_json2 = http_req(client, url_for('edc.field-add'), method='POST', payload=payload2)
        log.info(str(resp_json)+str(resp_json2))
        assert resp_json['code'] == 0 and resp_json2['code'] == 0

    def test_edc_field_list(self, client):
        payload = {'form_id': 1}
        resp_json = http_req(client, url_for('edc.field-list'), method='GET', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_field_update(self, client):
        payload = {'field_id': 2, 'field_format': '单选', 'field_range': '0-10'}
        resp_json = http_req(client, url_for('edc.field-update'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_field_delete(self, client):
        payload = {'field_id': 2}
        resp_json = http_req(client, url_for('edc.field-delete'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_field_sort(self, client):
        payload = {'form_id': 1, 'field_ids': [1, 2]}
        resp_json = http_req(client, url_for('edc.field-sort'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_field_copy(self, client):
        payload = {'field_id': 1, 'form_id': 1, 'count': 2}
        resp_json = http_req(client, url_for('edc.field-copy'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0


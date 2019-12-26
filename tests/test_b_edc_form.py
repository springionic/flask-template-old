# -*- coding: utf-8 -*-
# Created by lilei at 2019/12/19

from flask import url_for

from app.components.logger import get_logger
from tests.conftest import http_req

log = get_logger(__name__)


class TestEdcForm(object):
    """edc_form相关单元测试"""
    def test_edc_form_add(self, client):
        payload = {'visit_id': 1, 'form_name': '表单1', 'form_remark': '备注1', 'form_repeat': '否'}
        payload2 = {'visit_id': 1, 'form_name': '表单2', 'form_remark': '备注2', 'form_repeat': '否'}
        resp_json = http_req(client, url_for('edc.form-add'), method='POST', payload=payload)
        resp_json2 = http_req(client, url_for('edc.form-add'), method='POST', payload=payload2)
        log.info(str(resp_json)+str(resp_json2))
        assert resp_json['code'] == 0 and resp_json2['code'] == 0

    def test_edc_form_list(self, client):
        payload = {'visit_id': 1}
        resp_json = http_req(client, url_for('edc.form-list'), method='GET', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_form_sort(self, client):
        payload = {'visit_id': 1, 'form_ids': [2, 1]}
        resp_json = http_req(client, url_for('edc.form-sort'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_form_update(self, client):
        payload = {'form_id': 2, 'form_name': '新表单2', 'form_remark': '新备注2', 'form_repeat': '是'}
        resp_json = http_req(client, url_for('edc.form-update'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_form_delete(self, client):
        payload = {'form_id': 2}
        resp_json = http_req(client, url_for('edc.form-delete'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

    def test_edc_form_copy(self, client):
        payload = {'visit_id': 1, 'form_ids': [1]}
        resp_json = http_req(client, url_for('edc.form-copy'), method='POST', payload=payload)
        log.info(str(resp_json))
        assert resp_json['code'] == 0

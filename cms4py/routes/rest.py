from ..commons.Cms4pyRequestContext import Cms4pyRequestContext
from pydal.restapi import RestAPI, Policy
import tornado.escape
from ..actions import do_action

policy = Policy()
policy.set('*', 'GET', authorize=lambda tablename, id, get_vars, post_vars: True, allowed_patterns=['*'])


class DbAPI(Cms4pyRequestContext):
    # def get(self, table, record_id):
    #     get_vars = {}
    #     for key in self.request.query_arguments:
    #         get_vars[key] = self.get_query_argument(key)
    #     rest_api = RestAPI(self.db, policy)
    #     result = rest_api(self.request.method, table, record_id, get_vars)
    #     self.write(tornado.escape.json_encode(result))
    pass


class Action(Cms4pyRequestContext):
    def common_request(self, action):
        self.write(tornado.escape.json_encode(do_action(action, self)))

    def get(self, action):
        self.common_request(action)

    def post(self, action):
        self.common_request(action)

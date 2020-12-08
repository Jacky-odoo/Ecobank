from locust import  TaskSet, task
from OdooLocust import OdooLocust


class SellerTaskSet(TaskSet):
    @task(10)
    def read_partners(self):
        cust_model = self.client.get_model('res.partner')
        cust_ids = cust_model.search([])
        prtns = cust_model.read(cust_ids)
    @task(5)
    def read_products(self):
        prod_model = self.client.get_model('product.product')
        ids = prod_model.search([])
        prods = prod_model.read(ids)


class Seller(OdooLocust):
    host = "127.0.0.1"
    database = "test"
    port = 8015
    login = "admin"
    password = "admin"
    protocol = "jsonrpc"
    user_id = -1
    min_wait = 100
    max_wait = 1000
    weight = 3
    task_set = SellerTaskSet

import logging
import connexion
import unittest

from swagger_server.encoder import JSONEncoder


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        self.app = app.app
        self.client = self.app.test_client()  # Crea un cliente de prueba para la aplicación

    def tearDown(self):
        pass  # Puedes agregar limpieza de recursos si es necesario


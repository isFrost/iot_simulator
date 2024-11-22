from controllers.db_controller import DBController


controller = DBController()    # create database controller
while True:
    controller.consume()    # start consuming data from Kafka

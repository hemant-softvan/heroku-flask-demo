import time
from flask_api import status
from config import MyLogger
from src import que_conn, redis_obj

logger = MyLogger().get_logger("station_service_logger")


class StationService:

    # This function is used to create station
    def create_station(self, station_value):
        try:
            # header = request.headers['token']
            logger.info("station_value : {}".format(station_value))
            time.sleep(20)
            return StationService.response(status.HTTP_200_OK, "Ok", "Success!", None)
        except Exception as ex:
            logger.info("exception occurred in create station function : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", ex.__doc__, None)

    # This function is used to get wigos details
    def get_wigos(self, primary_wigos_id):
        try:
            logger.info("primary_wigos_id : {}".format(primary_wigos_id))
            time.sleep(15)
            return StationService.response(status.HTTP_200_OK, "Ok", "Success!", None)
        except Exception as get_ex:
            logger.info("exception occurred in get wigo function : {}".format(get_ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", get_ex.__doc__, None)

    # This function is used to update wigos details
    def update_wigos(self, wigos_details):
        try:
            logger.info("wigos_details : {}".format(wigos_details))
            time.sleep(15)
            return StationService.response(status.HTTP_200_OK, "Ok", "Success!", None)
        except Exception as get_ex:
            logger.info("exception occurred in get wigos function : {}".format(get_ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", get_ex.__doc__, None)

    # This function is used to create API response.
    @staticmethod
    def response(status_code, response_status, message, data):
        return {
                   "status": response_status,
                   "message": message,
                   "data": data
               }, status_code

    @staticmethod
    def common_validation(request):

        if not request.data or len(request.json) == 0:
            return "please enter the request data"

        if "token" not in request.headers or not request.headers['token']:
            return "please enter the token"

        if len(request.json) > 25:
            return "you can not insert more than 25 row"

        else:
            return None

    # This function is used to validate request
    @staticmethod
    def request_create_validation(request, schema):
        try:
            message = StationService.common_validation(request)
            if message:
                return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", message, None)

            for req in request.json:
                errors = schema.validate(req)
                if errors:
                    return StationService.response(status.HTTP_400_BAD_REQUEST, "Error",
                                                   "problem occurred in row number : " + str(req['rowNumber']),
                                                   errors)
        except Exception as ex:
            logger.error("exception occurred in request validation function : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", ex.__doc__, None)

    @staticmethod
    def request_get_wigos_validation(request):
        try:
            message = StationService.common_validation(request)

            if message:
                return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", message, None)

            if not "primaryWigosId" in request.json[0]:
                return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", "primaryWigosId not found.", None)

            for res in request.json:
                if not res["primaryWigosId"]:
                    return StationService.response(status.HTTP_400_BAD_REQUEST, "Error",
                                                   "primaryWigosId must be non empty",
                                                   None)

        except Exception as ex:
            logger.error("exception occurred in get wigos validation function : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", ex.__doc__, None)

    @staticmethod
    def create_queue_job(response, function):
        try:
            task = que_conn.enqueue(function, response)
            return task, 200
        except Exception as red_exc:
            logger.info("Not able to connect or something went wrong due to : {}".format(red_exc))
            return StationService.response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error", str(red_exc), None), 500

    @staticmethod
    def request_update_wigos_validation(request, schema):

        try:
            message = StationService.common_validation(request)
            if message:
                return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", message, None)

            for req in request.json:
                if "primaryWigosId" not in req:
                    return StationService.response(status.HTTP_400_BAD_REQUEST, "Error",
                                                   "primaryWigosId not found",
                                                   None)
                elif "primaryWigosId" in req and not req["primaryWigosId"]:
                    return StationService.response(status.HTTP_400_BAD_REQUEST, "Error",
                                                   "primaryWigosId must not be empty",
                                                   None)
                errors = schema.validate(req)
                if errors:
                    return StationService.response(status.HTTP_400_BAD_REQUEST, "Error",
                                                   "problem occurred in WIGOS Id : " + str(req['primaryWigosId']),
                                                   errors)
        except Exception as ex:
            logger.error("exception occurred in request validation in update wigos function : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", ex.__doc__, None)

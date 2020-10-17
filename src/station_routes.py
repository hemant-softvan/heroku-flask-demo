from flask import request, jsonify
from flask_api import status
from src.station_schema import create_station_schema, update_wigos_schema
from src.station_services import StationService
from flask import Blueprint
from src import que_conn, redis_obj
from rq.job import Job
from flask_restplus import Resource, Api
from config import MyLogger
from flask_restplus import apidoc
from flask import current_app as app

logger = MyLogger().get_logger("station_route_logger")

STATION_BLUEPRINT = Blueprint('station_blueprint',
                              __name__,
                              url_prefix='/v1',
                              )

api = Api(app=app, UI=False, doc=False)  # For Swagger off

station_ns = api.namespace('v1', description='Create Station')

# api.init_app(STATION_BLUEPRINT)
api.add_namespace(station_ns)

station_service = StationService()


@STATION_BLUEPRINT.route('/api/doc/', endpoint='doc')
def swagger_ui():
    """
    This function is used for swagger implementation.
    """
    return apidoc.ui_for(api)


@station_ns.route("/createStation")
class CreateStation(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @api.header('token', 'Some class header')
    def post(self):
        """
        This function is used to crete station using redis queue functionality for each row.
        """
        create_station_response = []
        logger.info("request : {}".format(request))
        try:
            create_errors = StationService.request_create_validation(request, create_station_schema)
            if not create_errors:
                for station in request.json:
                    logger.info("station : {}".format(station))
                    station_task_res, status_code = StationService.create_queue_job(station, station_service.create_station)
                    if status_code == 200:
                        create_station_response.append({"job_id": station_task_res.id, "request_body": station})
                    else:
                        return station_task_res
                return create_station_response
            else:
                return create_errors
        except KeyError as ex:
            logger.error("key error exception occurred in create station class : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", ex.__doc__, None)
        except Exception as ex:
            logger.error("exception occurred in create station class : {}".format(ex))
            return StationService.response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error", ex.__doc__, None)


@station_ns.route("/checkStatus")
class CheckStatusAndResult(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @api.header('token', 'Some class header')
    def get(self):
        """
        This function is used to get status and result of redis using job id.
        """
        result = {}
        if request.args and request.args["jobId"]:
            job_id = request.args["jobId"]
            try:
                job = Job.fetch(job_id, connection=redis_obj)
                if job and job.get_status() == "finished":
                    result = job.result
                return jsonify({"job_id": job.id, "job_status": job.get_status(), "job_result": result})
            except Exception as exc:
                return StationService.response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error", exc.__doc__, None)
        else:
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", "please enter jobId", None)


@station_ns.route("/getWigos")
class GetStation(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @api.header('token', 'Some class header')
    def post(self):
        """
        This function is used to get station response using redis queue functionality for each row.
        """
        logger.info("request : {}".format(request))
        wigos_response = []
        try:
            wigos_errors = StationService.request_get_wigos_validation(request)
            if not wigos_errors:
                for wigos_res in request.json:
                    wigos_id = wigos_res['primaryWigosId']
                    logger.info("wigos_id : {}".format(wigos_id))
                    wigos_task, status_code = StationService.create_queue_job(wigos_id, station_service.get_wigos)
                    if status_code == 200:
                        wigos_response.append({"job_id": wigos_task.id, "request_body": wigos_res})
                    else:
                        return wigos_task
                return wigos_response
            else:
                return wigos_errors
        except KeyError as ex:
            logger.error("key error exception occurred in get wigos class : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", ex.__doc__, None)
        except Exception as ex:
            logger.error("exception occurred in  get wigos class : {}".format(ex))
            return StationService.response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error", ex.__doc__, None)


@station_ns.route("/updateWigos")
class UpdateWigos(Resource):
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @api.header('token', 'Some class header')
    def post(self):
        """
        This function is used to crete station using redis queue functionality for each row.
        """
        update_station_response = []
        logger.info("request : {}".format(request))
        try:
            update_errors = StationService.request_update_wigos_validation(request, update_wigos_schema)
            if not update_errors:
                for wigos_update_res in request.json:
                    logger.info("wigos_update_res : {}".format(wigos_update_res))
                    update_task_res, status_code = StationService.create_queue_job(wigos_update_res,
                                                                                   station_service.update_wigos)
                    if status_code == 200:
                        update_station_response.append({"job_id": update_task_res.id, "request_body": wigos_update_res})
                    else:
                        return update_task_res
                return update_station_response
            else:
                return update_errors
        except KeyError as ex:
            logger.error("key error exception occurred in update wigos class : {}".format(ex))
            return StationService.response(status.HTTP_400_BAD_REQUEST, "Error", str(ex), None)
        except Exception as ex:
            logger.error("exception occurred in update wigos class : {}".format(ex))
            return StationService.response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error", str(ex), None)




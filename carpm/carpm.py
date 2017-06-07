import requests

import copy

from attrdict import AttrDict


class CarpmApiException(Exception):

    def __init__(self, status):
        description_map = {
            400: "Bad Request",
            401: "Your Access Token is wrong/expired",
            403: "Forbidden - The resourse requested is hidden for administrators only",
            404: "Not Found - The specified resource cannot be found.",
            405: "Method Not Allowed",
            406: "Not Acceptable - You requested a format that isn't json",
            422: "Inspection was not completed",
            429: "Too Many Requests",
            500: "Internal Server Error",
            503: "Service Unavailable"
        }
        self.status = status
        self.description = description_map[status]
        super(CarpmApiException, self).__init__(self.description)

    def to_dict(self):
        return {
            'status': self.status,
            'description': self.description
        }

    def __str__(self):
        return super(CarpmApiException, self).__str__()


class CarpmClient(object):

    def __init__(self, auth_token, email):
        if auth_token is None:
            raise Exception('auth token not defined')
        self.auth_token = auth_token
        self.email = email

    def convert_format(self, carpm_report, replacement_map):
        replacement_map_default = {'license_plate': 'registration_no', 'appointment_id': 'registration_no', 'car_model': 'model',
                                   'car': 'make', 'time': 'inspection_time',
                                   'engine_report': {}
                                   }
        replacement_map = replacement_map if replacement_map is not None else replacement_map_default
        carpm_report_old = carpm_report
        carpm_report_old['fuel_type'] = carpm_report_old['fuel_type'].upper()
        carpm_report_new = copy.deepcopy(carpm_report)

        for key in carpm_report_new.keys():
            if (key in replacement_map and key != 'engine_report') and (key != replacement_map[key]):
                    carpm_report_new[replacement_map[key]] = carpm_report_old[key]
                    carpm_report_new.pop(key, None)

        for key in carpm_report_new['engine_report'].keys():
            if (key in replacement_map['engine_report']) and (key != replacement_map['engine_report'][key]):
                    carpm_report_new['engine_report'][replacement_map['engine_report'][key]] = carpm_report_old['engine_report'][key]
                    carpm_report_new['engine_report'].pop(key, None)

        return AttrDict(carpm_report_new)

    def get_reports_list(self):

        url = "https://carpm.in/user_car_models/get_reports"

        headers = {
            'content-type': "application/json",
            'accept': "application/json",
            'x-user-email': self.email,
            'x-user-token': self.auth_token,
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code is not 200:
            raise CarpmApiException(response.status_code)
        return AttrDict(response.json())

    def get_vehicle_report(self, inspector_email, user_car_model_id, **kwargs):
        replacement_map = kwargs.get('replacement_map', None)

        url = "https://carpm.in/old_car/engine_reports/report"

        querystring = {"inspector_email": inspector_email, "user_car_model_id": user_car_model_id}
        headers = {
            'content-type': "application/json",
            'accept': "application/json",
            'x-user-email': self.email,
            'x-user-token': self.auth_token,
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code is not 200:
            raise CarpmApiException(response.status_code)

        return self.convert_format(response.json(), replacement_map)

    def handle_webhook(self, data, method_dict):
        user_car_model_id = (data.get('user_car_model_id') or None)
        inspector_email = (data.get('inspector_email') or None)
        event = (data.get('event') or None)
        registration_no = (data.get('appointment_id') or None)

        if registration_no is None or user_car_model_id is None or inspector_email is None or event is None:
            raise CarpmApiException(400)

        if event == "Report Generation Successful" and "REPORT_GENERATED" in method_dict:
            method_dict["REPORT_GENERATED"](inspector_email, registration_no, user_car_model_id)
        elif event == "Report Generation Failed" and "REPORT_FAILED" in method_dict:
            method_dict["REPORT_FAILED"](inspector_email, registration_no)
        elif event == "Data Received" and "INSPECTION_COMPLETE" in method_dict:
            method_dict["INSPECTION_COMPLETE"](inspector_email, registration_no)

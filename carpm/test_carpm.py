from __future__ import absolute_import
from __future__ import division

from carpm import CarpmClient, CarpmApiException
import pytest

carpm_client = CarpmClient("None", "None")
handle_webhook = carpm_client.handle_webhook
convert_format = carpm_client.convert_format


class TestCarpm(object):
    method_called = None

    def on_report(self, details):
        self.method_called = "on_report"

    def on_inspection(self, details):
        self.method_called = "on_inspection"

    def on_report_failed(self, details):
        self.method_called = "on_report_failed"

    @pytest.mark.parametrize(
        'event, method_called', [
            ("Data Received", "on_inspection"),
            ("Report Generation Failed", "on_report_failed"),
            ("Report Generation Successful", "on_report")
        ]
    )
    def test_handle_webhook(self, event, method_called):
        data = {
            "user_car_model_id": 17922,
            "inspector_email": "email@example.com",
            "event": event,
            "appointment_id": "DL1CAB0003"
        }
        handle_webhook(data, {'INSPECTION_COMPLETE': self.on_inspection, 'REPORT_GENERATED': self.on_report, 'REPORT_FAILED': self.on_report_failed})
        assert self.method_called == method_called

    @pytest.mark.parametrize(
        'registration_no, user_car_model_id, inspector_email, event', [
            (None, 1234, 'email@example.com', 'Data Received'),
            ('DL1CAB0003', None, 'email@example.com', 'Data Received'),
            ('DL1CAB0003', 1234, None, 'Data Received'),
            ('DL1CAB0003', 1234, 'email@example.com', None),
        ]
    )
    def test_webhook_handler_exceptions(self, registration_no, user_car_model_id, inspector_email, event):
        data = {'appointment_id': registration_no, 'user_car_model_id': user_car_model_id, 'inspector_email': inspector_email, 'event': event}
        with pytest.raises(CarpmApiException) as exc_info:
            handle_webhook(data, {'INSPECTION_COMPLETE': self.on_inspection, 'REPORT_GENERATED': self.on_report, 'REPORT_FAILED': self.on_report_failed})
        assert exc_info.value.__str__() == CarpmApiException(400, description='registration_no, user_car_model_id, inspector email and event is required').__str__()


def test_no_replacementmap_return():
    original_report = {
        "appointment_id": "KA05MS7503",
        "age": 1,
        "odometer_reading": 5483,
        "car": "Honda City",
        "car_model": "1.5 EXI",
        "fuel_type": "Petrol",
        "status": True,
        "inspection_time": "2017-05-27T09:09:23.288+05:30",
        "inspector_name": "Madhusudan",
        "inspector_email": "madhu@loanzen.in",
        "engine_report": {
            "fuel_economy": None,
            "max_hp": None,
            "avg_torque": None,
            "fuel_system": True,
            "fuel_trim": True,
            "fuel_pressure": None,
            "engine_misfire": True,
            "max_coolant_temp": 74,
            "battery_voltage": 13.8,
            "dist_with_mil_on": None,
            "odometer_fraud": True,
            "max_boost_pressure": None,
            "trip_distance": 0,
            "trip_duration": 42,
            "max_fuel_economy": None,
            "fuel_and_air_metering": True,
            "injector_circuit": True,
            "ignition_system": True,
            "auxiliary_emissions_control": True,
            "computer_output_circuit": True,
            "transmission_system": True,
            "vehicle_speed_and_idle_control_system": True,
            "engine_knocking": True,
            "coolant_temp_status": True,
            "max_speed": 0,
            "idling_rpm_status": 1,
            "rating": 4.81391585760518
        },
        "current_fault_codes": [],
        "upcoming_fault_codes": [],
        "engine_part_failure": []
    }
    expected_report = {
        "registration_no": "KA05MS7503",
        "age": 1,
        "odometer_reading": 5483,
        "make": "Honda City",
        "model": "1.5 EXI",
        "fuel_type": "PETROL",
        "status": True,
        "inspection_time": "2017-05-27T09:09:23.288+05:30",
        "inspector_name": "Madhusudan",
        "inspector_email": "madhu@loanzen.in",
        "engine_report": {
            "fuel_economy": None,
            "max_hp": None,
            "avg_torque": None,
            "fuel_system": True,
            "fuel_trim": True,
            "fuel_pressure": None,
            "engine_misfire": True,
            "max_coolant_temp": 74,
            "battery_voltage": 13.8,
            "dist_with_mil_on": None,
            "odometer_fraud": True,
            "max_boost_pressure": None,
            "trip_distance": 0,
            "trip_duration": 42,
            "max_fuel_economy": None,
            "fuel_and_air_metering": True,
            "injector_circuit": True,
            "ignition_system": True,
            "auxiliary_emissions_control": True,
            "computer_output_circuit": True,
            "transmission_system": True,
            "vehicle_speed_and_idle_control_system": True,
            "engine_knocking": True,
            "coolant_temp_status": True,
            "max_speed": 0,
            "idling_rpm_status": 1,
            "rating": 4.81391585760518
        },
        "current_fault_codes": [],
        "upcoming_fault_codes": [],
        "engine_part_failure": []
    }
    converted_report = convert_format(original_report, None)
    assert converted_report == expected_report


def test_with_replacementmap_return():
    original_report = {
        "appointment_id": "KA05MS7503",
        "age": 1,
        "odometer_reading": 5483,
        "car": "Honda City",
        "car_model": "1.5 EXI",
        "fuel_type": "Petrol",
        "status": True,
        "inspection_time": "2017-05-27T09:09:23.288+05:30",
        "inspector_name": "Madhusudan",
        "inspector_email": "madhu@loanzen.in",
        "engine_report": {
            "fuel_economy": 11,
            "max_hp": 8,
            "avg_torque": None,
            "fuel_system": True,
            "fuel_trim": True,
            "fuel_pressure": None,
            "engine_misfire": True,
            "max_coolant_temp": 74,
            "battery_voltage": 13.8,
            "dist_with_mil_on": None,
            "odometer_fraud": True,
            "max_boost_pressure": None,
            "trip_distance": 0,
            "trip_duration": 42,
            "max_fuel_economy": None,
            "fuel_and_air_metering": True,
            "injector_circuit": True,
            "ignition_system": True,
            "auxiliary_emissions_control": True,
            "computer_output_circuit": True,
            "transmission_system": True,
            "vehicle_speed_and_idle_control_system": True,
            "engine_knocking": True,
            "coolant_temp_status": True,
            "max_speed": 0,
            "idling_rpm_status": 1,
            "rating": 4.81391585760518
        },
        "current_fault_codes": [],
        "upcoming_fault_codes": [],
        "engine_part_failure": []
    }
    expected_report = {
        "appointment_id": "KA05MS7503",
        "age": 1,
        "distance_travelled": 5483,
        "make": "Honda City",
        "car_model": "1.5 EXI",
        "fuel_type": "PETROL",
        "status": True,
        "inspection_time": "2017-05-27T09:09:23.288+05:30",
        "inspector_name": "Madhusudan",
        "inspector_email": "madhu@loanzen.in",
        "engine_report": {
            "mileage": 11,
            "horse_power": 8,
            "avg_torque": None,
            "fuel_system": True,
            "fuel_trim": True,
            "fuel_pressure": None,
            "engine_misfire": True,
            "max_coolant_temp": 74,
            "battery_voltage": 13.8,
            "dist_with_mil_on": None,
            "odometer_fraud": True,
            "max_boost_pressure": None,
            "trip_distance": 0,
            "trip_duration": 42,
            "max_fuel_economy": None,
            "fuel_and_air_metering": True,
            "injector_circuit": True,
            "ignition_system": True,
            "auxiliary_emissions_control": True,
            "computer_output_circuit": True,
            "transmission_system": True,
            "vehicle_speed_and_idle_control_system": True,
            "engine_knocking": True,
            "coolant_temp_status": True,
            "max_speed": 0,
            "idling_rpm_status": 1,
            "rating": 4.81391585760518
        },
        "current_fault_codes": [],
        "upcoming_fault_codes": [],
        "engine_part_failure": []
    }
    replacement_map = {'odometer_reading': 'distance_travelled',
                       'car': 'make', 'time': 'inspection_time',
                       'engine_report': {"fuel_economy": "mileage", "max_hp": "horse_power"}
                       }
    converted_report = convert_format(original_report, replacement_map)
    assert converted_report == expected_report

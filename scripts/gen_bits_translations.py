"""Generate binary_sensor name maps for en/ru (run from repo root)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BITS = ROOT / "custom_components/east_ea900_g4_ups/discrete_bits.py"

EN = {
    "bus_high_voltage": "BUS high voltage",
    "bus_low_voltage": "BUS low voltage",
    "bus_unbalanced": "BUS unbalanced",
    "bus_soft_start_failure": "BUS soft start failure",
    "inverter_soft_start_failure": "Inverter soft start failure",
    "inverter_high_voltage": "Inverter high voltage",
    "inverter_low_voltage": "Inverter low voltage",
    "inverter_prohibited": "Inverter prohibited",
    "overtemperature": "Overtemperature",
    "output_short_circuit": "Output short circuit",
    "overload_fault": "Overload fault",
    "negative_power_abnormality": "Negative power abnormality",
    "shutdown_fault": "Shutdown fault",
    "parallel_ups_software_mismatch": "Parallel UPS software version mismatch",
    "sync_signal_abnormality_unused": "Sync signal abnormality (unused)",
    "sync_pulse_abnormality": "Sync pulse abnormality",
    "inverter_relay_adhesion": "Inverter relay adhesion",
    "bus_short_circuit": "BUS short circuit",
    "can_communication_abnormality": "CAN communication abnormality",
    "physical_address_conflict": "Physical address conflict",
    "parallel_ups_model_incompatible": "Parallel UPS model incompatible",
    "wrong_battery_numbers": "Wrong battery numbers",
    "input_scr_soft_start_failure": "Input SCR soft start failure",
    "rectifier_scr_fault_unused": "Rectifier SCR fault (unused)",
    "inverter_abnormality": "Inverter abnormality",
    "incorrect_parallel_bypass_wiring": "Incorrect parallel bypass wiring",
    "inverter_open_circuit": "Inverter open circuit",
    "pfc_abnormality": "PFC abnormality",
    "inverter_capacitor_abnormality": "Inverter capacitor abnormality",
    "fan_failed": "Fan failure",
    "epo": "EPO",
    "auxiliary_power_lost": "Auxiliary power lost",
    "parallel_cables_abnormal": "Parallel cables connection abnormal",
    "parallel_ups_settings_error": "Parallel UPS settings error",
    "reversed_battery_connection": "Reversed battery connection",
    "overload_alarm": "Overload alarm",
    "battery_disconnected": "Battery disconnected",
    "input_overcurrent": "Input overcurrent",
    "high_battery_voltage": "High battery voltage",
    "startup_abnormality": "Startup abnormality",
    "charger_failure": "Charger failure",
    "eeprom_abnormality": "EEPROM abnormality",
    "input_overcurrent_overtime": "Input overcurrent overtime",
    "low_battery_voltage_fault": "Low battery voltage",
    "ad_sampling_abnormality": "AD sampling abnormality",
    "sync_pulse_abnormality_2": "Sync pulse abnormality",
    "sync_signal_abnormality_2": "Sync signal abnormality",
    "can_communication_abnormality_2": "CAN communication abnormality",
    "high_bypass_voltage": "High bypass voltage",
    "bypass_fault": "Bypass fault",
    "mains_high_voltage": "Mains high voltage",
    "mains_frequency_abnormal": "Mains frequency abnormal",
    "bypass_frequency_out_of_tracking": "Bypass frequency out of tracking",
    "bypass_to_inverter_switching_limited": "Bypass to inverter switching limited",
    "battery_end_of_discharge": "Battery end of discharge",
    "battery_test_success": "Battery test successful",
    "power_on_prohibited": "Power-on prohibited",
    "battery_test_failed": "Battery test failed",
    "parallel_current_sharing_abnormality": "Parallel current sharing abnormality",
    "inverter_phase_lock_abnormality": "Inverter phase lock abnormality",
    "battery_maintenance_success": "Battery maintenance successful",
    "battery_maintenance_abnormality": "Battery maintenance abnormality",
    "input_current_unbalanced": "Input current unbalanced",
    "pfc_abnormality_2": "PFC abnormality",
    "bus_low_to_battery_switching_limited": "BUS low to battery switching limited",
    "mains_abnormality": "Mains abnormal",
    "bypass_abnormality": "Bypass abnormal",
    "bypass_frequency_abnormality": "Bypass frequency abnormal",
    "inconsistent_inverter_output_voltage_detection": (
        "Inconsistent inverter output voltage detection"
    ),
    "battery_voltage_abnormality": "Battery voltage abnormality",
    "inconsistent_bypass_output_voltage_detection": (
        "Inconsistent bypass output voltage detection"
    ),
    "instable_load_unused": "Unstable load (unused)",
    "maintain_bypass_enabled": "Maintenance bypass enabled",
    "frequent_overtemperature": "Frequent overtemperature",
    "parallel_battery_count_inconsistent": "Parallel battery count inconsistent",
    "battery_temp_compensation_abnormal_unused": (
        "Battery temperature compensation abnormal (unused)"
    ),
    "instable_bypass_voltage_unused": "Unstable bypass voltage (unused)",
    "test_mode": "Test mode",
    "overload_frequently": "Overload frequently",
}

RU = {
    "bus_high_voltage": "Повышенное напряжение шины (BUS)",
    "bus_low_voltage": "Пониженное напряжение шины (BUS)",
    "bus_unbalanced": "Дисбаланс шины (BUS)",
    "bus_soft_start_failure": "Сбой плавного пуска шины (BUS)",
    "inverter_soft_start_failure": "Сбой плавного пуска инвертора",
    "inverter_high_voltage": "Повышенное напряжение инвертора",
    "inverter_low_voltage": "Пониженное напряжение инвертора",
    "inverter_prohibited": "Инвертор запрещён",
    "overtemperature": "Перегрев",
    "output_short_circuit": "Короткое замыкание на выходе",
    "overload_fault": "Авария перегрузки",
    "negative_power_abnormality": "Аномалия обратной мощности",
    "shutdown_fault": "Авария при отключении",
    "parallel_ups_software_mismatch": "Несовпадение версий ПО параллельных ИБП",
    "sync_signal_abnormality_unused": "Аномалия сигнала синхронизации (не используется)",
    "sync_pulse_abnormality": "Аномалия импульса синхронизации",
    "inverter_relay_adhesion": "Залипание реле инвертора",
    "bus_short_circuit": "Короткое замыкание шины (BUS)",
    "can_communication_abnormality": "Аномалия связи CAN",
    "physical_address_conflict": "Конфликт физического адреса",
    "parallel_ups_model_incompatible": "Несовместимость моделей параллельных ИБП",
    "wrong_battery_numbers": "Неверное количество АКБ",
    "input_scr_soft_start_failure": "Сбой плавного пуска входного SCR",
    "rectifier_scr_fault_unused": "Неисправность SCR выпрямителя (не используется)",
    "inverter_abnormality": "Аномалия инвертора",
    "incorrect_parallel_bypass_wiring": "Неверная разводка байпаса параллельных ИБП",
    "inverter_open_circuit": "Обрыв цепи инвертора",
    "pfc_abnormality": "Аномалия PFC",
    "inverter_capacitor_abnormality": "Аномалия конденсаторов инвертора",
    "fan_failed": "Отказ вентилятора",
    "epo": "Аварийное отключение (EPO)",
    "auxiliary_power_lost": "Потеря вспомогательного питания",
    "parallel_cables_abnormal": "Аномалия соединения параллельных кабелей",
    "parallel_ups_settings_error": "Ошибка настроек параллельных ИБП",
    "reversed_battery_connection": "Обратное подключение АКБ",
    "overload_alarm": "Предупреждение перегрузки",
    "battery_disconnected": "АКБ отключена",
    "input_overcurrent": "Перегрузка по входному току",
    "high_battery_voltage": "Повышенное напряжение АКБ",
    "startup_abnormality": "Аномалия пуска",
    "charger_failure": "Неисправность зарядного устройства",
    "eeprom_abnormality": "Аномалия EEPROM",
    "input_overcurrent_overtime": "Перегрузка по входному току (время)",
    "low_battery_voltage_fault": "Низкое напряжение АКБ",
    "ad_sampling_abnormality": "Аномалия АЦП",
    "sync_pulse_abnormality_2": "Аномалия импульса синхронизации (2)",
    "sync_signal_abnormality_2": "Аномалия сигнала синхронизации (2)",
    "can_communication_abnormality_2": "Аномалия связи CAN (2)",
    "high_bypass_voltage": "Повышенное напряжение байпаса",
    "bypass_fault": "Неисправность байпаса",
    "mains_high_voltage": "Повышенное напряжение сети",
    "mains_frequency_abnormal": "Аномальная частота сети",
    "bypass_frequency_out_of_tracking": "Частота байпаса вне слежения",
    "bypass_to_inverter_switching_limited": "Ограничение переключений байпас-инвертор",
    "battery_end_of_discharge": "Разряд АКБ (конец разряда)",
    "battery_test_success": "Тест АКБ успешен",
    "power_on_prohibited": "Включение запрещено",
    "battery_test_failed": "Тест АКБ не пройден",
    "parallel_current_sharing_abnormality": "Аномалия разделения тока (параллель)",
    "inverter_phase_lock_abnormality": "Аномалия фазовой синхронизации инвертора",
    "battery_maintenance_success": "Обслуживающий разряд АКБ успешен",
    "battery_maintenance_abnormality": "Аномалия обслуживающего разряда АКБ",
    "input_current_unbalanced": "Дисбаланс входного тока",
    "pfc_abnormality_2": "Аномалия PFC (2)",
    "bus_low_to_battery_switching_limited": "Ограничение переключений BUS low - АКБ",
    "mains_abnormality": "Аномалия сети",
    "bypass_abnormality": "Аномалия байпаса",
    "bypass_frequency_abnormality": "Аномалия частоты байпаса",
    "inconsistent_inverter_output_voltage_detection": (
        "Расхождение детекции вых. напряжения инвертора"
    ),
    "battery_voltage_abnormality": "Аномалия напряжения АКБ",
    "inconsistent_bypass_output_voltage_detection": (
        "Расхождение детекции напряжения байпаса"
    ),
    "instable_load_unused": "Нестабильная нагрузка (не используется)",
    "maintain_bypass_enabled": "Включён обслуживающий байпас",
    "frequent_overtemperature": "Частый перегрев",
    "parallel_battery_count_inconsistent": "Несовпадение числа АКБ (параллель)",
    "battery_temp_compensation_abnormal_unused": (
        "Аномалия темп. компенсации АКБ (не используется)"
    ),
    "instable_bypass_voltage_unused": "Нестабильное напряжение байпаса (не используется)",
    "test_mode": "Режим теста",
    "overload_frequently": "Частая перегрузка",
}


def main() -> None:
    spec = importlib.util.spec_from_file_location("discrete_bits", BITS)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    keys = [t[1] for t in mod.DISCRETE_BIT_SPECS]
    assert set(keys) == set(EN.keys()) == set(RU.keys())
    en_bs = {k: {"name": EN[k]} for k in keys}
    ru_bs = {k: {"name": RU[k]} for k in keys}
    print(json.dumps({"en": en_bs, "ru": ru_bs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

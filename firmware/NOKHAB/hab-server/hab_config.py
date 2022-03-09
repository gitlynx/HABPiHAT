""" HAB Config Module """

import os
import typing
import yaml

_CONFIG_FILE: typing.Optional[str] = None
_CONFIG: typing.Optional[dict] = None

if _CONFIG is None:
    assert "HAB_CONFIG" in os.environ
    config_file = os.environ["HAB_CONFIG"]

    assert os.path.exists(config_file)

    _CONFIG_FILE = config_file
    with open(config_file, 'r', encoding="utf-8") as file:
        _CONFIG = yaml.load(file, Loader=yaml.FullLoader)

HabExperimentConfig: typing.Optional[dict] = _CONFIG["EXPERIMENT"]
HabSensorConfig: typing.Optional[dict]     = _CONFIG["SENSOR"]
HabShellConfig: typing.Optional[dict]      = _CONFIG["SHELL"]
HabLogConfig: typing.Optional[dict]        = _CONFIG["LOG"]

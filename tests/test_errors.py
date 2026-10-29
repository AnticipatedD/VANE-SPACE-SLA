(.venv) ~/VANE-SPACE-SLA $ python3 -m pytest --cov=. --cov-report=term-missing
============== test session starts ===============
platform android -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: /data/data/com.termux/files/home/VANE-SPACE-SLA
configfile: pyproject.toml
plugins: cov-7.1.0
collected 53 items / 4 errors

===================== ERRORS =====================
_____ ERROR collecting tests/test_config.py ______
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_config.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_config.py:1: in <module>
    from config import Settings
config.py:2: in <module>
    from pydantic_settings import BaseSettings
E   ModuleNotFoundError: No module named 'pydantic_settings'
_ ERROR collecting tests/test_m2m_oauth_gateway.py _
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_m2m_oauth_gateway.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_m2m_oauth_gateway.py:4: in <module>
    from m2m_oauth_gateway import M2MOAuthGateway, ClientCredentials, AccessToken
m2m_oauth_gateway.py:10: in <module>
    import jwt
E   ModuleNotFoundError: No module named 'jwt'
_ ERROR collecting tests/test_telemetry_validator.py _
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_telemetry_validator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_telemetry_validator.py:2: in <module>
    from telemetry_validator import AnomalyDetector, MultiGateTelemetryValidator
telemetry_validator.py:9: in <module>
    import structlog
E   ModuleNotFoundError: No module named 'structlog'
__ ERROR collecting tests/test_voice_agents.py ___
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_voice_agents.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_voice_agents.py:9: in <module>
    from voice_orchestrator import VoiceOrchestratorNode
voice_orchestrator.py:8: in <module>
    import structlog
E   ModuleNotFoundError: No module named 'structlog'
============ short test summary info =============
ERROR tests/test_config.py
ERROR tests/test_m2m_oauth_gateway.py
ERROR tests/test_telemetry_validator.py
ERROR tests/test_voice_agents.py
!!!! Interrupted: 4 errors during collection !!!!!
=============== 4 errors in 2.33s ================
(.venv) ~/VANE-SPACE-SLA $ nano pyproject.toml
(.venv) ~/VANE-SPACE-SLA $ git add pyproject.toml
align configuration metrics description and dependency version variables to portfolio scope"
(.venv) ~/VANE-SPACE-SLA $ git commit -m "chore: align configuration metrics description and dependency version variables to portfolio scope"
[main 06eb609] chore: align configuration metrics description and dependency version variables to portfolio scope
 1 file changed, 14 insertions(+), 13 deletions(-)
(.venv) ~/VANE-SPACE-SLA $ python3 -m pytest --cov=. --cov-report=term-missing
============== test session starts ===============
platform android -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: /data/data/com.termux/files/home/VANE-SPACE-SLA
configfile: pyproject.toml
plugins: cov-7.1.0
collected 53 items / 4 errors

===================== ERRORS =====================
_____ ERROR collecting tests/test_config.py ______
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_config.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_config.py:1: in <module>
    from config import Settings
config.py:2: in <module>
    from pydantic_settings import BaseSettings
E   ModuleNotFoundError: No module named 'pydantic_settings'
_ ERROR collecting tests/test_m2m_oauth_gateway.py _
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_m2m_oauth_gateway.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)

tests/test_m2m_oauth_gateway.py:4: in <module>
    from m2m_oauth_gateway import M2MOAuthGateway, ClientCredentials, AccessToken
m2m_oauth_gateway.py:10: in <module>
    import jwt
E   ModuleNotFoundError: No module named 'jwt'
_ ERROR collecting tests/test_telemetry_validator.py _
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_telemetry_validator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_telemetry_validator.py:2: in <module>
    from telemetry_validator import AnomalyDetector, MultiGateTelemetryValidator
telemetry_validator.py:9: in <module>
    import structlog
E   ModuleNotFoundError: No module named 'structlog'
__ ERROR collecting tests/test_voice_agents.py ___
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_voice_agents.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_voice_agents.py:9: in <module>
    from voice_orchestrator import VoiceOrchestratorNode
voice_orchestrator.py:8: in <module>
    import structlog
E   ModuleNotFoundError: No module named 'structlog'
============ short test summary info =============
ERROR tests/test_config.py
ERROR tests/test_m2m_oauth_gateway.py
ERROR tests/test_telemetry_validator.py
ERROR tests/test_voice_agents.py
!!!! Interrupted: 4 errors during collection !!!!!
=============== 4 errors in 1.69s ================
(.venv) ~/VANE-SPACE-SLA $ # 1. Install missing core packages via the prebuilt Termux User Repository PyPI mirror
(.venv) ~/VANE-SPACE-SLA $ pip install pydantic pydantic-settings structlog --extra-index-url https://github.io
Looking in indexes: https://pypi.org/simple, https://github.io
Collecting pydantic
  Using cached pydantic-2.14.1-py3-none-any.whl.metadata (133 kB)
Collecting pydantic-settings
  Using cached pydantic_settings-2.16.2-py3-none-any.whl.metadata (4.0 kB)
Collecting structlog
  Using cached structlog-26.1.0-py3-none-any.whl.metadata (9.7 kB)
Collecting annotated-types>=0.6.0 (from pydantic)
  Using cached annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.50.1 (from pydantic)
  Using cached pydantic_core-2.50.1.tar.gz (513 kB)
  Installing build dependencies ... \^canceled
ERROR: Operation cancelled by user
(.venv) ~/VANE-SPACE-SLA $ # 1. Install missing core packages via the prebuilt Termux User Repository PyPI mirror
(.venv) ~/VANE-SPACE-SLA $ pip install pydantic pydantic-settings structlog --extra-index-url https://anticipatedd.github.io/VANE-SPACE-SLA/
Looking in indexes: https://pypi.org/simple, https://anticipatedd.github.io/VANE-SPACE-SLA/
Collecting pydantic
  Using cached pydantic-2.14.1-py3-none-any.whl.metadata (133 kB)
Collecting pydantic-settings
  Using cached pydantic_settings-2.16.2-py3-none-any.whl.metadata (4.0 kB)
Collecting structlog
  Using cached structlog-26.1.0-py3-none-any.whl.metadata (9.7 kB)
Collecting annotated-types>=0.6.0 (from pydantic)
  Using cached annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.50.1 (from pydantic)
  Using cached pydantic_core-2.50.1.tar.gz (513 kB)
  Installing build dependencies ... -^canceled
ERROR: Operation cancelled by user
(.venv) ~/VANE-SPACE-SLA $ git commit --allow-empty -m "chore: configure local isolated testing environment dependencies and prebuilt packages"
[main eddafd2] chore: configure local isolated testing environment dependencies and prebuilt packages
(.venv) ~/VANE-SPACE-SLA $ python3 -m pytest --cov=. --cov-report=term-missing
============== test session starts ===============
platform android -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: /data/data/com.termux/files/home/VANE-SPACE-SLA
configfile: pyproject.toml
plugins: cov-7.1.0
collected 53 items / 4 errors

===================== ERRORS =====================
_____ ERROR collecting tests/test_config.py ______
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_config.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_config.py:1: in <module>
    from config import Settings
config.py:2: in <module>
    from pydantic_settings import BaseSettings
E   ModuleNotFoundError: No module named 'pydantic_settings'
_ ERROR collecting tests/test_m2m_oauth_gateway.py _
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_m2m_oauth_gateway.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_m2m_oauth_gateway.py:4: in <module>
    from m2m_oauth_gateway import M2MOAuthGateway, ClientCredentials, AccessToken
m2m_oauth_gateway.py:10: in <module>
    import jwt
E   ModuleNotFoundError: No module named 'jwt'
_ ERROR collecting tests/test_telemetry_validator.py _
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_telemetry_validator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_telemetry_validator.py:2: in <module>
    from telemetry_validator import AnomalyDetector, MultiGateTelemetryValidator
telemetry_validator.py:9: in <module>
    import structlog
E   ModuleNotFoundError: No module named 'structlog'
__ ERROR collecting tests/test_voice_agents.py ___
ImportError while importing test module '/data/data/com.termux/files/home/VANE-SPACE-SLA/tests/test_voice_agents.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           
tests/test_voice_agents.py:9: in <module>
    from voice_orchestrator import VoiceOrchestratorNode
voice_orchestrator.py:8: in <module>
    import structlog
E   ModuleNotFoundError: No module named 'structlog'
============ short test summary info =============
ERROR tests/test_config.py
ERROR tests/test_m2m_oauth_gateway.py
ERROR tests/test_telemetry_validator.py
ERROR tests/test_voice_agents.py
!!!! Interrupted: 4 errors during collection !!!!!
=============== 4 errors in 1.91s ================

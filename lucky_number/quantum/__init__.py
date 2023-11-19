
from importlib import import_module
from lucky_number.core import settings
from lucky_number.quantum.executor import *
from lucky_number.quantum.aer_simulator_executor import AerSimulatorExecutor
from lucky_number.quantum.ibmq_hardware_executor import IBMQHardwareExecutor
from lucky_number.quantum.ionq_simulator_executor import IonQSimulatorExecutor


def get_quantum_executor() -> QuantumExecutor:
    module_path_config = settings.get("QUANTUM_EXECUTOR")
    paths = module_path_config.split('.')

    classes_name = paths[paths.__len__() - 1]
    module_path = '.'.join(paths[0:paths.__len__() - 1])

    module = import_module(module_path)

    classes : QuantumExecutor = getattr(module, classes_name)

    if classes and issubclass(classes, QuantumExecutor):
        return classes()

    raise f'no classes in path {module_path_config}'


__all__ = [
    'get_quantum_executor',
    'AerSimulatorExecutor',
    'IBMQHardwareExecutor',
    'IonQSimulatorExecutor'
]
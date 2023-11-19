from qiskit import QuantumCircuit, IBMQ, transpile, execute
from qiskit.result import Result
from lucky_number.core import settings
from lucky_number.quantum.executor import QuantumExecutor
import logging

logger = logging.getLogger(__name__)


class IBMQHardwareExecutor(QuantumExecutor):
    def __init__(self) -> None:
        super().__init__()
        self.ibmq_token = settings.get('IBMQ_TOKEN')
        self.ibmq_backend = settings.get('IBMQ_BACKEND')
        assert self.ibmq_token, "Using IBMQ hardware requires providing IBMQ_TOKEN environment variable"
        assert self.ibmq_backend, "Using IBMQ hardware requires providing IBMQ_BACKEND environment variable"
        self.ibmq_account = IBMQ.enable_account(self.ibmq_token)

    def execute(self, circuit: QuantumCircuit, **kwargs) -> Result:
        # get IBMQ's hardware backend:
        hardware_backend = self.ibmq_account.get_backend(
            self.ibmq_backend or 'ibmq_santiago')

        # transpile for simulator
        circuit = transpile(circuit, hardware_backend)

        # run the circuit on IBMQ platform
        job: Result = execute(circuit, hardware_backend,  **kwargs)

        # return job result when job status is DONE
        return job

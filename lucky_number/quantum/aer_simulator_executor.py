from qiskit import QuantumCircuit, Aer, execute
from qiskit.result import Result
from lucky_number.quantum.executor import QuantumExecutor
import logging

logger = logging.getLogger(__name__)


class AerSimulatorExecutor(QuantumExecutor):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, circuit: QuantumCircuit, **kwargs) -> Result:

        # get IonQ's simulator backend:
        simulator_backend = Aer.get_backend('aer_simulator')

        # run the circuit on ionq platform
        job: Result = execute(circuit, simulator_backend, **kwargs)

        # return job result when job status is DONE
        return job

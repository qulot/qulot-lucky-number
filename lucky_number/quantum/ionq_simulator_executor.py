from qiskit import QuantumCircuit, transpile
from qiskit.result import Result
from qiskit_ionq import IonQProvider
from lucky_number.quantum.executor import QuantumExecutor
import logging

logger = logging.getLogger(__name__)


class IonQSimulatorExecutor(QuantumExecutor):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, circuit: QuantumCircuit, **kwargs) -> Result:
        provider = IonQProvider()

        # get IonQ's simulator backend:
        simulator_backend = provider.get_backend('ionq_simulator')

        transpiled_circuit = transpile(circuit, simulator_backend)

        # run the circuit on ionq platform
        job: Result = simulator_backend.run(transpiled_circuit, **kwargs)

        # perform instructions while waiting for the job to finish.
        self.wait_job_completed(job)

        # return job result when job status is DONE
        return job

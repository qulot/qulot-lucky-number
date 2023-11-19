import abc
import logging
import time

from lucky_number.core import settings
from qiskit import QuantumCircuit
from qiskit.providers.jobstatus import JOB_FINAL_STATES
from qiskit.result import Result

logger = logging.getLogger(__name__)


class QuantumExecutor(metaclass=abc.ABCMeta):
    """Base classes implement quantum service execute job
    """

    @abc.abstractmethod
    def execute(self, circuit: QuantumCircuit, **kwargs) -> Result:
        pass

    def wait_job_completed(self, job: Result) -> Result:
        """Perform instructions while waiting for the job to finish

        Args:
            job (Result): result of execute method

        Returns:
            Result: return job if job has status is DONE, CANCELLED, ERROR
        """

        QUANTUM_JOB_WAIT_TIME = float(
            settings.get('QUANTUM_JOB_WAIT_TIME', 0.5))

        while job.status() not in JOB_FINAL_STATES:
            logger.info(
                f'Waiting for job: {job.job_id()}, status: {job.status()}')

            # await 0.5s the continue to check again
            time.sleep(QUANTUM_JOB_WAIT_TIME)

        return job

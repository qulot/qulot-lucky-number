import logging
import math
import typing
from lucky_number.quantum.executor import QuantumExecutor
from lucky_number.quantum import get_quantum_executor
from lucky_number.random.random_generator import RandomGenerator
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

logger = logging.getLogger(__name__)

_circuit = None
_bitCache = ''


def _set_qubits(n):
    global _circuit
    qr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    _circuit = QuantumCircuit(qr, cr)
    _circuit.h(qr)  # Apply Hadamard gate to qubits
    _circuit.measure(qr, cr)  # Collapses qubit to either 1 or 0 w/ equal prob.


_set_qubits(8)  # Default Circuit is 8 Qubits


def _bit_from_counts(counts):
    '''Strips QISKit output to just a bitstring.
    '''
    return [k for k, v in counts.items() if v == 1][0]


def _request_bits(executor: QuantumExecutor, n: int):
    '''Populates the bitCache with at least n more bits.
    '''
    global _bitCache
    iterations = math.ceil(n/_circuit.width()*2)
    for _ in range(iterations):
        # Create new job and run the quantum circuit
        executor.execute(_circuit)
        # exclude and convert list bit to int value
        result = executor.execute(_circuit, shots=1).result()
        counts = result.get_counts()
        _bitCache += _bit_from_counts(counts)


def get_bit_string(executor: QuantumExecutor, n: int) -> str:
    """
    Returns a random n-bit bitstring.

    Parameters:
        n (int): Account token on IBMQ. If no token is given, will fall back to a local provider.
    """
    global _bitCache
    if len(_bitCache) < n:
        _request_bits(executor, n-len(_bitCache))
    bitString = _bitCache[0:n]
    _bitCache = _bitCache[n:]
    return bitString


# Running time is probabalistic but complexity is still O(n)
def get_random_int(executor: QuantumExecutor, min: int, max: int) -> int:
    """
    Returns a random int from [min, max] (bounds are inclusive).

    Parameters:
        min (int): The minimum possible returned integer.
        max (int): The maximum possible returned integer.
    """
    delta = max-min
    n = math.floor(math.log(delta, 2))+1
    result = int(get_bit_string(executor, n), 2)
    while (result > delta):
        result = int(get_bit_string(executor, n), 2)
    result += min
    return result


class QuantumRandomGenerator(RandomGenerator):

    def __init__(self, *args, **kwargs):
        self.quantum_executor = get_quantum_executor()
        self.executor = self.quantum_executor.__class__.__name__
        logger.info(f"[executor] process using executor: {self.executor}")

    def random_range(self, min: int, max: int):
        logger.info(f"[random_range] input min: {min}, max: {max}")
        number = get_random_int(self.quantum_executor, min, max)
        return number

    def bulk_random_range(
        self,
        bulk: int,
        min: int,
        max: int
    ) -> typing.List[int]:
        numbers = []
        while len(numbers) < bulk:
            number = get_random_int(self.quantum_executor, min, max)
            logger.info(f"[bulk_random_range] random range, min: {min}, max: {max}, result: {number}")
            if number in numbers:
                logger.warn(f"[bulk_random_range] exists the number in the result, continute")
                continue
            numbers.append(number)
        numbers = sorted(numbers)
        logger.info(
            f"[bulk_random_range] output number_of_items: {numbers}")
        return numbers

    def __str__(self):
        return f'{type(self).__name__}:{self.executor}'

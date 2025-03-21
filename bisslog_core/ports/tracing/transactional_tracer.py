"""
Module defining the base class for transactional tracing.
"""

from abc import abstractmethod, ABC
from typing import Optional

from bisslog_core.transactional.transaction_manager import TransactionManager, transaction_manager
from bisslog_core.ports.tracing.tracer import Tracer


class TransactionalTracer(Tracer, ABC):
    """
    Abstract base class for transactional tracing.

    This class extends `Tracer` and provides utility methods for managing
    transaction identifiers and checkpoints. It ensures that all tracing
    implementations handle transactional context correctly.
    """

    @property
    def _transaction_manager(self) -> TransactionManager:
        """
        Provides access to the transaction manager instance.

        Returns
        -------
        TransactionManager
            The singleton instance of the transaction manager.
        """
        return transaction_manager

    def _re_args_with_main(self, transaction_id: Optional[str] = None,
                           checkpoint_id: Optional[str] = None) -> dict:
        """
        Constructs a dictionary containing the main transaction ID and checkpoint ID.

        If the transaction ID is not provided, it retrieves the main transaction ID
        from the transaction manager.

        Parameters
        ----------
        transaction_id : Optional[str], optional
            The transaction ID to use. If None, retrieves the main transaction ID.
        checkpoint_id : Optional[str], optional
            The checkpoint identifier. If None, defaults to an empty string.

        Returns
        -------
        dict
            A dictionary containing `transaction_id` and `checkpoint_id`.
        """
        if transaction_id is None:
            transaction_id = self._transaction_manager.get_main_transaction_id()
        if checkpoint_id is None or not checkpoint_id:
            checkpoint_id = ""
        return {"transaction_id": transaction_id, "checkpoint_id": checkpoint_id}

    def _re_args_with_current(self, transaction_id: Optional[str] = None,
                              checkpoint_id: Optional[str] = None) -> dict:
        """
        Constructs a dictionary containing the current transaction ID and checkpoint ID.

        If the transaction ID is not provided, it retrieves the current transaction ID
        from the transaction manager.

        Parameters
        ----------
        transaction_id : Optional[str], optional
            The transaction ID to use. If None, retrieves the current transaction ID.
        checkpoint_id : Optional[str], optional
            The checkpoint identifier. If None, defaults to an empty string.

        Returns
        -------
        dict
            A dictionary containing `transaction_id` and `checkpoint_id`.
        """
        if transaction_id is None:
            transaction_id = self._transaction_manager.get_transaction_id()
        if checkpoint_id is None or not checkpoint_id:
            checkpoint_id = ""
        return {"transaction_id": transaction_id, "checkpoint_id": checkpoint_id}

    @abstractmethod
    def func_error(self, payload: object, *args, transaction_id: Optional[str] = None,
                   checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """
        Reports a functional error in the tracing system.

        This method must be implemented by subclasses to log functional errors.

        Parameters
        ----------
        payload : object
            The error payload containing relevant data.
        transaction_id : Optional[str], optional
            The transaction ID associated with the error.
        checkpoint_id : Optional[str], optional
            The checkpoint where the error occurred.
        extra : dict, optional
            Additional metadata for tracing.
        """
        raise NotImplementedError("TracingManager must implement method func_error")

    @abstractmethod
    def tech_error(self, payload: object, *args, transaction_id: Optional[str] = None,
                   checkpoint_id: Optional[str] = None, error: Exception = None, extra: dict = None,
                   **kwargs):
        """
        Reports a technical error in the tracing system.

        This method must be implemented by subclasses to log technical errors.

        Parameters
        ----------
        payload : object
            The error payload containing relevant data.
        transaction_id : Optional[str], optional
            The transaction ID associated with the error.
        checkpoint_id : Optional[str], optional
            The checkpoint where the error occurred.
        extra : dict, optional
            Additional metadata for tracing.
        error: Exception
            Captured error to be logged.
        """
        raise NotImplementedError("TracingManager must implement method tech_error")

    @abstractmethod
    def report_start_external(self, payload: object, *args, transaction_id: Optional[str] = None,
                              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """
        Reports the start of an external process in the tracing system.

        This method must be implemented by subclasses to log the start of an
        external interaction.

        Parameters
        ----------
        payload : object
            The payload containing relevant data about the external process.
        transaction_id : Optional[str], optional
            The transaction ID associated with the external process.
        checkpoint_id : Optional[str], optional
            The checkpoint where the external process started.
        extra : dict, optional
            Additional metadata for tracing.
        """
        raise NotImplementedError("TracingManager must implement method report_start_external")

    @abstractmethod
    def report_end_external(self, payload: object, *args, transaction_id: Optional[str] = None,
                            checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """
        Reports the end of an external process in the tracing system.

        This method must be implemented by subclasses to log the completion of an
        external interaction.

        Parameters
        ----------
        payload : object
            The payload containing relevant data about the external process.
        transaction_id : Optional[str], optional
            The transaction ID associated with the external process.
        checkpoint_id : Optional[str], optional
            The checkpoint where the external process ended.
        extra : dict, optional
            Additional metadata for tracing.
        """
        raise NotImplementedError("TracingManager must implement method report_end_external")


    @abstractmethod
    def info(self, payload: object, *args, transaction_id: Optional[str] = None,
             checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs an informational message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
            extra : dict, optional
            Additional context information for debugging.
        """
        raise NotImplementedError("TracingManager must implement method info")

    @abstractmethod
    def debug(self, payload: object, *args, transaction_id: Optional[str] = None,
                 checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a debug message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging.
        """
        raise NotImplementedError("TracingManager must implement method debug")

    @abstractmethod
    def warning(self, payload: object, *args, transaction_id: Optional[str] = None,
                 checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a warning message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging.
        """
        raise NotImplementedError("TracingManager must implement method warning")

    @abstractmethod
    def error(self, payload: object, *args, transaction_id: Optional[str] = None,
              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs an error message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging.
        """
        raise NotImplementedError("TracingManager must implement method error")

    @abstractmethod
    def critical(self, payload: object, *args, transaction_id: Optional[str] = None,
                 checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a critical error message.

        Parameters
        ----------
        payload : object
            The data or message to be logged.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging.
        """
        raise NotImplementedError("TracingManager must implement method critical")

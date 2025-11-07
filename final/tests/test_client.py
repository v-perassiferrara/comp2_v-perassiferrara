import unittest
from unittest.mock import patch, MagicMock, mock_open
import argparse
import socket
import io

from src.client.client import main
from src.shared.utils import DEFAULT_PORT, DEFAULT_HOST


class TestClient(unittest.TestCase):
    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="test data")
    @patch("src.client.client.socket.socket")
    def test_main_success_ipv4(self, mock_socket, mock_open_func, mock_argparse):
        """Testea el flujo exitoso del cliente con una conexión IPv4."""
        # Setup de mocks
        mock_args = argparse.Namespace(
            filepath="chat.txt", host="127.0.0.1", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_socket_instance = MagicMock()
        # Asegurarse que recv devuelve una secuencia que termina
        mock_socket_instance.recv.side_effect = [b'{"status": "ok"}', b""]
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        # Redireccionar stdout para verificar la salida
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()

        # Verificaciones
        mock_open_func.assert_called_once_with("chat.txt", "r", encoding="utf-8")
        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket_instance.connect.assert_called_once_with(
            ("127.0.0.1", DEFAULT_PORT)
        )
        mock_socket_instance.sendall.assert_called_once_with(b"test data")
        mock_socket_instance.shutdown.assert_called_once_with(socket.SHUT_WR)
        self.assertIn("Respuesta recibida", mock_stdout.getvalue())
        self.assertIn('"status": "ok"', mock_stdout.getvalue())

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="test data")
    @patch("src.client.client.socket.socket")
    def test_main_success_ipv6(self, mock_socket, mock_open_func, mock_argparse):
        """Testea el flujo exitoso con host IPv6."""
        mock_args = argparse.Namespace(
            filepath="chat.txt", host="::1", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_socket_instance = MagicMock()
        mock_socket_instance.recv.side_effect = [b'{"status": "ok"}', b""]
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        with patch("sys.stdout", new_callable=io.StringIO):
            main()

        mock_socket.assert_called_with(socket.AF_INET6, socket.SOCK_STREAM)
        mock_socket_instance.connect.assert_called_once_with(("::1", DEFAULT_PORT))

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="test data")
    @patch("src.client.client.socket.socket")
    def test_main_default_host(self, mock_socket, mock_open_func, mock_argparse):
        """Testea que el cliente se conecte al host por defecto si no se especifica."""
        mock_args = argparse.Namespace(
            filepath="chat.txt", host=None, port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_socket_instance = MagicMock()
        mock_socket_instance.recv.side_effect = [b'{"status": "ok"}', b""]
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        with patch("sys.stdout", new_callable=io.StringIO):
            main()

        expected_host = "::1" if ":" in DEFAULT_HOST else "127.0.0.1"
        mock_socket_instance.connect.assert_called_once_with(
            (expected_host, DEFAULT_PORT)
        )

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", side_effect=FileNotFoundError)
    def test_main_file_not_found(self, mock_open_func, mock_argparse):
        """Testea el manejo de un archivo no encontrado."""
        mock_args = argparse.Namespace(
            filepath="nonexistent.txt", host="localhost", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        self.assertIn("No se encontró el archivo", mock_stdout.getvalue())

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="")
    def test_main_empty_file(self, mock_open_func, mock_argparse):
        """Testea el manejo de un archivo vacío."""
        mock_args = argparse.Namespace(
            filepath="empty.txt", host="localhost", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        self.assertIn("El archivo 'empty.txt' está vacío", mock_stdout.getvalue())

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="test data")
    @patch("src.client.client.socket.socket")
    def test_main_socket_error(self, mock_socket, mock_open_func, mock_argparse):
        """Testea el manejo de un error de conexión de socket."""
        mock_args = argparse.Namespace(
            filepath="chat.txt", host="localhost", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_socket.return_value.__enter__.side_effect = socket.error(
            "Connection refused"
        )

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error de Socket", mock_stdout.getvalue())

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="test data")
    @patch("src.client.client.socket.socket")
    def test_main_unexpected_error(self, mock_socket, mock_open_func, mock_argparse):
        """Testea el manejo de un error inesperado."""
        mock_args = argparse.Namespace(
            filepath="chat.txt", host="localhost", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_socket.return_value.__enter__.side_effect = Exception("Unexpected error")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                main()

        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Ocurrió un error inesperado", mock_stdout.getvalue())

    @patch("src.client.client.argparse.ArgumentParser")
    @patch("src.client.client.open", new_callable=mock_open, read_data="test data")
    @patch("src.client.client.socket.socket")
    def test_main_invalid_json_response(
        self, mock_socket, mock_open_func, mock_argparse
    ):
        """Testea el manejo de una respuesta JSON inválida del servidor."""
        mock_args = argparse.Namespace(
            filepath="chat.txt", host="localhost", port=DEFAULT_PORT
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_socket_instance = MagicMock()
        mock_socket_instance.recv.side_effect = [b"this is not json", b""]
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            main()

        self.assertIn("Respuesta Inválida (No es JSON)", mock_stdout.getvalue())

import unittest
from unittest.mock import patch, MagicMock
from main_app11 import login_button_event
from Verification.account_ver11 import verify_credentials

import customtkinter

class TestLoginButtonEvent(unittest.TestCase):

    def setUp(self):
        # Create a mock for the app window and labels
        self.app11 = MagicMock()
        self.entry_login = MagicMock()
        self.entry_pass = MagicMock()
        self.login_error_label = MagicMock()


    @patch('main_app11.verify_credentials')
    def testEmptyLoginPassBadType(self, mock_verify):
        # Стовпчик 1: Логін, пароль не введені
        self.entry_login.get.return_value = ""
        self.entry_pass.get.return_value = ""
        mock_verify.return_value = None
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        self.login_error_label.configure.assert_called_with(text="Fill login.")
        self.entry_login.focus.assert_called_once()

    @patch('main_app11.verify_credentials')
    def testEmptyPassBadType(self, mock_verify):
        # Стовпчик 2: Логін введений, пароль не введений
        self.entry_login.get.return_value = "user"
        self.entry_pass.get.return_value = ""
        mock_verify.return_value = None
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        self.login_error_label.configure.assert_called_with(text="Fill password.")
        self.entry_pass.focus.assert_called_once()


    @patch('main_app11.verify_credentials')
    def testEmptyLogin(self, mock_verify):
        # Стовпчик 3: Логін не був введеним, пароль введений, тип правильний
        self.entry_login.get.return_value = ""
        self.entry_pass.get.return_value = "user"
        mock_verify.return_value = None
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        self.login_error_label.configure.assert_called_with(text="Fill login.")
        self.entry_login.focus.assert_called_once()

    @patch('main_app11.verify_credentials')
    @patch('main_app11.CTkMessagebox')
    def test_invalid_login_password(self, CTkMessagebox, mock_verify):
        # Стовпчик 4: Логін та пароль введені, але не правильні
        self.entry_login.get.return_value = "wrong_login"
        self.entry_pass.get.return_value = "wrong_password"
        mock_verify.return_value = None
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        CTkMessagebox.assert_called_once()
        args, kwargs = CTkMessagebox.call_args
        self.assertEqual(kwargs['message'], 'Invalid login or password.\n Maybe Try creating a new account!')
        mock_verify.assert_called_once_with("wrong_login", "wrong_password")
        self.login_error_label.configure.assert_not_called()


    @patch('main_app11.verify_credentials')
    @patch('main_app11.CTkMessagebox')
    def test_correct_login_wrong_password(self, CTkMessagebox, mock_verify):
        # Стовпчик 5: Логін правильний, пароль неправильний
        self.entry_login.get.return_value = "user"
        self.entry_pass.get.return_value = "wrong_password"
        mock_verify.return_value = None
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        CTkMessagebox.assert_called_once()
        args, kwargs = CTkMessagebox.call_args
        self.assertEqual(kwargs['message'], 'Invalid login or password.\n Maybe Try creating a new account!')
        mock_verify.assert_called_once_with("user", "wrong_password")
        self.login_error_label.configure.assert_not_called()


    @patch('main_app11.verify_credentials')
    @patch('main_app11.CTkMessagebox')
    def test_wrong_login_correct_password(self, CTkMessagebox, mock_verify):
        # Стовпчик 6: Логін неправильний, пароль правильний
        self.entry_login.get.return_value = "wrong_login"
        self.entry_pass.get.return_value = "user"
        mock_verify.return_value = None
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        CTkMessagebox.assert_called_once()
        args, kwargs = CTkMessagebox.call_args
        self.assertEqual(kwargs['message'], 'Invalid login or password.\n Maybe Try creating a new account!')
        mock_verify.assert_called_once_with("wrong_login", "user")
        self.login_error_label.configure.assert_not_called()


    @patch('main_app11.verify_credentials')
    @patch('main_app11.open_user_window1')
    def test_correct_login_password_user(self, mock_open_user_window, mock_verify):
        # Стовпчик 7: Логін правильний, пароль правильний, користувач
        self.entry_login.get.return_value = "user"
        self.entry_pass.get.return_value = "user"
        mock_verify.return_value = ['user']
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        mock_verify.assert_called_once_with("user", "user")
        mock_open_user_window.assert_called_once_with("user", self.app11)

    @patch('main_app11.verify_credentials')
    @patch('main_app11.open_admin_window1')
    def test_correct_login_password_admin(self, mock_open_admin_window, mock_verify):
        # Стовпчик 8: Логін правильний, пароль правильний, адмін
        self.entry_login.get.return_value = "admin"
        self.entry_pass.get.return_value = "admin"
        mock_verify.return_value = ['admin']  # Return admin account type
        login_button_event(self.entry_login, self.entry_pass, self.app11, self.login_error_label)
        mock_verify.assert_called_once_with("admin", "admin")
        mock_open_admin_window.assert_called_once_with("admin", self.app11)


if __name__ == '__main__':
    unittest.main()

import mock
from src import MemberService


class TestGpmService:

    @mock.patch('Main.create_connection')
    def test_update_project_member_attendance(self, mock_conn):
        mock_conn.cursor().execute.return_value = True
        mock_conn.commit.return_value = True
        project_member_id = 1

        result = MemberService.update_project_member_attendance(mock_conn, project_member_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_update_project_member_wage(self, mock_conn):
        project_member_id = 1
        mock_conn.cursor().execute.return_value = True
        mock_conn.commit.return_value = True

        result = MemberService.update_project_member_wage(mock_conn, project_member_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_show_member_details(self, mock_conn):
        dummy_object = ['MemberName', 'email@gmail.com', 22, 'male', 'place', 'address', 1000]
        member_id = 1
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = MemberService.show_member_details(mock_conn, member_id)

        assert result == dummy_object

    @mock.patch('Main.create_connection')
    def test_file_complaint(self, mock_conn):
        mock_conn.cursor().execute.return_value = True
        bdo_id = 1
        gpm_id = 1
        member_id = 1
        issue = 'test issue'
        result = MemberService.file_complaint(mock_conn, bdo_id, gpm_id, member_id, issue)

        assert result == True

    @mock.patch('src.MemberService.getpass')
    @mock.patch('Main.create_connection')
    def test_login_password_match(self, mock_conn, getpass):
        getpass.return_value = 'pass'
        email = "email@gmail.com"
        dummy_object = ['email@gmail.com', 'pass', 1, 1, 1]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = MemberService.member_login(mock_conn, email)

        assert result == [dummy_object[2], dummy_object[3], dummy_object[4]]

    @mock.patch('src.MemberService.getpass')
    @mock.patch('Main.create_connection')
    def test_login_password_mismatch(self, mock_conn, getpass):
        getpass.return_value = 'pass'
        email = "email@gmail.com"
        dummy_object = ['email@gmail.com', 'p', 1, 1, 1]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = MemberService.member_login(mock_conn, email)

        assert result == False

    @mock.patch('Main.create_connection')
    def test_login_invalid_user(self, mock_conn):
        email = "email@gmail.com"
        dummy_object = []
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = MemberService.member_login(mock_conn, email)

        assert result == False

    @mock.patch('src.MemberService.getpass')
    @mock.patch('Main.create_connection')
    def test_first_time_login(self, mock_conn, getpass):
        getpass.return_value = 'pass'
        email = "email@gmail.com"
        dummy_object = ['email@gmail.com', None, 1, 1, 1]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = MemberService.member_login(mock_conn, email)

        assert result == [dummy_object[2], dummy_object[3], dummy_object[4]]



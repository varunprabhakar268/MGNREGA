import mock
from src import GpmService


class TestGpmService:

    @mock.patch('Main.create_connection')
    @mock.patch('model.Member', return_value=[1, 1, 'MemberName', 'member@gmail.com', 22, 'Male', 'Place', 'Address', '2020-01-21 16:20:05.112581'])
    def test_create_member_success(self, member, mock_conn):
        mock_conn.cursor().execute.return_value = True

        result = GpmService.create_member(mock_conn, member)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_get_member_by_id_success(self, mock_conn):
        member_id = 1
        dummy_object = ['MemberName', 'member@gmail.com', 22, 'Male', 'Place', 'Address']
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.get_member_by_id(mock_conn, member_id)

        assert result == dummy_object

    @mock.patch('Main.create_connection')
    def test_update_member_success(self, mock_conn):
        name = 'MemberName'
        email = 'member@gmail.com'
        age = 22
        gender = 'Male'
        place = 'Place'
        address = 'Address'
        member_id = 1
        mock_conn.cursor().execute.return_value = True
        mock_conn.commit.return_value = True

        result = GpmService.update_member(mock_conn, name,email, age, gender, place, address, member_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_delete_member_success(self, mock_conn):
        member_id = 1
        mock_conn.cursor().execute.return_value = True
        mock_conn.commit.return_value = True

        result = GpmService.delete_member(mock_conn, member_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_show_member_details_success(self, mock_conn):
        gpm_id = 1
        dummy_object = [[1, 'TestName', 22, 'Male', 'Place', 'Address']]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchall.return_value = dummy_object

        result = GpmService.show_member_details(mock_conn, gpm_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_show_member_details_failure(self, mock_conn):
        gpm_id = 1
        dummy_object = []
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchall.return_value = dummy_object

        result = GpmService.show_member_details(mock_conn, gpm_id)

        assert result == False

    @mock.patch('Main.create_connection')
    @mock.patch('model.ProjectMember', return_value=[1, 1, 1, 1, 'TestArea', 123123, 10, 100, 60, 1, '2020-01-21 16:20:05.112581', 1])
    def test_assign_project_member_success(self, project_member, mock_conn):
        mock_conn.cursor().execute.return_value = True

        result = GpmService.assign_project_member(mock_conn, project_member)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_update_project_member_success(self, mock_conn):
        area = 'TestArea'
        pincode = 123123
        project_member_id = 1
        mock_conn.cursor().execute.return_value = True
        mock_conn.commit.return_value = True

        result = GpmService.update_project_member(mock_conn, area, pincode, project_member_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_delete_project_member_success(self, mock_conn):
        project_id = 1
        member_id = 1
        mock_conn.cursor().execute.return_value = True
        mock_conn.commit.return_value = True

        result = GpmService.delete_project_member(mock_conn, project_id, member_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_show_project_member_details_success(self, mock_conn):
        gpm_id = 1
        dummy_object = [[1, 'ProjectName', 22, 'MemberName', 'Area', 123123, 22, 10, 100, 56.0 ]]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchall.return_value = dummy_object

        result = GpmService.show_project_member_details(mock_conn, gpm_id)

        assert result == True

    @mock.patch('Main.create_connection')
    def test_show_project_member_details_failure(self, mock_conn):
        gpm_id = 1
        dummy_object = []
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchall.return_value = dummy_object

        result = GpmService.show_project_member_details(mock_conn, gpm_id)

        assert result == False

    @mock.patch('Main.create_connection')
    def test_fetch_project_members_success(self, mock_conn):
        project_id = 1
        dummy_object = [[1, 'MemberName', 'Area', 122122, 22]]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchall.return_value = dummy_object

        result = GpmService.fetch_project_members(mock_conn, project_id)

        assert result == dummy_object

    @mock.patch('Main.create_connection')
    def test_fetch_project_member_success(self, mock_conn):
        project_id = 1
        member_id = 1
        dummy_object = [1, 'Area', 122122]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.fetch_project_member(mock_conn, project_id, member_id)

        assert result == dummy_object

    @mock.patch('Main.create_connection')
    def test_issue_job_card_success(self, mock_conn):
        member_id = 1
        dummy_object = ['MemberName', 'Area', 122122, 22]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.issue_job_card(mock_conn, member_id)

        assert result == dummy_object

    @mock.patch('Main.create_connection')
    def test_view_complaints_success(self, mock_conn):
        gpm_id = 1
        dummy_object = [[1, 'Issue']]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchall.return_value = dummy_object

        result = GpmService.view_complaints(mock_conn, gpm_id)

        assert result == dummy_object

    @mock.patch('src.GpmService.getpass')
    @mock.patch('Main.create_connection')
    def test_login_password_match(self, mock_conn, getpass):
        getpass.return_value = 'pass'
        email = "email@gmail.com"
        dummy_object = ['email@gmail.com', 'pass', 1, 1]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.gpm_login(mock_conn, email)

        assert result == [dummy_object[2], dummy_object[3]]

    @mock.patch('src.GpmService.getpass')
    @mock.patch('Main.create_connection')
    def test_login_password_mismatch(self, mock_conn, getpass):
        getpass.return_value = 'pass'
        email = "email@gmail.com"
        dummy_object = ['email@gmail.com', 'p', 1, 1]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.gpm_login(mock_conn, email)

        assert result == False

    @mock.patch('Main.create_connection')
    def test_login_invalid_user(self, mock_conn):
        email = "email@gmail.com"
        dummy_object = []
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.gpm_login(mock_conn, email)

        assert result == False

    @mock.patch('src.GpmService.getpass')
    @mock.patch('Main.create_connection')
    def test_first_time_login(self, mock_conn, getpass):
        getpass.return_value = 'pass'
        email = "email@gmail.com"
        dummy_object = ['email@gmail.com', None, 1, 1]
        mock_conn.cursor().execute.return_value = True
        mock_conn.cursor().fetchone.return_value = dummy_object

        result = GpmService.gpm_login(mock_conn, email)

        assert result == [dummy_object[2], dummy_object[3]]




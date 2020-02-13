# import allow as allow
from doubles import allow
import mock

from src import BdoService
from src.BdoService import Bdo


class TestBdoService:

    @mock.patch('src.BdoService.getpass')
    @mock.patch('src.BdoRepository.BdoQuery.login')
    @mock.patch('src.BdoService.input')
    def test_login_password_match(self, inputs, query, getpass):
        inputs.return_value = "email@gmail.com"
        getpass.return_value = 'pass'
        test_class = BdoService.Bdo()
        query.return_value = ['email@gmail.com', 'pass', 1]

        result = test_class.bdo_login()

        assert result is True

    @mock.patch('src.BdoService.getpass')
    @mock.patch('src.BdoRepository.BdoQuery.login')
    @mock.patch('src.BdoService.input')
    def test_login_password_mismatch(self, inputs, query, getpass):
        inputs.return_value = "email@gmail.com"
        getpass.return_value = 'p'
        test_class = BdoService.Bdo()
        query.return_value = ['email@gmail.com', 'pass', 1]

        result = test_class.bdo_login()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.login')
    @mock.patch('src.BdoService.input')
    def test_login_invalid_user(self, inputs, query):
        inputs.return_value = "email@gmail.com"
        test_class = BdoService.Bdo()
        query.return_value = []

        result = test_class.bdo_login()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.create_gpm')
    @mock.patch('src.BdoService.input')
    @mock.patch('src.model.GpmModel')
    def test_create_gpm_success(self, gpm, inputs, query):
        inputs.side_effect = ['GpmName', 'gpm@gmail.com', 'GpmArea', 123456]
        test_class = BdoService.Bdo()
        gpm.return_value = [1, 'GpmName', 'GpmArea', 123456, 'gpm@gmail.com', '2020-01-21 16:20:05.112581']
        query.return_value = True

        result = test_class.create_gpm()

        assert result is True

    @mock.patch('src.BdoService.input')
    def test_create_gpm_invalid_name(self, inputs):
        inputs.side_effect = [12]
        test_class = BdoService.Bdo()

        result = test_class.create_gpm()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_create_gpm_invalid_email(self, inputs):
        inputs.side_effect = [12, 'gpm.com', 'GpmArea', 'string']
        test_class = BdoService.Bdo()

        result = test_class.create_gpm()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_create_gpm_invalid_area(self, inputs):
        inputs.side_effect = [12, 'gpm.com', '@', 'string']
        test_class = BdoService.Bdo()

        result = test_class.create_gpm()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_create_gpm_invalid_pincode(self, inputs):
        inputs.side_effect = ['GpmName', 'gpm@gmail.com', 'GpmArea', 'string']
        test_class = BdoService.Bdo()

        result = test_class.create_gpm()

        assert result is False

    def test_create_gpm_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.create_gpm()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_gpm_by_id')
    def test_get_gpm_by_id_success(self, query):
        gpm_id = 1
        test_class = BdoService.Bdo()
        query.return_value = ['TestName', 'email@gmail.com', 'TestArea', 123123]

        result = test_class.get_gpm_by_id(gpm_id)

        assert result == ['TestName', 'email@gmail.com', 'TestArea', 123123]

    @mock.patch('src.BdoRepository.BdoQuery.get_gpm_by_id')
    def test_get_gpm_by_id_failure(self, query):
        gpm_id = 1
        test_class = BdoService.Bdo()
        query.return_value = []

        result = test_class.get_gpm_by_id(gpm_id)

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_gpm_by_id')
    @mock.patch('src.BdoRepository.BdoQuery.update_gpm')
    @mock.patch('src.BdoService.input')
    def test_update_gpm_success(self, inputs, query_update, query_get):
        inputs.side_effect = [1, 'GpmName', 'gpm@gmail.com', 'GpmArea', 123456]
        test_class = Bdo()
        query_get.return_value(['GpmName', 'gpm@gmail.com', 'GpmArea', 123456])
        query_update.return_value = True

        result = test_class.update_gpm()

        assert result is True

    @mock.patch('src.BdoService.input')
    def test_update_gpm_invalid_input(self, inputs):
        inputs.side_effect = ['a', 'GpmName', 'gpm@gmail.com', 'GpmArea', 'a']
        test_class = BdoService.Bdo()

        result = test_class.update_gpm()

        assert result is False

    def test_update_gpm_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.update_gpm()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_gpm_by_id')
    @mock.patch('src.BdoRepository.BdoQuery.delete_gpm')
    @mock.patch('src.BdoService.input')
    def test_delete_gpm_success(self, inputs, query_delete, query_get):
        inputs.side_effect = [1, 'y']
        test_class = Bdo()
        query_get.return_value(['GpmName', 'gpm@gmail.com', 'GpmArea', 123456])
        query_delete.return_value = True

        result = test_class.delete_gpm()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.get_gpm_by_id')
    @mock.patch('src.BdoRepository.BdoQuery.delete_gpm')
    @mock.patch('src.BdoService.input')
    def test_delete_gpm_failure(self, inputs, query_delete, query_get):
        inputs.side_effect = [1, 'n']
        test_class = Bdo()
        query_get.return_value(['GpmName', 'gpm@gmail.com', 'GpmArea', 123456])
        query_delete.return_value = True

        result = test_class.delete_gpm()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_delete_gpm_invalid_input(self, inputs, ):
        inputs.side_effect = ['n', 'n']
        test_class = Bdo()

        result = test_class.delete_gpm()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_gpm_details')
    def test_show_gpm_details_success(self, query):
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'TestName', 'email@gmail.com', 'TestArea', 123123,'2020-01-21'],[2,'TestName2', 'email2@gmail.com', 'TestArea2', 123456,'2020-01-21 ']]

        query.return_value = dummy_object
        result = test_class.show_gpm_details()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.show_gpm_details')
    def test_show_gpm_details_failure(self, query):
        test_class = BdoService.Bdo()

        query.return_value = []
        result = test_class.show_gpm_details()

        assert result is False

    def test_show_gpm_details_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.show_gpm_details()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.create_project')
    @mock.patch('src.BdoService.input')
    @mock.patch('src.model.ProjectModel')
    def test_create_project_success(self, project, inputs, query):
        inputs.side_effect = ['1', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        test_class = BdoService.Bdo()
        project.return_value = [1, 'Road Construction', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        query.return_value = True

        result = test_class.create_project()

        assert result is True

    @mock.patch('src.BdoService.input')
    def test_create_project_invalid_project_type(self, inputs):
        inputs.side_effect = [8, 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        test_class = BdoService.Bdo()

        result = test_class.create_project()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_create_project_invalid_input(self, inputs):
        inputs.side_effect = ['2', 'ProjectName', 'ProjectArea', 'aa', 100, '2020-01-01', '2020-01-20']
        test_class = BdoService.Bdo()

        result = test_class.create_project()

        assert result is False

    def test_create_project_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.create_project()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_project_by_id')
    def test_get_project_by_id_success(self, query):
        project_id = 1
        test_class = BdoService.Bdo()
        dummy_object = ['Road Construction', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        query.return_value = dummy_object

        result = test_class.get_project_by_id(project_id)

        assert result == dummy_object

    @mock.patch('src.BdoRepository.BdoQuery.get_project_by_id')
    def test_get_project_by_id_failure(self, query):
        project_id = 1
        test_class = BdoService.Bdo()
        query.return_value = []

        result = test_class.get_project_by_id(project_id)

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_project_by_id')
    @mock.patch('src.BdoRepository.BdoQuery.update_project')
    @mock.patch('src.BdoService.input')
    def test_update_project_success(self, inputs, query_update, query_get):
        dummy_object = ['Road Construction', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        inputs.side_effect = [1, '1', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        test_class = Bdo()
        query_get.return_value = dummy_object
        query_update.return_value = True

        result = test_class.update_project()

        assert result is True

    @mock.patch('src.BdoService.input')
    def test_update_project_invalid_input(self, inputs):
        inputs.side_effect = ['invalid_input']

        test_class = BdoService.Bdo()

        result = test_class.update_project()

        assert result is False

    def test_update_project_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.update_project()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_project_by_id')
    @mock.patch('src.BdoService.input')
    def test_update_project_does_not_exist(self, inputs, query_get):
        project_id = 1
        query_get(project_id).return_value = []
        inputs.side_effect = [1]
        test_class = Bdo()

        result = test_class.update_project()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_update_project_invalid_project_type(self, inputs):
        inputs.side_effect = [1, '8', 'GpmName', 'gpm@gmail.com', 'GpmArea', 123456]

        test_class = BdoService.Bdo()

        result = test_class.update_project()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.get_project_by_id')
    @mock.patch('src.BdoRepository.BdoQuery.delete_project')
    @mock.patch('src.BdoService.input')
    def test_delete_project_success(self, inputs, query_delete, query_get):
        inputs.side_effect = [1, 'y']
        dummy_object = ['Road Construction', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        test_class = Bdo()
        query_get.return_value = dummy_object
        query_delete.return_value = True

        result = test_class.delete_project()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.get_project_by_id')
    @mock.patch('src.BdoService.input')
    def test_delete_project_failure(self, inputs, query_get):
        inputs.side_effect = [1, 'n']
        dummy_object = ['Road Construction', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']
        test_class = Bdo()
        query_get.return_value = dummy_object

        result = test_class.delete_project()

        assert result is False

    @mock.patch('src.BdoService.input')
    def test_delete_project_invalid_input(self, inputs, ):
        inputs.side_effect = ['n', 'n']
        test_class = Bdo()

        result = test_class.delete_project()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_project_details')
    def test_show_project_details_success(self, query):
        test_class = BdoService.Bdo()
        dummy_object = [[1,'Road Construction', 'ProjectName', 'ProjectArea', 10, 100, '2020-01-01', '2020-01-20']]
        query.return_value = dummy_object
        result = test_class.show_project_details()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.show_project_details')
    def test_show_project_details_failure(self, query):
        test_class = BdoService.Bdo()

        query.return_value = []
        result = test_class.show_project_details()

        assert result is False

    def test_show_project_details_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.show_project_details()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_requests')
    def test_show_project_approval_requests_success(self, query):
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 1]]
        query.return_value = dummy_object
        result = test_class.show_project_approval_requests()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_requests')
    def test_show_project_approval_requests_failure(self, query):
        test_class = BdoService.Bdo()
        dummy_object = []
        query.return_value = dummy_object
        result = test_class.show_project_approval_requests()

        assert result is False

    def test_show_project_approval_requests_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.show_project_approval_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_project_approval_pending_requests(self, inputs, query_get):
        inputs.side_effect = ['n']
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 0]]
        query_get.return_value = dummy_object

        result = test_class.show_project_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_project_approval_pending_requests_invalid_wish(self, inputs, query_get):
        inputs.side_effect = ['z']
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 0]]
        query_get.return_value = dummy_object

        result = test_class.show_project_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.update_project_member_wage')
    @mock.patch('src.BdoRepository.BdoQuery.update_project_member_attendance')
    @mock.patch('src.BdoRepository.BdoQuery.approve_project_assignment')
    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_project_approval_pending_requests_and_approve(self, inputs, query_get, query_approve, query_attendance, query_wage):
        inputs.side_effect = ['y', 1, 1]
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 0]]
        query_get.return_value = dummy_object
        query_approve.return_value = True
        query_attendance.return_value = True
        query_wage.return_value = True

        result = test_class.show_project_approval_pending_requests()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.approve_project_assignment')
    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_project_approval_pending_requests_and_reject(self, inputs, query_get, query_approve):
        inputs.side_effect = ['y', 1, 2]
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 0]]
        query_get.return_value = dummy_object
        query_approve.return_value = True

        result = test_class.show_project_approval_pending_requests()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.approve_project_assignment')
    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_project_approval_pending_requests_invalid_choice(self, inputs, query_get, query_approve):
        inputs.side_effect = ['y', 1, 6]
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 0]]
        query_get.return_value = dummy_object
        query_approve.return_value = True

        result = test_class.show_project_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_project_approval_pending_requests')
    def test_show_project_approval_pending_requests_failure(self, query):
        test_class = BdoService.Bdo()
        dummy_object = []
        query.return_value = dummy_object
        result = test_class.show_project_approval_pending_requests()

        assert result is False

    def test_show_project_approval_pending_requests_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.show_project_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_requests')
    def test_show_wage_approval_requests_success(self, query):
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 10, 100, 69.0, 1]]
        query.return_value = dummy_object
        result = test_class.show_wage_approval_requests()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_requests')
    def test_show_wage_approval_requests_failure(self, query):
        test_class = BdoService.Bdo()
        dummy_object = []
        query.return_value = dummy_object
        result = test_class.show_wage_approval_requests()

        assert result is False

    def test_show_wage_approval_requests_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.show_wage_approval_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_wage_approval_pending_requests(self, inputs, query_get):
        inputs.side_effect = ['n']
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 10, 100, 69.0, 0]]
        query_get.return_value = dummy_object

        result = test_class.show_wage_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_wage_approval_pending_requests_invalid_wish(self, inputs, query_get):
        inputs.side_effect = ['z']
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 10, 100, 69.0, 0]]
        query_get.return_value = dummy_object

        result = test_class.show_wage_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.approve_wage')
    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_wage_approval_pending_requests_and_approve(self, inputs, query_get, query_approve):
        inputs.side_effect = ['y', 1, 1]
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 10, 100, 69.0, 0]]
        query_get.return_value = dummy_object
        query_approve.return_value = True

        result = test_class.show_wage_approval_pending_requests()

        assert result is True

    @mock.patch('src.BdoRepository.BdoQuery.approve_wage')
    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_pending_requests')
    @mock.patch('src.BdoService.input')
    def test_show_wage_approval_pending_requests_invalid_choice(self, inputs, query_get, query_approve):
        inputs.side_effect = ['y', 1, 6]
        test_class = BdoService.Bdo()
        dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 0]]
        query_get.return_value = dummy_object
        query_approve.return_value = True

        result = test_class.show_wage_approval_pending_requests()

        assert result is False

    @mock.patch('src.BdoRepository.BdoQuery.show_wage_approval_pending_requests')
    def test_show_wage_approval_pending_requests_failure(self, query):
        test_class = BdoService.Bdo()
        dummy_object = []
        query.return_value = dummy_object
        result = test_class.show_wage_approval_pending_requests()

        assert result is False

    def test_show_wage_approval_pending_requests_unknown_error(self):
        test_class = BdoService.Bdo()

        result = test_class.show_wage_approval_pending_requests()

        assert result is False



    # @mock.patch('Main.create_connection')
    # def test_wage_approval_requests(self, mock_conn):
    #     bdo_id = 1
    #     dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 10, 100, 69.0, 1]]
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.cursor().fetchall.return_value = dummy_object
    #
    #     result = BdoService.show_wage_approval_requests(mock_conn, bdo_id)
    #
    #     assert result == dummy_object
    #
    # @mock.patch('Main.create_connection')
    # def test_wage_approval_pending_requests(self, mock_conn):
    #     bdo_id = 1
    #     dummy_object = [[1, 'GpmName', 'ProjectName', 'MemberName', 10, 100, 69.0, 0]]
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.cursor().fetchall.return_value = dummy_object
    #
    #     result = BdoService.show_wage_approval_pending_requests(mock_conn, bdo_id)
    #
    #     assert result == dummy_object
    #
    # @mock.patch('Main.create_connection')
    # def test_approve_wage(self, mock_conn):
    #     status = 1
    #     project_member_id = 1
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.commit.return_value = True
    #
    #     result = BdoService.approve_wage(mock_conn, status, project_member_id)
    #
    #     assert result == True
    #
    # @mock.patch('Main.create_connection')
    # def test_view_complaints_success(self, mock_conn):
    #     bdo_id = 1
    #     dummy_object = [[1, 1, 'Issue']]
    #     mock_conn.cursor().execute.return_value = True
    #     mock_conn.cursor().fetchall.return_value = dummy_object
    #
    #     result = BdoService.view_complaints(mock_conn, bdo_id)
    #
    #     assert result == dummy_object
    #


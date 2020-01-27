import mock
from src import BdoService


class TestBdoService:

    @mock.patch('Main.create_connection')
    # @mock.patch('BdoService.bdo_login', return_value=1)
    @mock.patch('model.Gpm', return_value=[1, 'GpmName', 'GpmArea', 123456, 'gpm@gmail.com', '2020-01-21 16:20:05.112581'])
    def test_create_gpm_success(self, mock_connect, gpm):
        db_mock = mock.Mock()
        mock_conn = mock_connect.return_value
        mock_cur = mock_conn.cursor.return_value
        mock_cur.execute.return_value = True
        mock_cur.fetchone.return_value = 2

        result = BdoService.create_gpm(mock_conn, gpm)

        self.assertEqual(result, 2)

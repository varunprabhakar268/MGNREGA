from src import Main


class MemberQuery:
    def __init__(self):
        self.conn = Main.create_connection()

    def login(self, email):
        sql = "SELECT Email,Password,BdoId,GpmId,MemberId FROM Members WHERE Email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_password(self,password, member_id):
        sql = "Update Members SET Password = '{}' WHERE MemberId = {}".format(password,
                                                                                 member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True

    def show_member_details(self, member_id):
        sql = '''With MemberWage(Wage) as (select Sum(Wage)as TotalWage from ProjectMembers
                                     Where MemberId = {} and WageApproval = 1)
                                     select MemberName, Email, Age, Gender, Place, Address,Wage from Members,MemberWage
                                     Where MemberId = {}'''.format(member_id, member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def file_complaint(self, bdo_id, gpm_id, member_id, issue):
        sql = '''Insert into ComplaintLogs(BdoId,GpmId,MemberId,Issue)
                                     Values({},{},{},'{}')'''.format(bdo_id, gpm_id, member_id, issue)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True
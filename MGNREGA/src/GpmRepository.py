from src import Main


class GpmQuery:
    def __init__(self):
        self.conn = Main.create_connection()

    def login(self, email):
        sql = "SELECT Email,Password,GpmId,BdoId FROM Gpms WHERE Email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_password(self, password,gpm_id):
        sql = "Update Gpms SET Password = '{}' WHERE GpmId = {}".format(password, gpm_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True

    def create_member(self, member):
        sql = '''
                                    INSERT INTO Members (BdoId, GpmId, MemberName,Email, Age, Gender, Place, Address,RegisteredAt)
                                    VALUES({}, {}, '{}', '{}', {}, '{}', '{}', '{}','{}')
                                  '''.format(member.bdo_id, member.gpm_id, member.name, member.email, member.age,
                                             member.gender,
                                             member.place, member.address, member.RegisteredAt)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True

    def get_member_by_id(self, member_id):
        sql = '''SELECT MemberName,Email,Age,Gender,Place,Address
                         FROM Members WHERE MemberId = {}'''.format(member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_member(self, name, age, gender, email, place, address, member_id):
        sql = ''' UPDATE Members
                                              SET MemberName = '{}',
                                                  Email = '{}',
                                                  Age = {},
                                                  Gender = '{}',
                                                  Place = '{}',
                                                  Address = '{}'                      
                                              WHERE MemberId = {}'''.format(name, email, age, gender, place, address,
                                                                            member_id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def delete_member(self, member_id):
        sql = "DELETE FROM Members WHERE MemberId={}".format(member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def show_member_details(self, gpm_id):
        sql = '''SELECT MemberId,MemberName,Age,Gender,Place,Address
                             FROM Members WHERE GpmId = {}'''.format(gpm_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_project_details(self, bdo_id):
        sql = '''SELECT ProjectId, Type, Name, Area, TotalMembers ,CostEstimate, date(StartDate), date(EndDate)
                             FROM Projects WHERE BdoId = {}'''.format(bdo_id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def assign_project_member(self, projectmember):
        sql = '''INSERT INTO ProjectMembers(BdoId,GpmId,ProjectId,MemberId,Area,Pincode,TotalWorkingDays,Wage,Attendance,Approval,CreatedAt,WageApproval)
                                     Values({},{},{},{},'{}',{},{},{},{},{},'{}',{})
                                  '''.format(projectmember.bdo_id, projectmember.gpm_id, projectmember.project_id,
                                             projectmember.member_id,
                                             projectmember.area, projectmember.pincode,
                                             projectmember.total_working_days,
                                             projectmember.wage, projectmember.attendance,
                                             projectmember.project_approval,
                                             projectmember.RegisteredAt, projectmember.wage_approval)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True

    def delete_project_member(self, project_id, member_id):
        sql = '''DELETE FROM ProjectMembers WHERE ProjectId = {} and MemberId = {}
                                      '''.format(project_id, member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def update_project_member(self, area, pincode, project_member_id):
        sql = ''' UPDATE ProjectMembers
                                          SET Area = '{}',
                                              Pincode = {}                
                                          WHERE ProjectMemberId = {}
                                      '''.format(area, pincode, project_member_id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def show_project_member_details(self, gpm_id):
        sql = '''SELECT ProjectMembers.ProjectId ,Projects.Name,ProjectMembers.MemberId,Members.MemberName,
                         ProjectMembers.Area,ProjectMembers.Pincode,Members.Age,ProjectMembers.TotalWorkingDays,
                         ProjectMembers.Wage,ProjectMembers.Attendance 
                         FROM ProjectMembers inner join Projects on ProjectMembers.ProjectId = Projects.ProjectId
                         inner join Members on ProjectMembers.MemberId = Members.MemberId
                         WHERE ProjectMembers.GpmId = {}
                         order by ProjectMembers.ProjectId
                      '''.format(gpm_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def fetch_project_members(self, project_id):
        sql = '''SELECT ProjectMembers.MemberId, Members.MemberName,ProjectMembers.Area,ProjectMembers.Pincode,Members.Age 
                        FROM ProjectMembers inner join Members on ProjectMembers.MemberId = Members.MemberId
                        WHERE ProjectId = {} '''.format(project_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def fetch_project_member(self, project_id, member_id):
        """
        Fetch details of a particular member in a particular project.
        :param conn:
        :param project_id:
        :param member_id:
        :return:
        """
        sql = '''SELECT ProjectMemberId,Area,Pincode from ProjectMembers
                 WHERE ProjectId = {} and MemberId = {}
              '''.format(project_id, member_id)
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def issue_job_card(self, member_id):
        sql = '''Select MemberName, Age, Gender, Place, Address 
                                     From Members Where MemberId = {}
                                  '''.format(member_id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def view_complaints(self, gpm_id):
        sql = '''Select MemberId,Issue 
                                     From ComplaintLogs Where GpmId = {}
                                  '''.format(gpm_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

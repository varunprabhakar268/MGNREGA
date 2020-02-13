from src import Main


class BdoQuery:
    def __init__(self):
        self.conn = Main.create_connection()

    def login(self, email):
        sql = "SELECT Email,Password,BdoId FROM Bdos WHERE Email = '{}'".format(email)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def create_gpm(self, gpm):
        sql = '''
                 INSERT INTO Gpms(BdoId, Name, Area, Pincode, Email, RegisteredAt )
                 VALUES({}, '{}', '{}', {}, '{}', '{}')
              '''.format(gpm.BdoId, gpm.name, gpm.area, gpm.pincode, gpm.email, gpm.RegisteredAt)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True

    def get_gpm_by_id(self, gpm_id):
        sql = "SELECT Name,Email,Area,Pincode FROM Gpms WHERE GpmId = {}".format(gpm_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchone()

    def update_gpm(self, name, area, pincode, email, gpm_id):
        sql = ''' UPDATE Gpms
                  SET Name = '{}' ,
                      Area = '{}' ,
                      Pincode = {},
                      Email = '{}'                      
                  WHERE GpmId = {}'''.format(name, area, pincode, email, gpm_id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def delete_gpm(self, gpm_id):
        sql = "DELETE FROM Gpms WHERE GpmId={}".format(gpm_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def show_gpm_details(self, bdo_id):
        sql = "SELECT GpmId,Name,Email,Area,Pincode,date(RegisteredAt) FROM Gpms WHERE BdoId = {}".format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def create_project(self, project):
        sql = '''INSERT INTO Projects (BdoId, Type, Name, Area, TotalMembers, CostEstimate, StartDate, EndDate )
                                     VALUES({}, '{}', '{}', '{}', {}, {}, '{}', '{}')
                                  '''.format(project.bdoId, project.type, project.name, project.area,
                                             project.total_members,
                                             project.cost_estimate, project.start_date, project.end_date)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return True

    def get_project_by_id(self, project_id):
        """
        get details of a particular project.
        :param conn:
        :param project_id:
        :return: details of project matching the projectId
        """
        sql = '''SELECT Type,Name,Area,TotalMembers,CostEstimate,StartDate,EndDate 
                 FROM Projects WHERE ProjectId = {}'''.format(project_id)
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def update_project(self, project_type, name, area, total_members, cost_estimate, start_date, end_date, project_id):
        sql = ''' UPDATE Projects
                  SET Type = '{}' ,
                      Name = '{}' ,
                      Area = '{}',
                      TotalMembers = {} ,
                      CostEstimate = {} ,
                      StartDate = '{}' ,
                      EndDate = '{}'                      
                  WHERE ProjectId = {}
              '''.format(project_type, name, area, total_members, cost_estimate, start_date, end_date, project_id)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return True

    def delete_project(self, project_id):
        sql = "DELETE FROM Projects WHERE ProjectId={}".format(project_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def show_project_details(self, bdo_id):
        sql = '''SELECT ProjectId, Type, Name, Area, TotalMembers ,CostEstimate, date(StartDate), date(EndDate)
                     FROM Projects WHERE BdoId = {}'''.format(bdo_id)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_project_approval_requests(self,bdo_id):
        sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
                                    Projects.Name as ProjectName, Members.MemberName,ProjectMembers.Approval
                                    from ProjectMembers inner join Projects on 
                                    ProjectMembers.ProjectId = Projects.ProjectId
                                    inner join Members on ProjectMembers.MemberId = Members.MemberId
                                    inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
                                    Where ProjectMembers.BdoId = {} and ProjectMembers.Approval = 1 or ProjectMembers.Approval = 2
             '''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_project_approval_pending_requests(self, bdo_id):
        sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
                                     Projects.Name as ProjectName, Members.MemberName,ProjectMembers.Approval
                                     from ProjectMembers inner join Projects on 
                                     ProjectMembers.ProjectId = Projects.ProjectId
                                     inner join Members on ProjectMembers.MemberId = Members.MemberId
                                     inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
                                     Where ProjectMembers.BdoId = {} and ProjectMembers.Approval = 0
             '''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def approve_project_assignment(self, status, project_member_id):
        sql = '''Update ProjectMembers Set Approval = {} Where ProjectMemberId = {} 
                          '''.format(status, project_member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def show_wage_approval_requests(self, bdo_id):
        sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
                 Projects.Name as ProjectName, Members.MemberName,
                 ProjectMembers.TotalWorkingDays, ProjectMembers.Wage,
                 ProjectMembers.Attendance, ProjectMembers.WageApproval
                 from ProjectMembers inner join Projects on 
                 ProjectMembers.ProjectId = Projects.ProjectId
                 inner join Members on ProjectMembers.MemberId = Members.MemberId
                 inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
                 Where ProjectMembers.BdoId = {} and ProjectMembers.Approval = 1 and  ProjectMembers.WageApproval = 1 or ProjectMembers.WageApproval = 2 
              '''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_wage_approval_pending_requests(self, bdo_id):
        sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
                     Projects.Name as ProjectName, Members.MemberName,
                     ProjectMembers.TotalWorkingDays, ProjectMembers.Wage,
                     ProjectMembers.Attendance, ProjectMembers.WageApproval
                     from ProjectMembers inner join Projects on 
                     ProjectMembers.ProjectId = Projects.ProjectId
                     inner join Members on ProjectMembers.MemberId = Members.MemberId
                     inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
                     Where ProjectMembers.BdoId = {} and ProjectMembers.Approval = 1 and ProjectMembers.WageApproval = 0
               '''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def approve_wage(self, status, project_member_id):
        sql = '''Update ProjectMembers Set WageApproval = {} Where ProjectMemberId = {} 
                          '''.format(status, project_member_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True

    def view_complaints(self, bdo_id):
        sql = '''Select MemberId,GpmId,Issue 
                             From ComplaintLogs Where BdoId = {}
                          '''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def update_project_member_attendance(self, project_member_id):
        sql = ''' With temp (EndDate,StartDate) as 
                  (select EndDate,StartDate From Projects where 
                  ProjectId = (Select ProjectId from ProjectMembers where ProjectMemberId = {}) ) 
                  ,ProjectTenure (TotalDays,WorkingDays) as 
                  (SELECT (julianday(EndDate) - julianday(StartDate)) as TotalDays,
                  (julianday(EndDate) - julianday(CreatedAt)) as WorkingDays 
                  from temp,ProjectMembers Where ProjectMemberId = {})
                  Update ProjectMembers set
                  TotalWorkingDays = (select TotalDays from ProjectTenure),
                  Attendance = (select (WorkingDays*100/TotalDays) from ProjectTenure)
                  Where ProjectMemberId = {}
              '''.format(project_member_id, project_member_id, project_member_id)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return True

    def update_project_member_wage(self, project_member_id):
        sql = '''Update ProjectMembers Set 
                 Wage = TotalWorkingDays * 100
                 where ProjectMemberId = {}
              '''.format(project_member_id)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return True

    def show_member_details(self, bdo_id):
        sql = '''SELECT MemberId,MemberName,Age,Gender,Place,Address
                             FROM Members WHERE BdoId = {}'''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def show_project_member_details(self, bdo_id):
        sql = '''SELECT ProjectMembers.ProjectId ,Projects.Name,ProjectMembers.MemberId,Members.MemberName,
                         ProjectMembers.Area,ProjectMembers.Pincode,Members.Age,ProjectMembers.TotalWorkingDays,
                         ProjectMembers.Wage,ProjectMembers.Attendance 
                         FROM ProjectMembers inner join Projects on ProjectMembers.ProjectId = Projects.ProjectId
                         inner join Members on ProjectMembers.MemberId = Members.MemberId
                         WHERE ProjectMembers.BdoId = {}
                         order by ProjectMembers.ProjectId
                      '''.format(bdo_id)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

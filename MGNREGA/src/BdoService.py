from getpass import getpass


def bdo_login(conn, email):
    """ Authenticate BDO.
    :param conn:
    :param email:
    :return: BdoId
    """
    sql = "SELECT Email,Password,BdoId FROM Bdos WHERE Email = '{}'".format(email)
    cur = conn.cursor()
    cur.execute(sql)
    record = cur.fetchone()
    if record:
        password = getpass('\tEnter Password: ')
        if record[1] == password:
            print("\tAuthentication Successful")
            return record[2]
        else:
            print("\tAuthentication failed. Please check your credentials")
    else:
        print("\tUser does not exist")


def create_gpm(conn, gpm):
    """
    Add GPM.
    :param conn:
    :param gpm:
    :return: GpmId
    """
    sql = '''
            INSERT INTO Gpms(BdoId, Name, Area, Pincode, Email, RegisteredAt )
            VALUES({}, '{}', '{}', {}, '{}', '{}')
            '''.format(gpm.BdoId, gpm.name, gpm.area, gpm.pincode, gpm.email, gpm.RegisteredAt)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid


def get_gpm_by_id(conn, gpm_id):
    """
    Get details of a particular Gpm.
    :param conn:
    :param gpm_id:
    :return: Gpm Details matching the Id
    """
    sql = "SELECT Name,Email,Area,Pincode FROM Gpms WHERE GpmId = {}".format(gpm_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()


def update_gpm(conn, name, area, pincode, email, gpm_id):
    """
    Update Gpm Details.
    :param conn:
    :param name:
    :param area:
    :param pincode:
    :param email:
    :param gpm_id:
    :return:
    """
    sql = ''' UPDATE Gpms
                  SET Name = '{}' ,
                      Area = '{}' ,
                      Pincode = {},
                      Email = '{}'                      
                  WHERE GpmId = {}'''.format(name, area, pincode, email, gpm_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def delete_gpm(conn, gpm_id):
    """
    Delete gpm.
    :param conn:
    :param gpm_id:
    :return:
    """
    sql = "DELETE FROM Gpms WHERE GpmId={}".format(gpm_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def show_gpm_details(conn, bdo_id):
    """
    show details of all GPMs under a particular BDO.
    :param conn:
    :param bdo_id:
    :return:
    """
    sql = "SELECT GpmId,Name,Email,Area,Pincode,date(RegisteredAt) FROM Gpms WHERE BdoId = {}".format(bdo_id)
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    for row in records:
        print('''
                GPM ID: {}
                Name: {}
                Email: {}
                Area: {}
                Pincode: {}
                RegisteredAt: {}\n'''.format(row[0], row[1], row[2], row[3], row[4], row[5]))


def create_project(conn, project):
    """
    create project.
    :param conn:
    :param project:
    :return:
    """
    sql = '''INSERT INTO Projects (BdoId, Type, Name, Area, TotalMembers, CostEstimate, StartDate, EndDate )
             VALUES({}, '{}', '{}', '{}', {}, {}, '{}', '{}')
          '''.format(project.bdoId, project.type, project.name, project.area, project.total_members,
                     project.cost_estimate, project.start_date, project.end_date)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid


def get_project_by_id(conn, project_id):
    """
    get details of a particular project.
    :param conn:
    :param project_id:
    :return: details of project matching the projectId
    """
    sql = '''SELECT Type,Name,Area,TotalMembers,CostEstimate,StartDate,EndDate 
             FROM Projects WHERE ProjectId = {}'''.format(project_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()


def update_project(conn, project_type, name, area, total_members, cost_estimate, start_date, end_date, project_id):
    """
    Update project details.
    :param conn:
    :param project_type:
    :param name:
    :param area:
    :param total_members:
    :param cost_estimate:
    :param start_date:
    :param end_date:
    :param project_id:
    :return:
    """
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
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def delete_project(conn, project_id):
    """
    Delete Project.
    :param conn:
    :param project_id:
    :return:
    """
    sql = "DELETE FROM Projects WHERE ProjectId={}".format(project_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def show_project_details(conn, bdo_id):
    """
    Show Details of all projects under a particular BDO.
    :param conn:
    :param bdo_id:
    :return:
    """
    sql = '''SELECT ProjectId, Type, Name, Area, TotalMembers ,CostEstimate, date(StartDate), date(EndDate)
             FROM Projects WHERE BdoId = {}'''.format(bdo_id)
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    for row in records:
        print('''
                Project ID: {}
                Project Type: {}
                Name: {}
                Area: {}
                TotalMembers: {}
                CostEstimate: {}
                StartDate: {}
                EndDate: {}\n'''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


def show_project_approval_requests(conn, bdo_id):
    """
    Show status of all project assignment approval requests
    :param conn:
    :param bdo_id:
    :return: status of all project assignment approval requests
    """
    sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
             Projects.Name as ProjectName, Members.MemberName,ProjectMembers.Approval
             from ProjectMembers inner join Projects on 
             ProjectMembers.ProjectId = Projects.ProjectId
             inner join Members on ProjectMembers.MemberId = Members.MemberId
             inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
             Where ProjectMembers.BdoId = {} and ProjectMembers.Approval = 1 or ProjectMembers.Approval = 2'''.format(bdo_id)

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def show_project_approval_pending_requests(conn, bdo_id):
    """
    Show pending project assignment approval requests
    :param conn:
    :param bdo_id:
    :return: all pending project assignment approval requests
    """
    sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
             Projects.Name as ProjectName, Members.MemberName,ProjectMembers.Approval
             from ProjectMembers inner join Projects on 
             ProjectMembers.ProjectId = Projects.ProjectId
             inner join Members on ProjectMembers.MemberId = Members.MemberId
             inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
             Where ProjectMembers.BdoId = {} and ProjectMembers.Approval = 0'''.format(bdo_id)

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def approve_project_assignment(conn, status, project_member_id):
    """
    Approve/Reject Project Assignment.
    :param conn:
    :param status:
    :param project_member_id:
    :return:
    """
    sql = '''Update ProjectMembers Set Approval = {} Where ProjectMemberId = {} 
              '''.format(status, project_member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Action Successful.")


def show_wage_approval_requests(conn, bdo_id):
    """
       Show all wage approval requests status.
       :param conn:
       :param bdo_id:
       :return: wage approval requests status.
    """
    sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
             Projects.Name as ProjectName, Members.MemberName,
             ProjectMembers.TotalWorkingDays, ProjectMembers.Wage,
             ProjectMembers.Attendance, ProjectMembers.WageApproval
             from ProjectMembers inner join Projects on 
             ProjectMembers.ProjectId = Projects.ProjectId
             inner join Members on ProjectMembers.MemberId = Members.MemberId
             inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
             Where ProjectMembers.BdoId = {} and ProjectMembers.WageApproval = 1 or ProjectMembers.WageApproval = 2 '''.format(bdo_id)

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def show_wage_approval_pending_requests(conn, bdo_id):
    """
    Show pending wage approval requests status.
    :param conn:
    :param bdo_id:
    :return: pending wage approval requests status.
    """
    sql = '''select ProjectMembers.ProjectMemberId as Id,Gpms.Name as GpmName,
             Projects.Name as ProjectName, Members.MemberName,
             ProjectMembers.TotalWorkingDays, ProjectMembers.Wage,
             ProjectMembers.Attendance, ProjectMembers.WageApproval
             from ProjectMembers inner join Projects on 
             ProjectMembers.ProjectId = Projects.ProjectId
             inner join Members on ProjectMembers.MemberId = Members.MemberId
             inner join Gpms on ProjectMembers.GpmId = Gpms.GpmId
             Where ProjectMembers.BdoId = {} and ProjectMembers.WageApproval = 0'''.format(bdo_id)

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def approve_wage(conn, status, project_member_id):
    """
    Approve Wage.
    :param conn:
    :param status:
    :param project_member_id:
    :return:
    """
    sql = '''Update ProjectMembers Set WageApproval = {} Where ProjectMemberId = {} 
              '''.format(status, project_member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Action Successful.")


def view_complaints(conn, bdo_id):
    """
    View complaints.
    :param conn:
    :param bdo_id:
    :return:
    """
    sql = '''Select MemberId,GpmId,Issue 
             From ComplaintLogs Where BdoId = {}
          '''.format(bdo_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


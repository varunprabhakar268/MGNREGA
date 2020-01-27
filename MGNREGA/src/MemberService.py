from getpass import getpass


def member_login(conn, email):
    sql = "SELECT Email,Password,BdoId,GpmId,MemberId FROM Members WHERE Email = '{}'".format(email)
    cur = conn.cursor()
    cur.execute(sql)
    record = cur.fetchone()
    if record:
        if record[1] is None:
            password = getpass('\tFirst Time Login. Please set your password: ')
            update_password = "Update Members SET Password = '{}' WHERE MemberId = {}".format(password, record[4])
            cur.execute(update_password)
            ids = [record[2], record[3], record[4]]
            return ids
        else:
            password = getpass('\tEnter Password: ')
            if record[1] == password:
                print("Authentication Successful")
                ids = [record[2], record[3], record[4]]
                return ids
            else:
                print("Authentication failed. Please check your credentials")
    else:
        print("User does not exist")


def update_project_member_attendance(conn, project_member_id):
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
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def update_project_member_wage(conn, project_member_id):
    sql = '''Update ProjectMembers Set 
             Wage = TotalWorkingDays * 100
             where ProjectMemberId = {}
          '''.format(project_member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def show_member_details(conn, member_id):
    sql = '''With MemberWage(Wage) as (select Sum(Wage)as TotalWage from ProjectMembers
             Where MemberId = {} and WageApproval = 1)
             select MemberName, Email, Age, Gender, Place, Address,Wage from Members,MemberWage
             Where MemberId = {}'''.format(member_id, member_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()


def file_complaint(conn, bdo_id, gpm_id, member_id, issue):
    sql = '''Insert into ComplaintLogs(BdoId,GpmId,MemberId,Issue)
             Values({},{},{},'{}')'''.format(bdo_id, gpm_id, member_id, issue)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid








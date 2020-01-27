from getpass import getpass

def gpm_login(conn, email):
    """
    Authenticate GPM.
    :param conn:
    :param email:
    :return: GpmId
    """
    sql = "SELECT Email,Password,GpmId,BdoId FROM Gpms WHERE Email = '{}'".format(email)
    cur = conn.cursor()
    cur.execute(sql)
    record = cur.fetchone()
    if record:
        if record[1] is None:
            password = getpass('\tFirst time Login. Enter Password: ')
            update_password = "Update Gpms SET Password = '{}' WHERE GpmId = {}".format(password, record[2])
            cur.execute(update_password)
            ids = [record[2], record[3]]
            return ids
        else:
            password = getpass('\tEnter Password: ')
            if record[1] == password:
                print("Authentication Successful")
                ids = [record[2], record[3]]
                return ids
            else:
                print("Authentication failed. Please check your credentials")
    else:
        print("User does not exist")


def create_member(conn, member):
    """
    Add Member.
    :param conn:
    :param member:
    :return: Id of the newly added Member.
    """
    sql = '''
            INSERT INTO Members (BdoId, GpmId, MemberName,Email, Age, Gender, Place, Address,RegisteredAt)
            VALUES({}, {}, '{}', '{}', {}, '{}', '{}', '{}','{}')
          '''.format(member.bdo_id, member.gpm_id, member.name,member.email, member.age, member.gender, member.place, member.address, member.RegisteredAt)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid


def get_member_by_id(conn, member_id):
    """
    Get details of a particular member.
    :param conn:
    :param member_id:
    :return: details of a particular member matching the Id.
    """
    sql = '''SELECT MemberName,Email,Age,Gender,Place,Address
             FROM Members WHERE MemberId = {}'''.format(member_id)
    cur = conn.cursor()
    cur.execute(sql)
    record = cur.fetchone()
    return record


def update_member(conn, name, email, age, gender, place, address, member_id):
    """
    Update Member Details
    :param conn:
    :param name:
    :param email:
    :param age:
    :param gender:
    :param place:
    :param address:
    :param member_id:
    :return:
    """
    sql = ''' UPDATE Members
                  SET MemberName = '{}',
                      Email = '{}',
                      Age = {},
                      Gender = '{}',
                      Place = '{}',
                      Address = '{}'                      
                  WHERE MemberId = {}'''.format(name, email, age, gender, place, address, member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def delete_member(conn, member_id):
    """
    Delete Member.
    :param conn:
    :param member_id:
    :return:
    """
    sql = "DELETE FROM Members WHERE MemberId={}".format(member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def show_member_details(conn, gpm_id):
    """
    Display details of all Members under a particular GPM.
    :param conn:
    :param gpm_id:
    :return:
    """
    sql = '''SELECT MemberId,MemberName,Age,Gender,Place,Address
             FROM Members WHERE GpmId = {}'''.format(gpm_id)
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    for row in records:

        print('''
                MemberId ID: {}
                Name: {}
                Age: {}
                Gender: {}
                Place: {}
                Address: {}
              '''.format(row[0], row[1], row[2], row[3], row[4], row[5]))


def assign_project_member(conn, projectmember):
    """
    Assign member to project
    :param conn:
    :param projectmember:
    :return: ProjectMemberId
    """
    sql = '''INSERT INTO ProjectMembers(BdoId,GpmId,ProjectId,MemberId,Area,Pincode,TotalWorkingDays,Wage,Attendance,Approval,CreatedAt,WageApproval)
             Values({},{},{},{},'{}',{},{},{},{},{},'{}',{})
          '''.format(projectmember.bdo_id, projectmember.gpm_id, projectmember.project_id, projectmember.member_id, projectmember.area, projectmember.pincode, projectmember.total_working_days, projectmember.wage, projectmember.attendance, projectmember.project_approval, projectmember.RegisteredAt,projectmember.wage_approval)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid


def delete_project_member(conn, project_id, member_id):
    """
    Delete Project Member.
    :param conn:
    :param project_id:
    :param member_id:
    :return:
    """
    sql = '''DELETE FROM ProjectMembers WHERE ProjectId = {} and MemberId = {}
          '''.format(project_id, member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Member removed from Project.")


def update_project_member(conn, area, pincode, project_member_id):
    """
    Update Project Member Details.
    :param conn:
    :param area:
    :param pincode:
    :param project_member_id:
    :return:
    """
    sql = ''' UPDATE ProjectMembers
              SET Area = '{}',
                  Pincode = {}                
              WHERE ProjectMemberId = {}
          '''.format(area, pincode, project_member_id)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Update Successful.")


def show_project_member_details(conn, gpm_id):
    """
    Show details of all project Members.
    :param conn:
    :param gpm_id:
    :return:
    """

    sql = '''SELECT ProjectMembers.ProjectId ,Projects.Name,ProjectMembers.MemberId,Members.MemberName,
             ProjectMembers.Area,ProjectMembers.Pincode,Members.Age,ProjectMembers.TotalWorkingDays,
             ProjectMembers.Wage,ProjectMembers.Attendance 
             FROM ProjectMembers inner join Projects on ProjectMembers.ProjectId = Projects.ProjectId
             inner join Members on ProjectMembers.MemberId = Members.MemberId
             WHERE ProjectMembers.GpmId = {}
             order by ProjectMembers.ProjectId
          '''.format(gpm_id)
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    for row in records:
        print('''\tProject Id: {} \n\tProject Name: {} \n\tMember Id: {} \n\tMemberName: {}\n\tArea: {}\n\tPincode: {}\n \tAge: {}\n\tTotal Working Days: {} \n\tWage: {} \n\tAttendance: {}
                '''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))


def fetch_project_members(conn,project_id):
    """
    Fetch details of all Members in a particular project.
    :param conn:
    :param project_id:
    :return:
    """
    sql = '''SELECT ProjectMembers.MemberId, Members.MemberName,ProjectMembers.Area,ProjectMembers.Pincode,Members.Age 
             FROM ProjectMembers inner join Members on ProjectMembers.MemberId = Members.MemberId
             WHERE ProjectId = {} '''.format(project_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def fetch_project_member(conn, project_id, member_id):
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
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()


def issue_job_card(conn,member_id):
    """
    Issue Job Card.
    :param conn:
    :param member_id:
    :return:
    """
    sql = '''Select MemberName, Age, Gender, Place, Address 
             From Members Where MemberId = {}
          '''.format(member_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()


def view_complaints(conn, gpm_id):
    """
    View Complaints from Members.
    :param conn:
    :param gpm_id:
    :return:
    """
    sql = '''Select MemberId,Issue 
             From ComplaintLogs Where GpmId = {}
          '''.format(gpm_id)
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()



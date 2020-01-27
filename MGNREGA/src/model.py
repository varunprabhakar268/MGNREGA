import datetime


class User:

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.area = kwargs.get('area', None)
        self.pincode = kwargs.get('pincode', None)
        self.RegisteredAt = datetime.datetime.now()
        self.email = kwargs.get('email', None)
        self.password = kwargs.get('password', None)


class Bdo(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_bdo(self, conn):
        bdo = (self.name, self.area, self.pincode, self.email, self.password, self.RegisteredAt)
        sql = ''' INSERT INTO Bdos(Name, Area, Pincode, Email, Password, RegisteredAt )
                  VALUES(?, ?, ?, ?, ?, ?) '''
        cur = conn.cursor()
        cur.execute(sql, bdo)
        return cur.lastrowid


class Gpm(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BdoId = kwargs.get('BdoId', None)


class Project:
    def __init__(self, **kwargs):
        self.bdoId = kwargs.get('bdoId', None)
        self.type = kwargs.get('type', None)
        self.name = kwargs.get('name', None)
        self.area = kwargs.get('area', None)
        self.total_members = kwargs.get('total_members', None)
        self.cost_estimate = kwargs.get('cost_estimate', None)
        self.start_date = kwargs.get('start_date', None)
        self.end_date = kwargs.get('end_date', None)


class Member(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bdo_id = kwargs.get('bdoId', None)
        self.gpm_id = kwargs.get('gpmId', None)
        self.age = kwargs.get('age', None)
        self.gender = kwargs.get('gender', None)
        self.place = kwargs.get('place', None)
        self.address = kwargs.get('address', None)
        self.total_wage = 0
        self.wage_approval = 0


class ProjectMember(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bdo_id = kwargs.get('bdoId', None)
        self.gpm_id = kwargs.get('gpmId', None)
        self.project_id = kwargs.get('projectId', None)
        self.member_id = kwargs.get('memberId', None)
        self.total_working_days = 0
        self.wage = 0
        self.attendance = 0
        self.project_approval = 0
        self.wage_approval = 0








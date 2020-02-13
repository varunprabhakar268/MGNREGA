

def create_tables(conn):
    cur = conn.cursor()

    bdo_table = '''CREATE TABLE if not exists Bdos (
    BdoId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Name TEXT NOT NULL UNIQUE,
    Area TEXT,
    Pincode INTEGER,
    Email TEXT NOT NULL UNIQUE,
    Password TEXT,
    RegisteredAt REAL
    );'''
    cur.execute(bdo_table)
    conn.commit()

    gpm_table = '''CREATE TABLE if not exists Gpms (
    GpmId	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    BdoId	INTEGER NOT NULL,
    Name	TEXT NOT NULL,
    Area	TEXT NOT NULL,
    Pincode	INTEGER NOT NULL,
    Email	TEXT NOT NULL UNIQUE,
    Password	TEXT,
    RegisteredAt	REAL,
    FOREIGN KEY(BdoId) REFERENCES Bdos(BdoId)
    );'''
    cur.execute(gpm_table)
    conn.commit()

    members_table = '''CREATE TABLE if not exists Members (
    MemberId	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    BdoId	INTEGER NOT NULL,
    GpmId	INTEGER NOT NULL,
    MemberName	TEXT NOT NULL,
    Email	TEXT NOT NULL UNIQUE,
    Password	TEXT,
    Age	INTEGER NOT NULL,
    Gender	TEXT NOT NULL,
    Place	TEXT NOT NULL,
    Address	TEXT NOT NULL,
    RegisteredAt	REAL NOT NULL,
    FOREIGN KEY(GpmId) REFERENCES Gpms(GpmId),
    FOREIGN KEY(BdoId) REFERENCES Bdos(BdoId)
    );'''
    cur.execute(members_table)
    conn.commit()

    projects_table = '''CREATE TABLE if not exists Projects (
    ProjectId	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    BdoId	INTEGER NOT NULL,
    Type	TEXT NOT NULL,
    Name	TEXT NOT NULL,
    Area	TEXT NOT NULL,
    TotalMembers	INTEGER NOT NULL,
    CostEstimate	INTEGER NOT NULL,
    StartDate	TEXT NOT NULL,
    EndDate	TEXT NOT NULL,
    FOREIGN KEY(BdoId) REFERENCES Bdos(BdoId)
    );'''
    cur.execute(projects_table)
    conn.commit()

    project_memebers_table = '''CREATE TABLE if not exists ProjectMembers (
    `ProjectMemberId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `BdoId`	INTEGER NOT NULL,
    `GpmId`	INTEGER NOT NULL,
    `ProjectId`	INTEGER NOT NULL,
    `MemberId`	INTEGER NOT NULL,
    `Area`	TEXT NOT NULL,
    `Pincode`	INTEGER NOT NULL,
    `TotalWorkingDays`	INTEGER,
    `Wage`	INTEGER,
    `Attendance`	INTEGER,
    `Approval`	INTEGER,
    `CreatedAt`	REAL NOT NULL,
    `WageApproval`	INTEGER,
    FOREIGN KEY(`GpmId`) REFERENCES `Gpms`(`GpmId`),
    FOREIGN KEY(`MemberId`) REFERENCES `Members`(`MemberId`),
    FOREIGN KEY(`BdoId`) REFERENCES `Bdos`(`BdoId`),
    FOREIGN KEY(`ProjectId`) REFERENCES `Projects`(`ProjectId`)
    );'''
    cur.execute(project_memebers_table)
    conn.commit()

    complaint_logs_table = '''CREATE TABLE if not exists ComplaintLogs (
    `ComplaintId`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `BdoId`	INTEGER NOT NULL,
    `GpmId`	INTEGER NOT NULL,
    `MemberId`	INTEGER NOT NULL,
    `Issue`	TEXT NOT NULL,
    FOREIGN KEY(`BdoId`) REFERENCES `Bdos`(`BdoId`),
    FOREIGN KEY(`GpmId`) REFERENCES `Gpms`(`GpmId`),
    FOREIGN KEY(`MemberId`) REFERENCES `Members`(`MemberId`)
    );'''
    cur.execute(complaint_logs_table)
    conn.commit()

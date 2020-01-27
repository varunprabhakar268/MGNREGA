from src import model, BdoService, GpmService, MemberService, Tables
import sqlite3
from sqlite3 import Error
from getpass import getpass


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        Tables.create_tables(conn)
        sql = "PRAGMA foreign_keys = ON"
        cur = conn.cursor()
        cur.execute(sql)

    except Error as e:
        print(e)
    return conn


if __name__ == '__main__':
    ch = ''
    num = 0
    database = "MnregaDb"

    conn = create_connection(database)

    while ch != 5:

        print("\tMAIN MENU")
        print("\t1. Register BDO")
        print("\t2. BDO Login")
        print("\t3. GPM Login")
        print("\t4. Member Login")
        print("\t5. Exit")
        ch = input("\tSelect Your Option ")

        if ch == '1':
            SuperUser = str(input("Enter SuperUser Password: "))
            if SuperUser == "BATMAN":
                try:
                    Name = str(input("\tEnter Name: "))
                    Email = str(input("\tEnter EmailId: "))
                    Password = str(input("\tEnter Password: "))
                    Area = str(input("\tEnter Area: "))
                    Pincode = int(input("\tEnter Pincode: "))
                    BDO = model.Bdo(name=Name, email=Email, password=Password, area=Area, pincode=Pincode)
                    with conn:
                        Id = BDO.create_bdo(conn)
                        print("BDO registered successfully \n BDO ID: ", Id)
                except ValueError:
                    print("Invalid Input.")
                    continue
                except Error as e:
                    print(e)
            else:
                print("Authentication failed.")

        elif ch == '2':
            Email = str(input("\tEnter Email Id: "))
            with conn:
                Id = BdoService.bdo_login(conn, Email)
            if Id:
                option = ''
                while option != '15':
                    print("\t1. Add GPM")
                    print("\t2. Show GPMs")
                    print("\t3. Update GPM")
                    print("\t4. Delete GPM")
                    print("\t5. Add Project")
                    print("\t6. Show Projects")
                    print("\t7. Update Project")
                    print("\t8. Delete Project")
                    print("\t9. ProjectAssignment Approval Requests Status")
                    print("\t10. ProjectAssignment Approval Pending Requests")
                    print("\t11. Wage Approval Status")
                    print("\t12. Wage Approval Pending Requests")
                    print("\t13. View Complaints")
                    print("\t14. Exit")

                    option = input("Select Option ")

                    if option == '1':
                        try:
                            Name = str(input("\t Enter GPM Name: "))
                            Email = str(input("\t Enter GPM EmailId: "))
                            Area = str(input("\t Enter Area: "))
                            Pincode = int(input("\t Enter Pincode: "))
                            bdo_id = Id
                            GPM = model.Gpm(BdoId=bdo_id, name=Name, email=Email, area=Area, pincode=Pincode)
                            with conn:
                                Gpm_Id = BdoService.create_gpm(conn, GPM)
                                print("Successfully created GPM. GPM ID: ", Gpm_Id)
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '2':
                        try:
                            with conn:
                                BdoService.show_gpm_details(conn, Id)
                        except:
                            print("Some Error occured. Please try again.")
                    elif option == '3':
                        try:
                            Gpm_Id = int(input("Enter GPM Id "))
                            with conn:
                                record = BdoService.get_gpm_by_id(conn, Gpm_Id)
                                print('''Name: {}\tEmail: {}\tArea: {}\tPincode: {}
                                        '''.format(record[0], record[1], record[2], record[3]))

                            Name = str(input("Enter Updated Name ") or record[0])
                            Email = str(input("Enter Updated Email ") or record[1])
                            Area = str(input("Enter Updated Area ") or record[2])
                            Pincode = int(input("Enter Updated Pincode ") or record[3])

                            with conn:
                                BdoService.update_gpm(conn, Name, Area, Pincode, Email, Gpm_Id)
                                print("Record Updated Successfully")
                                record = BdoService.get_gpm_by_id(conn, Gpm_Id)
                                print('''Name: {}\tEmail: {}\tArea: {}\tPincode: {}
                                      '''.format(record[0], record[1], record[2], record[3]))
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '4':
                        try:
                            Gpm_Id = int(input("Enter GPM Id "))
                            with conn:
                                BdoService.delete_gpm(conn, Gpm_Id)
                                print("GPM Deleted")
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '5':
                        try:
                            bdo_id = Id
                            choice = ''
                            print("Select Project Type: ")
                            print("1. Road Construction")
                            print("2. Sewage Treatment")
                            print("3. Building Construction")
                            choice = input("Select your option.")
                            if choice == '1':
                                project_type = "Road Construction"
                            elif choice == '2':
                                project_type = "Sewage Treatment"
                            elif choice == '3':
                                project_type = "Building Construction"
                            else:
                                print("Invalid choice.")
                                continue

                            Name = str(input("\t Enter Project Name: "))
                            Area = str(input("\t Enter Area: "))

                            TotalMembers = int(input("\t Enter Total Members: "))
                            CostEstimate = int(input("\t Enter Cost Estimate: "))
                            StartDate = str(input("\t Enter Start Date in YYYY-MM-DD format: "))
                            EndDate = str(input("\t Enter Estimated End Date in YYYY-MM-DD format: "))
                            project = model.Project(bdoId=bdo_id, type=project_type, name=Name, area=Area, total_members=TotalMembers, cost_estimate=CostEstimate, start_date=StartDate, end_date=EndDate)

                            with conn:
                                project_Id = BdoService.create_project(conn, project)
                                print("Successfully created Project. Project ID: ", project_Id)
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '6':
                        with conn:
                            BdoService.show_project_details(conn, Id)

                    elif option == '7':
                        try:
                            Project_Id = int(input("Enter Project Id "))
                            with conn:
                                row = BdoService.get_project_by_id(conn, Project_Id)
                                print('''
                                Project Type: {}
                                Name: {}
                                Area: {}
                                TotalMembers: {}
                                CostEstimate: {}
                                StartDate: {}
                                EndDate: {}
                                \n'''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                            choice = ''
                            print("Select Updated Project Type: ")
                            print("1. Road Construction")
                            print("2. Sewage Treatment")
                            print("3. Building Construction")
                            choice = input()
                            if choice == '1':
                                project_type = "Road Construction"
                            elif choice == '2':
                                project_type = "Sewage Treatment"
                            elif choice == '3':
                                project_type = "Building Construction"
                            else:
                                print("Invalid Choice.")
                            Name = str(input("Enter Updated Name ") or row[1])
                            Area = str(input("Enter Updated Area ") or row[2])
                            TotalMembers = int(input("Enter Updated TotalMembers ") or row[3])
                            CostEstimate = int(input("Enter Updated CostEstimate ") or row[4])
                            StartDate = str(input("Enter Updated StartDate ") or row[5])
                            EndDate = str(input("Enter Updated EndDate ") or row[6])

                            with conn:
                                BdoService.update_project(conn, project_type, Name, Area, TotalMembers, CostEstimate, StartDate, EndDate, Project_Id)
                                print("Record Updated Successfully")
                                row = BdoService.get_project_by_id(conn, Project_Id)
                                print('''
                                Project Type: {}
                                Name: {}
                                Area: {}
                                TotalMembers: {}
                                CostEstimate: {}
                                StartDate: {}
                                EndDate: {}
                                \n'''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")
                    elif option == '8':
                        try:
                            Project_Id = int(input("Enter Project Id "))
                            with conn:
                                BdoService.delete_project(conn, Project_Id)
                                print("Project Deleted \n")

                        except ValueError:
                            print("Invalid Input")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '9':
                        with conn:
                            records = BdoService.show_project_approval_requests(conn, Id)
                            if records:
                                for row in records:
                                    if row[4] == 1:
                                        approval = "Accepted"
                                    else:
                                        approval = "Rejected"
                                    print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tApprovalStatus: {}
                                    '''.format(row[0], row[1], row[2], row[3], approval))
                            else:
                                print("No Report. Approve Requests from  Pending Requests Section.")

                    elif option == '10':
                        try:
                            with conn:
                                records = BdoService.show_project_approval_pending_requests(conn, Id)
                            if records:
                                for row in records:
                                    approval = "Pending"
                                    print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tApprovalStatus: {}
                                        '''.format(row[0], row[1], row[2], row[3], approval))
                                wish = str(input("Do you wish to Approve/Reject Requests (y/n): "))
                                if wish.lower() == 'y':
                                    Id = int(input("Enter Id of the request you want to Approve/Reject: "))
                                    option = int(input("1. Accept\t2. Reject.\nSelect your option. "))
                                    if option == 1:
                                        approval = 1
                                    elif option == 2:
                                        approval = 2
                                    else:
                                        print("Invalid input")
                                    with conn:
                                        BdoService.approve_project_assignment(conn, approval, Id)
                                        MemberService.update_project_member_attendance(conn, Id)
                                        MemberService.update_project_member_wage(conn, Id)
                                elif wish.lower() == 'n':
                                    continue
                                else:
                                    print("invalid input")
                            else:
                                print("No Pending Requests.")
                        except ValueError:
                                print("Invalid Input.")
                                continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '11':
                        with conn:
                            records = BdoService.show_wage_approval_requests(conn, Id)
                            if records:
                                for row in records:
                                    if row[7] == 1:
                                        approval = "Accepted"
                                    else:
                                        approval = "Rejected"
                                    print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tTotal Working Days: {}\tWage: {}\tAttendance: {}\tApproval: {}
                                        '''.format(row[0], row[1], row[2], row[3],row[4],row[5], row[6], approval))
                            else:
                                print("No Report. Approve Requests from  Pending Wage Requests Section.")

                    elif option == '12':
                        try:
                            with conn:
                                records = BdoService.show_wage_approval_pending_requests(conn, Id)
                                if records:
                                    for row in records:
                                        approval = "Pending"
                                        print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tTotal Working Days: {}\tWage: {}\tAttendance: {}\tApproval: {}'''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], approval))

                                    wish = str(input("Do you wish to Approve/Reject Requests (y/n): "))
                                    if wish.lower() == 'y':
                                        Id = int(input("Enter Id of the request you want to Approve/Reject: "))
                                        option = int(input("1. Accept\t2. Reject.\nSelect your option. "))
                                        if option == 1:
                                            approval = 1
                                        elif option == 2:
                                            approval = 2
                                        else:
                                            print("Invalid input")
                                        with conn:
                                            BdoService.approve_wage(conn, approval, Id)
                                    elif wish.lower() == 'n':
                                        continue
                                    else:
                                        print("invalid input")
                                else:
                                    print("No Pending Requests.")
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '13':
                        records = BdoService.view_complaints(conn, Id)
                        if records:
                            for row in records:
                                print('''\tMemberId: {}\tGpmId: {}\tIssue: {}
                                 '''.format(row[0], row[1], row[2]))
                        else:
                            print("No Complaints received.")

                    elif option == '14':
                        break
        elif ch == '3':
            Email = str(input("\tEnter Email Id: "))
            with conn:
                record = GpmService.gpm_login(conn, Email)
            if record:
                Gpm_Id, Bdo_Id = record[0], record[1]
                option = ''
                while option != '13':
                    print("\t1. Add Member")
                    print("\t2. Show Members")
                    print("\t3. Update Member")
                    print("\t4. Delete Member")
                    print("\t5. Show Projects")
                    print("\t6. Assign Task/Project to Members")
                    print("\t7. Show Project Details of Members")
                    print("\t8. Update Task/Project assigned to Members")
                    print("\t9. Remove Member from Project")
                    print("\t10. Issue Job Card")
                    print("\t11. View Complaints")
                    print("\t12. Exit")
                    option = input("Select your option: ")
                    if option == '1':
                        try:
                            Name = str(input("Enter Name: "))
                            Email = str(input("Enter Email: "))
                            Age = int(input("Enter Age: "))
                            Gender = str(input("Enter Gender: "))
                            Place = str(input("Enter Place(City/Town): "))
                            Address = str(input("Enter Address: "))
                            member = model.Member(bdoId=Bdo_Id, gpmId=Gpm_Id, name=Name, email=Email, age=Age, gender=Gender, place=Place, address=Address)
                            with conn:
                                Member_Id = GpmService.create_member(conn, member)
                                print("Successfully created Member. Member ID: ", Member_Id)
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '2':
                        with conn:
                            GpmService.show_member_details(conn, Gpm_Id)

                    elif option == '3':
                        try:
                            Member_Id = int(input("Enter Member Id "))
                            with conn:
                                record = GpmService.get_member_by_id(conn, Member_Id)
                                print('''Name: {}\tEmail: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}
                                    '''.format(record[0], record[1], record[2], record[3], record[4], record[5]))

                            Name = str(input("Enter Updated Name: ") or record[0])
                            Email = str(input("Enter Updated Email: ") or record[1])
                            Age = int(input("Enter Updated Age: ") or record[2])
                            Gender = str(input("Enter Updated Gender: ") or record[3])
                            Place = str(input("Enter Updated Place(City/Town): ") or record[4])
                            Address = str(input("Enter Updated Address: ") or record[5])

                            with conn:
                                GpmService.update_member(conn, Name, Email, Age, Gender, Place, Address, Member_Id)
                                print("Record Updated Successfully")
                                record = GpmService.get_member_by_id(conn, Member_Id)
                                print('''Name: {}\tEmail: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}
                                      '''.format(record[0], record[1], record[2], record[3], record[4], record[5]))
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '4':
                        try:
                            Member_Id = int(input("Enter Member Id "))
                            with conn:
                                GpmService.delete_member(conn, Member_Id)
                                print("Member Deleted")
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '5':
                        with conn:
                            BdoService.show_project_details(conn, Bdo_Id)

                    elif option == '6':
                        try:
                            ProjectId = int(input("Enter Project Id: "))
                            MemberId = int(input("Enter Member Id: "))
                            Area = str(input("Enter Area: "))
                            Pincode = int(input("Enter Pincode: "))
                            project_member = model.ProjectMember(bdoId=Bdo_Id, gpmId=Gpm_Id,area=Area,pincode=Pincode, projectId=ProjectId, memberId=MemberId)
                            with conn:
                                Id = GpmService.assign_project_member(conn, project_member)
                                print(" Member Assigned to Project.")
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '7':
                        with conn:
                            GpmService.show_project_member_details(conn, Gpm_Id)

                    elif option == '8':
                        try:
                            ProjectId = int(input("Enter Project Id of the Project whose Member Details you want to update: "))
                            with conn:
                                records = GpmService.fetch_project_members(conn, ProjectId)
                                if records:
                                    print("Following Members have been allotted the project")
                                    for row in records:
                                        print('''\tMember Id: {}\tMemberName: {}\tArea: {}\tPincode: {}\tAge: {}
                                              '''.format(row[0], row[1], row[2], row[3], row[4]))
                                    MemberId = int(input("Enter Member Id of the Member whose details you want to update"))

                                    ProjectMember = GpmService.fetch_project_member(conn, ProjectId, MemberId)
                                    ProjectMemberId = ProjectMember[0]
                                    Area = str(input("Enter Updated Area: ") or ProjectMember[1])
                                    Pincode = int(input("Enter Updated Pincode: ") or ProjectMember[2])

                                    GpmService.update_project_member(conn, Area, Pincode, ProjectMemberId)

                                else:
                                    print("No Members Found")
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '9':
                        try:
                            ProjectId = int(input("Enter Project Id: "))
                            with conn:
                                records = GpmService.fetch_project_members(conn, ProjectId)
                                if records:
                                    for row in records:
                                        print('''\tMember Id: {}\tMemberName: {}\tArea: {}\tPincode: {}\tAge: {}
                                              '''.format(row[0], row[1], row[2], row[3], row[4]))
                                    MemberId = int(input("\n Enter Member Id of the member you want to remove"))
                                    GpmService.delete_project_member(conn,ProjectId,MemberId)
                                else:
                                    print("No Members Found")
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '10':
                        try:
                            MemberId = int(input("Enter Member Id: "))
                            with conn:
                                Member = GpmService.issue_job_card(conn, MemberId)
                                print("Job Card Issued")
                                print('''Name: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}
                                      '''.format(Member[0], Member[1], Member[2], Member[3], Member[4]))
                        except ValueError:
                            print("Invalid Input.")
                            continue
                        except:
                            print("Some Error occured. Please try again.")

                    elif option == '11':
                        with conn:
                            records = GpmService.view_complaints(conn, Gpm_Id)
                        if records:
                            for row in records:
                                print('''\tMemberId: {}\tIssue: {}
                                 '''.format(row[0], row[1]))
                        else:
                            print("No Complaints received.")

                    elif option == '12':
                        break

        elif ch == '4':
            Email = str(input("\tEnter Email Id: "))
            with conn:
                record = MemberService.member_login(conn, Email)
            if record:
                Bdo_Id, Gpm_Id, Member_Id = record[0], record[1], record[2]

                option = ''
                while option != '4':
                    print("\t1. View Personal Details")
                    print("\t2. File Complaint")
                    print("\t3. Exit")
                    option = input("Select your option: ")
                    if option == '1':
                        with conn:
                            record = MemberService.show_member_details(conn, Member_Id)
                            print('''\tName: {}\tEmail: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}\tWage: {}
                            '''.format(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
                    elif option == '2':
                        with conn:
                            issue = str(input("\tEnter your Issue: "))
                            IssueId = MemberService.file_complaint(conn, Bdo_Id, Gpm_Id, Member_Id, issue)
                            print("Complaint Filed. Complaint Id: ", IssueId)

                    elif option == '3':
                        break

        else:
            print("Invalid choice")

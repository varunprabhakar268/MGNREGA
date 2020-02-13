from src import model, BdoService, GpmService, MemberService, Tables
import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    db_file = "MnregaDb"
    try:
        conn = sqlite3.connect(db_file)
        Tables.create_tables(conn)
        sql = "PRAGMA foreign_keys = ON"
        cur = conn.cursor()
        cur.execute(sql)
        return conn
    except Error as e:
        print(e)


if __name__ == '__main__':
    ch = ''
    num = 0
    conn = create_connection()

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
                    BDO = model.BdoModel(name=Name, email=Email, password=Password, area=Area, pincode=Pincode)
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
            bdo = BdoService.Bdo()
            if bdo.bdo_login():
                option = ''
                while option != '16':
                    print("\t1. Add GPM")
                    print("\t2. Show GPMs")
                    print("\t3. Update GPM")
                    print("\t4. Delete GPM")
                    print("\t5. Add Project")
                    print("\t6. Show Projects")
                    print("\t7. Update Project")
                    print("\t8. Delete Project")
                    print("\t9. ProjectAssignment Approval Requests Status")
                    print("\t10. ProjectAssignment Approval Pending Requests/Approve Requests")
                    print("\t11. Wage Approval Status")
                    print("\t12. Wage Approval Pending Requests/Approve Wage")
                    print("\t13. View Complaints")
                    print("\t14. Show Members")
                    print("\t15. Show Project Details of Members")
                    print("\t16. Exit to Main Menu")

                    option = input("Select Option ")

                    if option == '1':
                        bdo.create_gpm()
                    elif option == '2':
                        bdo.show_gpm_details()
                    elif option == '3':
                        bdo.update_gpm()
                    elif option == '4':
                        bdo.delete_gpm()
                    elif option == '5':
                        bdo.create_project()
                    elif option == '6':
                        bdo.show_project_details()
                    elif option == '7':
                        bdo.update_project()
                    elif option == '8':
                        bdo.delete_project()
                    elif option == '9':
                        bdo.show_project_approval_requests()
                    elif option == '10':
                        bdo.show_project_approval_pending_requests()
                    elif option == '11':
                        bdo.show_wage_approval_requests()
                    elif option == '12':
                        bdo.show_wage_approval_pending_requests()
                    elif option == '13':
                        bdo.view_complaints()
                    elif option == '14':
                        bdo.show_member_details()
                    elif option == '15':
                        bdo.show_project_member_details()
                    elif option == '16':
                        break
                    else:
                        print("Invalid choice")
        elif ch == '3':
            gpm = GpmService.gpm()
            if gpm.gpm_login():
                option = ''
                while option != '12':
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
                    print("\t12. Exit to Main Menu")
                    option = input("Select your option: ")
                    if option == '1':
                        gpm.create_member()
                    elif option == '2':
                        gpm.show_member_details()
                    elif option == '3':
                        gpm.update_member()
                    elif option == '4':
                        gpm.delete_member()
                    elif option == '5':
                        gpm.show_project_details()
                    elif option == '6':
                        gpm.assign_project_member()
                    elif option == '7':
                        gpm.show_project_member_details()
                    elif option == '8':
                        gpm.update_project_member()
                    elif option == '9':
                        gpm.delete_project_member()
                    elif option == '10':
                        gpm.issue_job_card()
                    elif option == '11':
                        gpm.view_complaints()
                    elif option == '12':
                        break
                    else:
                        print("Invalid choice")

        elif ch == '4':
            member = MemberService.member()
            if member.member_login():
                option = ''
                while option != '3':
                    print("\t1. View Personal Details")
                    print("\t2. File Complaint")
                    print("\t3. Exit to Main Menu")
                    option = input("Select your option: ")
                    if option == '1':
                        member.show_member_details()
                    elif option == '2':
                        member.file_complaint()
                    elif option == '3':
                        break
                    else:
                        print("Invalid choice")
        elif ch == '5':
            print("Thank You.")
            break
        else:
            print("Invalid choice")
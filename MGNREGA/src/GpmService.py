from getpass import getpass
from src import model, GpmRepository, Main, InputValidations
import sqlite3


class gpm:

    def __init__(self):
        self.bdo_id = None
        self.gpm_id = None
        self.query = GpmRepository.GpmQuery()

    def gpm_login(self):
        """
        Authenticate GPM.
        :param conn:
        :param email:
        :return: GpmId
        """
        email = input("\tEnter Email Id: ")
        record = self.query.login(email)
        if record:
            if record[1] is None:
                password = getpass('\tFirst time Login. Enter Password: ')
                self.query.update_password(password, record[2])
                self.gpm_id = record[2]
                self.bdo_id = record[3]
                return True
            else:
                password = getpass('\tEnter Password: ')
                if record[1] == password:
                    print("\tAuthentication Successful")
                    self.gpm_id = record[2]
                    self.bdo_id = record[3]
                    return True
                else:
                    print("\tAuthentication failed. Please check your credentials")
                    return False
        else:
            print("User does not exist")
            return False

    def create_member(self):
        """
        Add Member.
        :param conn:
        :param member:
        :return: Id of the newly added Member.
        """
        try:
            name = input("Enter Name: ")
            if not name.isalpha():
                print("\tInvalid data format. Name should contain only alphabets. ")
                return False
            email = input("Enter Email: ")
            if not InputValidations.validate_email(email):
                return False
            age = int(input("Enter Age: "))
            gender = input("Enter Gender: ")
            if not gender.isalpha():
                print("\tInvalid data format. Gender should contain only alphabets. ")
                return False
            place = input("Enter Place(City/Town): ")
            if not place.isalpha():
                print("\tInvalid data format. Place should contain only alphabets. ")
                return False
            address = input("Enter Address: ")
            member = model.MemberModel(bdoId=self.bdo_id, gpmId=self.gpm_id, name=name, email=email, age=age,
                                       gender=gender,
                                       place=place, address=address)
            self.query.create_member(member)
            print("Successfully created Member")
            return True

        except ValueError:
            print("Invalid Input.")
            return False

        except:
            print("Some Error occured. Please try again.")
            return False

    def get_member_by_id(self, member_id):
        """
        Get details of a particular member.
        :param conn:
        :param member_id:
        :return: details of a particular member matching the Id.
        """
        record = self.query.get_member_by_id(member_id)
        if record:
            print('''Name: {}\tEmail: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}
                                            '''.format(record[0], record[1], record[2], record[3], record[4],
                                                       record[5]))
            return record
        else:
            print("Member does not exist")
            return False

    def update_member(self):
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
        try:
            member_id = int(input("Enter Member Id "))
            record = self.get_member_by_id(member_id)
            if record:
                name = (input("Enter Updated Name or Enter to continue: ") or record[0])
                if not name.isalpha():
                    print("\tInvalid data format. Name should contain only alphabets. ")
                    return False
                email = (input("Enter Updated Email or Enter to continue: ") or record[1])
                if not InputValidations.validate_email(email):
                    return False
                age = int(input("Enter Updated Age or Enter to continue: ") or record[2])
                gender = (input("Enter Updated Gender or Enter to continue: ") or record[3])
                if not gender.isalpha():
                    print("\tInvalid data format. Gender should contain only alphabets. ")
                    return False
                place = (input("Enter Updated Place(City/Town) or Enter to continue: ") or record[4])
                if not place.isalpha():
                    print("\tInvalid data format. Place should contain only alphabets. ")
                    return False
                address = (input("Enter Updated Address or Enter to continue: ") or record[5])

                self.query.update_member(name, age, gender, email, place, address, member_id)
                print("Record Updated Successfully")
                record = self.get_member_by_id(member_id)
                return True

        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some Error occurred. Please try again.")
            return False

    def delete_member(self):
        """
        Delete Member.
        :param conn:
        :param member_id:
        :return:
        """
        try:
            member_id = int(input("Enter Member Id "))
            record = self.get_member_by_id(member_id)
            if record:
                confirm = input("Do you wish to continue (y/n):")
                if confirm.lower() == 'y':
                    self.query.delete_member(member_id)
                    print("Member Deleted")
                    return True
                else:
                    return False
        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def show_member_details(self):
        """
        Display details of all Members under a particular GPM.
        :param conn:
        :param gpm_id:
        :return:
        """
        try:
            records = self.query.show_member_details(self.gpm_id)
            if records:
                for row in records:
                    print('''
                            MemberId ID: {}
                            Name: {}
                            Age: {}
                            Gender: {}
                            Place: {}
                            Address: {}
                          '''.format(row[0], row[1], row[2], row[3], row[4], row[5]))
                return True
            else:
                print("No records found.")
                return False
        except:
            print("Some Error occurred. Please try again.")
            return False

    def show_project_details(self):
        """
        Show Details of all projects under a particular BDO.
        :param conn:
        :param bdo_id:
        :return:
        """
        try:
            records = self.query.show_project_details(self.bdo_id)
            if records:
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
                return True
            else:
                print("No records found.")
                return False
        except:
            print("Some error occurred. Please try again.")
            return False

    def assign_project_member(self):
        """
        Assign member to project
        :param conn:
        :param projectmember:
        :return: ProjectMemberId
        """
        try:
            project_id = int(input("Enter Project Id: "))
            member_id = int(input("Enter Member Id: "))
            area = input("Enter Area: ")
            pincode = int(input("Enter Pincode: "))
            projectmember = model.ProjectMemberModel(bdoId=self.bdo_id, gpmId=self.gpm_id, area=area, pincode=pincode,
                                                     projectId=project_id, memberId=member_id)

            if self.query.assign_project_member(projectmember):
                print(" Member Assigned to Project.")
                return True
            else:
                print("Action Unsuccessful. Please try again.")

        except ValueError:
            print("Invalid Input.")
            return False
        except sqlite3.IntegrityError:
            print("Invalid Project/MemberId")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def delete_project_member(self):
        """
        Delete Project Member.
        :param conn:
        :param project_id:
        :param member_id:
        :return:
        """
        try:
            project_id = int(input("Enter Project Id: "))
            records = self.query.fetch_project_members(project_id)
            if records:
                print("Following Members have been allotted the project")
                for row in records:
                    print('''\tMember Id: {}\tMemberName: {}\tArea: {}\tPincode: {}\tAge: {}
                                                                          '''.format(row[0], row[1], row[2], row[3],
                                                                                     row[4]))

                member_id = int(input("\n Enter Member Id of the member you want to remove: "))

                project_member = self.query.fetch_project_member(project_id, member_id)

                if project_member:
                    self.query.delete_project_member(project_id, member_id)
                    print("Member removed from Project.")
                    return True
                else:
                    print("No record found. Please try again.")
                    return False

            else:
                print("No record found. Please try again.")
                return False
        except ValueError:
            print("Invalid ProjectId/MemberId.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def update_project_member(self):
        """
        Update Project Member Details.
        :param conn:
        :param area:
        :param pincode:
        :param project_member_id:
        :return:
        """
        try:
            project_id = int(input("Enter Project Id of the Project whose Member Details you want to update: "))
            records = self.query.fetch_project_members(project_id)
            if records:
                print("Following Members have been allotted the project")
                for row in records:
                    print('''\tMember Id: {}\tMemberName: {}\tArea: {}\tPincode: {}\tAge: {}
                                                          '''.format(row[0], row[1], row[2], row[3], row[4]))
                member_id = int(input("Enter Member Id of the Member whose details you want to update: "))
                project_member = self.query.fetch_project_member(project_id, member_id)
                if project_member:
                    project_member_id = project_member[0]
                    area = (input("Enter Updated Area or Enter to continue: ") or project_member[1])
                    pincode = int(input("Enter Updated Pincode or Enter to continue: ") or project_member[2])

                    self.query.update_project_member(area, pincode, project_member_id)
                    print("Update Successful.")
                    return True
                else:
                    print("No record found.")
                    return False

            else:
                print("No record found.")
                return False

        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def show_project_member_details(self):
        """
        Show details of all project Members.
        :param conn:
        :param gpm_id:
        :return:
        """

        records = self.query.show_project_member_details(self.gpm_id)
        if records:
            for row in records:
                print('''\tProject Id: {} \n\tProject Name: {} \n\tMember Id: {} \n\tMemberName: {}\n\tArea: {}\n\tPincode: {}\n \tAge: {}\n\tTotal Working Days: {} \n\tWage: {} \n\tAttendance: {}
                        '''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            return True
        else:
            print("No records found.")
            return False

    def issue_job_card(self):
        """
        Issue Job Card.
        :param conn:
        :param member_id:
        :return:
        """
        try:
            member_id = int(input("Enter Member Id: "))

            record = self.query.issue_job_card(member_id)
            if record:
                print("Job Card Issued")
                print('''Name: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}
                      '''.format(record[0], record[1], record[2], record[3], record[4]))
                return True
            else:
                print("Invalid Member Id.")

        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def view_complaints(self):
        """
        View Complaints from Members.
        :param conn:
        :param gpm_id:
        :return:
        """
        try:
            records = self.query.view_complaints(self.gpm_id)
            if records:
                for row in records:
                    print('''\tMemberId: {}\tIssue: {}
                     '''.format(row[0], row[1]))
                return True
            else:
                print("No Complaints received.")
                return False
        except:
            print("Some Error occured. Please try again.")
            return False

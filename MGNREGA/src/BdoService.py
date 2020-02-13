import datetime
from getpass import getpass

from src import model, BdoRepository, InputValidations


class Bdo:

    def __init__(self):
        self.bdo_id = None
        self.project_type = ['Road Construction', 'Sewage Treatment', 'Building Construction']
        self.query = BdoRepository.BdoQuery()

    def bdo_login(self):
        """ Authenticate BDO.
        :param conn:
        :param email:
        :return: BdoId
        """
        email = input("\tEnter Email: ")
        record = self.query.login(email)
        if record:
            password = getpass('\tEnter Password: ')
            if record[1] == password:
                print("\tAuthentication Successful")
                self.bdo_id = record[2]
                return True
            else:
                print("\tAuthentication failed. Please check your credentials")
                return False
        else:
            print("\tUser does not exist")
            return False

    def create_gpm(self):
        """
        Add GPM.
        :param conn:
        :param gpm:
        :return: GpmId
        """
        try:
            name = input("\t Enter GPM Name: ")
            if not name.isalpha():
                print("\tInvalid data format. Name should contain only alphabets. ")
                return False
            email = input("\t Enter GPM EmailId: ")
            if not InputValidations.validate_email(email):
                return False
            area = input("\t Enter Area: ")
            if not area.isalpha():
                print("\tInvalid data format. Area should contain only alphabets.")
                return False
            pincode = int(input("\t Enter Pincode: "))
            gpm = model.GpmModel(BdoId=self.bdo_id, name=name, email=email, area=area, pincode=pincode)

            self.query.create_gpm(gpm)
            print("\nSuccessfully created GPM")
            return True

        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occurred. Please try again.")
            return False

    def get_gpm_by_id(self, gpm_id):
        """
        Get details of a particular Gpm.
        :param conn:
        :param gpm_id:
        :return: Gpm Details matching the Id
        """
        record = self.query.get_gpm_by_id(gpm_id)
        if record:
            print('''Name: {}\tEmail: {}\tArea: {}\tPincode: {}
                      '''.format(record[0], record[1], record[2], record[3]))
            return record
        else:
            print("Invalid GPM Id")
            return False

    def update_gpm(self):
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
        try:
            gpm_id = int(input("Enter GPM Id "))
            record = self.get_gpm_by_id(gpm_id)
            if record:
                name = (input("Enter Updated Name or Enter to continue ") or record[0])
                if not name.isalpha():
                    print("\tInvalid data format. Name should contain only alphabets. ")
                    return False
                email = (input("Enter Updated Email or Enter to continue ") or record[1])
                if not InputValidations.validate_email(email):
                    return False
                area = (input("Enter Updated Area or Enter to continue ") or record[2])
                if not area.isalpha():
                    print("\tInvalid data format. Area should contain only alphabets.")
                    return False
                pincode = int(input("Enter Updated Pincode or Enter to continue ") or record[3])

                self.query.update_gpm(name, area, pincode, email, gpm_id)
                print("Record Updated Successfully")
                record = self.get_gpm_by_id(gpm_id)
                return True

        except ValueError:
            print("Invalid input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def delete_gpm(self):
        """
        Delete gpm.
        :param conn:
        :param gpm_id:
        :return:
        """
        try:
            gpm_id = int(input("Enter GPM Id "))
            record = self.get_gpm_by_id(gpm_id)
            if record:
                confirm = input("Do you wish to continue? y for yes, any other key to go back: ")
                if confirm.lower() == 'y':
                    self.query.delete_gpm(gpm_id)
                    print("GPM Deleted")
                    return True
                else:
                    return False
        except ValueError:
            print("Invalid GpmId.")
            return False
        except:
            print("Some Error occurred. Please try again.")
            return False

    def show_gpm_details(self):
        """
        show details of all GPMs under a particular BDO.
        :param conn:
        :param bdo_id:
        :return:
        """
        try:
            records = self.query.show_gpm_details(self.bdo_id)
            if records:
                for row in records:
                    print('''
                            GPM ID: {}
                            Name: {}
                            Email: {}
                            Area: {}
                            Pincode: {}
                            RegisteredAt: {}\n'''.format(row[0], row[1], row[2], row[3], row[4], row[5]))
                return True
            else:
                print("No records found.")
                return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def create_project(self):
        """
        create project.
        :param conn:
        :param project:
        :return:
        """
        try:
            print("Select Project Type: ")
            print("1. Road Construction")
            print("2. Sewage Treatment")
            print("3. Building Construction")
            choice = input("Select your option.")
            if choice == '1':
                project_type = self.project_type[0]
            elif choice == '2':
                project_type = self.project_type[1]
            elif choice == '3':
                project_type = self.project_type[2]
            else:
                print("Invalid choice.")
                return False

            name = input("\t Enter Project Name: ")
            if not name.isalpha():
                print("\tInvalid data format. Name should contain only alphabets.")
                return False
            area = input("\t Enter Area: ")
            if not area.isalpha():
                print("\tInvalid data format. Area should contain only alphabets.")
                return False

            total_members = int(input("\t Enter Total Members: "))
            cost_estimate = int(input("\t Enter Cost Estimate: "))
            start_date = str(input("\t Enter Start Date in YYYY-MM-DD: "))
            if InputValidations.validate_date(start_date):
                end_date = str(input("\t Enter Estimated End Date in YYYY-MM-DD: "))
                if InputValidations.validate_date(end_date) and InputValidations.validate_end_date(start_date, end_date):
                    project = model.ProjectModel(bdoId=self.bdo_id, type=project_type, name=name, area=area,
                                         total_members=total_members, cost_estimate=cost_estimate,
                                         start_date=start_date,
                                         end_date=end_date)

                    self.query.create_project(project)
                    print("\nSuccessfully created Project.")
                    return True
        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def get_project_by_id(self, project_id):
        """
        get details of a particular project.
        :param conn:
        :param project_id:
        :return: details of project matching the projectId
        """
        record = self.query.get_project_by_id(project_id)
        if record:
            print('''
                     Project Type: {}
                     Name: {}
                     Area: {}
                     TotalMembers: {}
                     CostEstimate: {}
                     StartDate: {}
                     EndDate: {}
                 \n'''.format(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
            return record
        else:
            print("Project Does not exist")
            return False

    def update_project(self):
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
        try:
            project_id = int(input("Enter Project Id "))

            row = self.get_project_by_id(project_id)
            if row:
                print("Select Updated Project Type: ")
                print("1. Road Construction")
                print("2. Sewage Treatment")
                print("3. Building Construction")
                choice = input()
                if choice == '1':
                    project_type = self.project_type[0]
                elif choice == '2':
                    project_type = self.project_type[1]
                elif choice == '3':
                    project_type = self.project_type[2]
                else:
                    print("Invalid Choice.")
                    return False
                name = (input("Enter Updated Name or Enter to continue ") or row[1])
                if not name.isalpha():
                    print("\tInvalid data format. Name should contain only alphabets.")
                    return False
                area = (input("Enter Updated Area or Enter to continue ") or row[2])
                if not area.isalpha():
                    print("\tInvalid data format. Area should contain only alphabets.")
                    return False
                total_members = int(input("Enter Updated TotalMembers or Enter to continue ") or row[3])
                cost_estimate = int(input("Enter Updated CostEstimate or Enter to continue ") or row[4])
                start_date = (input("Enter Updated StartDate or Enter to continue ") or row[5])
                if InputValidations.validate_date(start_date):
                    end_date = (input("Enter Updated EndDate or Enter to continue ") or row[6])
                    if InputValidations.validate_date(end_date) and InputValidations.validate_end_date(start_date,
                                                                                                       end_date):

                        self.query.update_project(project_type, name, area, total_members, cost_estimate, start_date, end_date,
                                             project_id)
                        print("Record Updated Successfully")
                        row = self.get_project_by_id(project_id)
                        return True

        except ValueError:
            print("Invalid Input. Please try again.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def delete_project(self):
        """
        Delete Project.
        :param conn:
        :param project_id:
        :return:
        """
        try:
            project_id = int(input("Enter Project Id "))
            record = self.get_project_by_id(project_id)
            if record:
                confirm = input("Do you wish to continue (y/n):")
                if confirm.lower() == 'y':
                    self.query.delete_project(project_id)
                    print("Project Deleted")
                    return True
                else:
                    return False

        except ValueError:
            print("Invalid Input")
            return False
        except:
            print("Some Error occured. Please try again.")
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

    def show_project_approval_requests(self):
        """
        Show status of all project assignment approval requests
        :param conn:
        :param bdo_id:
        :return: status of all project assignment approval requests
        """
        try:
            records = self.query.show_project_approval_requests(self.bdo_id)
            if records:
                for row in records:
                    if row[4] == 1:
                        approval = "Accepted"
                    else:
                        approval = "Rejected"
                    print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tApprovalStatus: {}
                                           '''.format(row[0], row[1], row[2], row[3], approval))
                return True
            else:
                print("No Report. Approve Requests from  Pending Requests Section.")
                return False
        except:
            print("Some error occurred. Please try again.")
            return False

    def show_project_approval_pending_requests(self):
        """
        Show pending project assignment approval requests
        :param conn:
        :param bdo_id:
        :return: all pending project assignment approval requests
        """
        try:
            records = self.query.show_project_approval_pending_requests(self.bdo_id)
            if records:
                for row in records:
                    approval = "Pending"
                    print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tApprovalStatus: {}
                        '''.format(row[0], row[1], row[2], row[3], approval))
                wish = input("Do you wish to Approve/Reject Requests (y/n): ")
                if wish.lower() == 'y':
                    id = int(input("Enter Id of the request you want to Approve/Reject: "))
                    option = int(input("1. Accept\t2. Reject.\nSelect your option. "))
                    if option == 1:
                        approval = 1
                    elif option == 2:
                        approval = 2
                    else:
                        print("Invalid input")
                        return False
                    self.approve_project_assignment(approval, id)
                    if approval == 1:
                        self.query.update_project_member_attendance(id)
                        self.query.update_project_member_wage(id)
                elif wish.lower() == 'n':
                    return False
                else:
                    print("invalid input")
                    return False
                return True
            else:
                print("No Pending Requests.")
                return False
        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some Error occured. Please try again.")
            return False

    def approve_project_assignment(self, status, project_member_id):
        """
        Approve/Reject Project Assignment.
        :param conn:
        :param status:
        :param project_member_id:
        :return:
        """
        if self.query.approve_project_assignment(status, project_member_id):
            print("Action Successful.")
            return True
        else:
            print("Action Unsuccessful. Please try again.")
            return False

    def show_wage_approval_requests(self):
        """
           Show all wage approval requests status.
           :param conn:
           :param bdo_id:
           :return: wage approval requests status.
        """
        try:
            records = self.query.show_wage_approval_requests(self.bdo_id)
            if records:
                for row in records:
                    if row[7] == 1:
                        approval = "Accepted"
                    else:
                        approval = "Rejected"
                    print('''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tTotal Working Days: {}\tWage: {}\tAttendance: {}\tApproval: {}
                            '''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], approval))
                return True
            else:
                print("No Report. Approve Requests from  Pending Wage Requests Section.")
                return False
        except:
            print("Some error occurred. Please try again.")
            return False

    def show_wage_approval_pending_requests(self):
        """
        Show pending wage approval requests status.
        :param conn:
        :param bdo_id:
        :return: pending wage approval requests status.
        """
        try:
            records = self.query.show_wage_approval_pending_requests(self.bdo_id)
            if records:
                for row in records:
                    wage_approval = "Pending"
                    print(
                        '''Id: {}\tGPM Name: {}\tProjectName: {}\tMemberName: {}\tTotal Working Days: {}\tWage: {}\tAttendance: {}\tApproval: {}'''.format(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], wage_approval))

                wish = str(input("Do you wish to Approve/Reject Requests (y/n): "))
                if wish.lower() == 'y':
                    id = int(input("Enter Id of the request you want to Approve/Reject: "))
                    option = int(input("1. Accept\t2. Reject.\nSelect your option. "))
                    if option == 1:
                        approval = 1
                    elif option == 2:
                        approval = 2
                    else:
                        print("Invalid input")
                        return False
                    self.approve_wage(approval, id)
                elif wish.lower() == 'n':
                    return False
                else:
                    print("invalid input")
                    return False
                return True
            else:
                print("No Pending Requests.")
                return False
        except ValueError:
            print("Invalid Input.")
            return False
        except:
            print("Some error occurred. Please try again.")
            return False

    def approve_wage(self, status, project_member_id):
        """
        Approve Wage.
        :param conn:
        :param status:
        :param project_member_id:
        :return:
        """
        if self.query.approve_wage(status, project_member_id):
            print("Action Successful.")
            return True
        else:
            print("Action UnSuccessful.")
            return False

    def view_complaints(self):
        """
        View complaints.
        :param conn:
        :param bdo_id:
        :return:
        """
        try:
            records = self.query.view_complaints(self.bdo_id)
            if records:
                for row in records:
                    print('''\tMemberId: {}\tGpmId: {}\tIssue: {}
                     '''.format(row[0], row[1], row[2]))
                return False
            else:
                print("No Complaints received.")
                return False
        except:
            print("Some error occurred. Please try again.")
            return False

    def show_member_details(self):
        """
        Display details of all Members under a particular GPM.
        :param conn:
        :param gpm_id:
        :return:
        """
        try:
            records = self.query.show_member_details(self.bdo_id)
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

    def show_project_member_details(self):
        """
        Show details of all project Members.
        :param conn:
        :param gpm_id:
        :return:
        """

        records = self.query.show_project_member_details(self.bdo_id)
        if records:
            for row in records:
                print('''\tProject Id: {} \n\tProject Name: {} \n\tMember Id: {} \n\tMemberName: {}\n\tArea: {}\n\tPincode: {}\n \tAge: {}\n\tTotal Working Days: {} \n\tWage: {} \n\tAttendance: {}
                        '''.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            return True
        else:
            print("No records found.")
            return False

from getpass import getpass

from src import MemberRepository, Main


class member:
    def __init__(self):
        self.bdo_id = None
        self.gpm_id = None
        self.member_id = None
        self.query = MemberRepository.MemberQuery()

    def member_login(self):
        """
        Member login.
        :return:
        """
        try:
            email = str(input("\tEnter Email Id: "))
            record = self.query.login(email)
            if record:
                if record[1] is None:
                    password = getpass('\tFirst Time Login. Please set your password: ')
                    self.query.update_password(password, record[4])
                    self.bdo_id = record[2]
                    self.gpm_id = record[3]
                    self.member_id = record[4]
                    return True
                else:
                    password = getpass('\tEnter Password: ')
                    if record[1] == password:
                        print("\tAuthentication Successful")
                        self.bdo_id = record[2]
                        self.gpm_id = record[3]
                        self.member_id = record[4]
                        return True
                    else:
                        print("\tAuthentication failed. Please check your credentials")
                        return False
            else:
                print("\tUser does not exist")
                return False
        except:
            print("Some Error occurred. Please try again.")
            return False

    def show_member_details(self):
        """
        View member details
        :return:
        """
        try:
            record = self.query.show_member_details(self.member_id)
            print('''\tName: {}\tEmail: {}\tAge: {}\tGender: {}\tPlace: {}\tAddress: {}\tWage: {}
                        '''.format(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
            return True
        except:
            print("Some Error occurred. Please try again.")
            return False

    def file_complaint(self):
        """
        File complaint regarding your issue to Gpm/Bdo.
        :return:
        """
        try:
            issue = input("\tEnter your Issue: ")
            if self.query.file_complaint(self.bdo_id, self.gpm_id, self.member_id, issue):
                print("Complaint Filed. Complaint Id: ")
                return True
            else:
                print("Could not file complaint. Please try again.")
                return False
        except:
            print("Some Error occurred. Please try again.")
            return False

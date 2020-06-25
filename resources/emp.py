from flask_restful import Resource,reqparse
from db import query
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required

class Profile(Resource):
    @jwt_required
    def get(self):
        try:
            return query("""SELECT * FROM project.profile""")
        except:
            return {"message":"There was an error connecting to profile table."},500

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('stuid',type=int,required=True,help="student id cannot be left blank!")
        parser.add_argument('name',type=str,required=True,help="name cannot be left blank!")
        parser.add_argument('branch',type=str,required=True,help="branch cannot be left blank!")
        parser.add_argument('year',type=int,required=True,help="year cannot be left blank!")
        parser.add_argument('grade',type=float,required=True,help="grade cannot be left blank!")
        parser.add_argument('cactivities',type=str,required=True,help="cactivities cannot be left blank!")
        parser.add_argument('hobbies',type=int,required=True,help="Hobbies cannot be left blank!")
        parser.add_argument('phoneno',type=int,required=True,help="phonenp cannot be left blank!")
        parser.add_argument('emailid',type=str,required=True,help="emailid cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""INSERT INTO project.profile (stuid,name,branch,year,grade,cactivities,hobbies,phoenno,emailid)
                                                    VALUES({data['stuid']},
                                                        '{data['name']}',
                                                        '{data['branch']}',
                                                        {data['year']},
                                                        '{data['grade']}',
                                                        '{data['cactivities']}',
                                                        '{data['hobbies']}',
                                                        '{data['phoenno']}',
                                                        '{data['emailid']}')""")
        except:
            return {"message":"There was an error inserting into profile table."},500

        return {"message":"Successfully Inserted."},201

class Changepassword(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse-args()
        try:
            query(f"""update table admin set password='{data['password']}' where username='{data['username']}'""")
        except:
            return {"message":"Updation of password is not successful"}
        return {"password updated successfully"}

class superadmin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse-args()

        try:
            query(f"""insert into superadmin values('{data['username']}','{data['password']}')""")
        except:
            return {"Insertion into super admin table has falied"}
        return {"message":"Insertion is succesful in to super admin table"}

class Addclub(Resource):
    @jwt_required
    def get(self):
        try:
            return query("""SELECT * FROM project.admin""")
        except:
            return {"message":"There was an error connecting to admin table."},500

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('uid',type=int,required=True,help="id cannot be left blank!")
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()

        try:

            query(f"""INSERT INTO admin (uid,username,password,clubname)
                                                    VALUES('{data['uid']}','{data['username']}',
                                                        '{data['password']}','{data['clubname']}')""")


        except:

            return {"message":"There was an error inserting into admin table,bcoz the user has not registered in superadmin"},500

        try:

            query(f"""create table {data['clubname']} (clubid int primary key auto_increment,stuid int,eventname varchar(40),eventdate date)""")

        except:

            return {"message":"There was an error in creating the club"},500

        return {"message":"Successfully Inserted and created."},201

class Addclubmembers(Resource):
    #@jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubid',type=int,required=False,help="id can be left blank!")
        parser.add_argument('stuid',type=int,required=True,help="student id cannot be left blank!")
        parser.add_argument('eventname',type=str,required=True,help="eventname cannot be left blank!")
        parser.add_argument('eventdate',type=str,required=True,help="eventdate cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""insert into cosc (clubid,stuid,eventname,eventdate) values('{data['clubid']}','{data['stuid']}','{data['eventname']}','{data['eventdate']}')""")
        except:
            return "error inserting into the respective club"
        return {"inserted data in to club succesfully"}

class Allclubdetails(Resource):
    def get(self):
        try:
            query("""select * from student""")
        except:
            return {"message":"Unable to fetch all club details"}
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('cid',type=int,required=False,help="id can be left blank!")
        parser.add_argument('stuid',type=int,required=True,help="student id cannot be left blank!")
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        parser.add_argument('clubroel',type=str,required=True,help="club role cannot be left blank!")
        data=parser.parse_args()
        try:
            query(f"""insert into student (cid,stuid,clubname,clubrole) values('{data['cid']}','{data['stuid']}','{data['clubname']}','{data['clubrole']}')""")
        except:
            return {"Unable to insert in to student club table"}
        return {"Succefully inserted into student table"}


class Adminlogin(Resource):
    @jwt_required
    def get(self):
        try:
            return query("""SELECT * FROM project.admin""")
        except:
            return {"message":"There was an error connecting to admin table."},500

    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('uid',type=int,required=True,help="id cannot be left blank!")
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()

        try:
            query(f"""INSERT INTO project.admin (uid,username,password,clubname)
                                                    VALUES('{data['uid']}','{data['username']}',
                                                        '{data['password']}','{data['clubname']}')""")
        except:
            return {"message":"There was an error inserting into admin table,bcoz the user has not registered in superadmin"},500

        try:
            query(f"""create table {data['clubname']} (clubid int primary key auto_increment,stuid int,eventname varchar(40),eventdate date)""")
        except:
            return {"message":"There was an error in creating the club"},500
        return {"message":"Successfully Inserted and created."},201

class Clubdelete(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        data=parser.parse_args()

        try:

            clubname=query(f"""select clubname from admin where username='{data['username']}'""",return_json=False)
            cname=clubname[0]['clubname']

            query(f"""delete from admin where username='{data['username']}'""")

            query("drop table if exists {}".format(cname))

            return {"message":"deleted"}
        except:
            return {"message":"tables are not deleted"},500
class Clubnames(Resource):
    #@jwt_required
    def get(self):
        try:
            return query(f"""select clubname from admin""")
        except:
            return {"message":"Unable to fetch club names"}
class Clubmembers(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('clubname',type=str,required=True,help="clubname cannot be left blank!")
        data=parser.parse_args()
        clubname = data['clubname']
        try:

            return query(f"""select p.stuid,p.name,p.branch,s.crole from profile p,student s
             where s.clubname='{clubname}' and p.stuid=s.stuid and s.acceptstatus=1""")

        except:
            return {"message":"club members not returned"},500

class User():
    def __init__(self,username,password):
        self.username=username
        self.password=password

    @classmethod
    def getUserByUsername(cls,username):
        result=query(f"""SELECT username,password FROM superadmin WHERE username='{username}'""",return_json=False)
        if len(result)>0: return User(result[0]['username'],result[0]['password'])
        return None

    @classmethod
    def getAdminbyUserid(cls,username):
        result=query(f"""SELECT uid,password FROM admin WHERE uid='{username}'""",return_json=False)
        if len(result)>0: return User(result[0]['uid'],result[0]['password'])
        return None

class Login(Resource):

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="username cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        user=User.getUserByUsername(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.username,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401

class Adminlog(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userid',type=int,required=True,help="userid cannot be left blank!")
        parser.add_argument('password',type=str,required=True,help="password cannot be left blank!")
        data=parser.parse_args()
        user=User.getAdminbyUserid(data['userid'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.username,expires_delta=False)
            return {'access_token':access_token},200
        return {"message":"Invalid Credentials!"}, 401
class ForgetPassword(Resource):
    @jwt_required
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('userid',type=int,required=True,help="userid name cannot be left blank!")
        parser.add_argument('otp',type=str,required=True,help="OTP not assigned")
        data=parser.parse_args()
        adminid = data['userid']
        otp=data['otp']
        try:
            result=query(f"""select emailid from project.profile where stuid={adminid} """,return_json=False)
            query(f""" insert into email (stuid,emailid,pin) values ({adminid},'{result[0]['emailid']}','{otp}')""")
            return result
        except:
            return {"message":"No entry with the given studentid "},500

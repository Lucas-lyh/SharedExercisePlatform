from peewee import *
import pymysql
import datetime
db = MySQLDatabase("testdatabase", user='root', password='buaa2023', host='43.143.129.27',
                           port=3306)


class User(Model):
    '''记录用户'''
    id = AutoField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = db
    
class UserGroup(Model):
    '''记录一个用户组'''
    id = AutoField(primary_key=True)
    group_name = CharField(unique=True)
    creator_id = ForeignKeyField(User)
    administrator_id = ForeignKeyField(User, default=creator_id)

    class Meta:
        database = db
        table_name = 'user_group'

class Question(Model):
    '''记录一个问题'''
    id = AutoField(primary_key=True)
    creator_id = ForeignKeyField(User)
    content = TextField()

    class Meta:
        database = db

class QuestionGroup(Model):
    '''记录一个问题组'''
    id = AutoField(primary_key=True)
    group_name = CharField(unique=True)
    creator_id = ForeignKeyField(User)
    is_public = BooleanField(default=True)

    class Meta:
        database = db
        table_name = 'question_group'

class SolutionHistory(Model):
    '''记录一条用户的做题记录'''
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(User)
    question_id = ForeignKeyField(Question)
    time = TimestampField()
    score = FloatField()
    user_answer = TextField()

    class Meta:
        database = db
        table_name = 'solution_history'

class ReUserToGroup(Model):
    '''记录用户与用户组的所属关系'''
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(User)
    group_id = ForeignKeyField(UserGroup)
    class Meta:
        database = db
        table_name = 're_user_to_group'
        constraints = [SQL('UNIQUE(user_id, group_id)')]

class ReQuestionToGroup(Model):
    '''记录问题与问题组的所属关系'''
    id = AutoField(primary_key=True)
    question_id = ForeignKeyField(Question)
    group_id = ForeignKeyField(QuestionGroup)
    class Meta:
        database = db
        table_name = 're_question_to_group'
        constraints = [SQL('UNIQUE(question_id, group_id)')]

class QuestionGroupPerm(Model):
    '''记录问题组的权限'''
    id = AutoField(primary_key=True)
    user_group_id = ForeignKeyField(UserGroup)
    question_group_id = ForeignKeyField(QuestionGroup)
    class Meta:
        database = db
        table_name = 'question_group_perm'
        constraints = [SQL('UNIQUE(user_group_id, question_group_id)')]

class Manager:
    def try_login(self, username, pwhash):
        users = User.select().where(User.username == username)
        if len(users) == 0:
            return False
        return users[0].password == pwhash
    
    def try_register(self, username, pwhash):
        users = User.select().where(User.username == username)
        if len(users) !=0:
            return False
        new_user = User(username = username, password = pwhash)
        new_user.save()
        return True
    
    def select_allowed_questiongroup_by_user(self, username):
        '''
        根据用户名，查看对用户可见的问题组
        返回值为一个列表，列表中每个元素都有四个类变量，与QuestionGroup相同
        '''
        result = (QuestionGroup
            .select(QuestionGroup.id, QuestionGroup.group_name, QuestionGroup.creator_id, QuestionGroup.is_public)
            .join(QuestionGroupPerm, on=(QuestionGroupPerm.question_group_id == QuestionGroup.id))
            .join(UserGroup, on=(QuestionGroupPerm.user_group_id == UserGroup.id))
            .join(ReUserToGroup, on=(UserGroup.id == ReUserToGroup.group_id))
            .join(User, on=(ReUserToGroup.user_id == User.id))
            .where(User.username == username))
        print(result[0].creator_id)
        return result
    
    def select_allowed_questiongroup_by_usergroup(self, group_name):
        '''
        根据用户名，查看对某用户组可见的问题组
        返回值为一个列表，列表中每个元素都有四个类变量，与QuestionGroup相同
        '''
        result = (QuestionGroup
            .select(QuestionGroup.id, QuestionGroup.group_name, QuestionGroup.creator_id, QuestionGroup.is_public)
            .join(QuestionGroupPerm, on=(QuestionGroupPerm.question_group_id == QuestionGroup.id))
            .join(UserGroup, on=(QuestionGroupPerm.user_group_id == UserGroup.id))
            .where(UserGroup.group_name == group_name))
        print(result[0].group_name)
        return result
    
    

# User.create_table()
# user = User(username = "lucas", password = "buaa2023")
# user.save()
# all = User.get()
# all.delete_instance()

# db.create_tables([UserGroup, QuestionGroup, SolutionHistory, ReUserToGroup, ReQuestionToGroup, QuestionGroupPerm])
Manager().select_allowed_questiongroup_by_usergroup('测试用户组')

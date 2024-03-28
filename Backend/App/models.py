# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import db


# 用户信息表
class User(db.Model):
    __tablename__ = 'tb_user'
    user_id = db.Column(db.String(30), primary_key=True)  # 用户ID
    user_name = db.Column(db.String(30))
    user_tel = db.Column(db.String(30), unique=True)  # 唯一约束
    user_email = db.Column(db.String(30), unique=True)  # 唯一约束
    user_password = db.Column(db.String(30), nullable=False)  # 不为空值
    user_IP = db.Column(db.String(30))  # 用户IP
    user_iconUrl = db.Column(db.String(80))  # 用户头像Url
    user_authToken = db.Column(db.String(30))  # 用户密钥

    apiKeys = db.relationship('APIKey', backref='user', lazy='dynamic')

    def __str__(self):
        if self.user_tel:
            return f'id:{self.user_id}\tname:{self.user_name}\ttel:{self.user_tel}'
        if self.user_email:
            return f'id:{self.user_id}\tname:{self.user_name}\temail:{self.user_email}'


# # 用户好友关系表
class FriendShip(db.Model):
    __tablename__ = 'tb_friendship'
    fs_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 好友关系id值，自增
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id), nullable=False)  # 用户ID---外键
    friend_token = db.Column(db.String(30), nullable=False)  # 好友的token密钥
    friend_state = db.Column(db.Integer, default=0, nullable=False)  # 好友状态【0:未审核;1:同意;-1:拒绝】
    createTime = db.Column(db.DateTime, nullable=False)  # 好友创建的时间


# APIKey信息表
class APIKey(db.Model):
    __tablename__ = 'tb_APIKey'
    AK_id = db.Column(db.String(30), primary_key=True)
    AK_name = db.Column(db.String(30), nullable=False)  # 模型名称
    AK_value = db.Column(db.String(30), nullable=False)  # APIKey值
    AK_intro = db.Column(db.String(600), nullable=True)  # LLM的详细背景介绍
    # AK_auth = db.Column(db.String(30))  # 鉴权秘钥
    # AK_type = db.Column(db.String(30))  # APIKey类型
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键


# 数据集表
class DataSet(db.Model):
    __tablename__ = 'tb_DataSet'
    DS_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 数据集id
    DS_name = db.Column(db.String(30), nullable=True)  # 数据集名称
    DS_info = db.Column(db.String(200))  # 数据集描述
    DS_url = db.Column(db.String(80))  # 数据集文件存储url
    userid = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键


# 项目数据表
class Project(db.Model):
    __tablename__ = 'tb_Project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 项目id值，自增
    project_name = db.Column(db.String(80))  # 项目名称
    project_info = db.Column(db.String(200))  # 项目描述
    userId = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 用户ID---外键

    APIKeys = db.relationship('ProjectAPIKey', backref='projectAK', cascade='all, delete-orphan')  # 1:m=project:AK
    DataSets = db.relationship('ProjectDataSet', backref='projectDS', cascade='all, delete-orphan')  # 1:m=project:DS


# 项目--AK关联表
class ProjectAPIKey(db.Model):
    __tablename__ = 'tb_ProjectAPIKey'
    Project_APIKey_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Pid = db.Column(db.Integer, db.ForeignKey(Project.project_id))  # project项目---外键
    AKid = db.Column(db.String(30), db.ForeignKey(APIKey.AK_id, ondelete='CASCADE'))  # apiKey---外键


# 项目--数据集关联表
class ProjectDataSet(db.Model):
    __tablename__ = 'tb_ProjectDataSet'
    Project_DataSet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Pid = db.Column(db.Integer, db.ForeignKey(Project.project_id))  # project项目---外键
    DSid = db.Column(db.Integer, db.ForeignKey(DataSet.DS_id, ondelete='CASCADE'))  # 数据集---外键


# 用户测试实验信息
class TestProject(db.Model):
    __tablename__ = 'tb_TestProject'
    tP_id = db.Column(db.String(30), primary_key=True)  # 测试实验信息ID
    tP_name = db.Column(db.String(30))  # 实验名称
    tP_time = db.Column(db.DateTime)  # 测试时间
    tP_status = db.Column(db.Integer, default=0)  # 实验状态   【0:待实验、1:正在实验、2:待审核、3:已完成】
    tP_progress = db.Column(db.Float, default=0)  # 实验进度
    tP_configURL = db.Column(db.String(80))  # 实验配置文件Url
    Pid = db.Column(db.Integer, db.ForeignKey(Project.project_id))  # 项目ID---外键
    AK1 = db.Column(db.String(30), db.ForeignKey(APIKey.AK_id))  # APIKey1---外键
    AK2 = db.Column(db.String(30), db.ForeignKey(APIKey.AK_id))  # APIKey2---外键
    DS = db.Column(db.Integer, db.ForeignKey(DataSet.DS_id))  # 数据集---外键

    # 该实验下的协作者
    collaborators = db.relationship('TestProjectUser', backref='testProject', cascade='all, delete-orphan')


# 实验--协作者
class TestProjectUser(db.Model):
    __tablename__ = 'tb_TestProjectUser'
    tPU_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TPid = db.Column(db.String(30), db.ForeignKey(TestProject.tP_id, ondelete='CASCADE'))  # 实验ID---外键
    uid = db.Column(db.String(30), db.ForeignKey(User.user_id, ondelete='CASCADE'))  # 协助者-用户ID---外键


# 实验审核任务表
class QA(db.Model):
    __tablename__ = 'tb_QA'
    QA_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    QA_time = db.Column(db.DateTime)  # 审核时间
    QA_question = db.Column(db.String(80))  # 审核的问题
    QA_answer = db.Column(db.String(200))  # 审核的回答
    QA_score = db.Column(db.Float)  # 审核打分
    QA_thread = db.Column(db.Integer)  # 线程号
    QA_field = db.Column(db.String(80))  # 领域
    TPid = db.Column(db.String(30), db.ForeignKey(TestProject.tP_id))  # 实验ID---外键【ondelete='CASCADE'】
    uid = db.Column(db.String(30), db.ForeignKey(User.user_id))  # 审核人---外键

    def __str__(self):
        return f'Q:{self.QA_question}\tA:{self.QA_answer}\tthrad:{self.QA_thread}'

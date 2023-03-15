import json
import os
from flask import Flask, jsonify, request, url_for, render_template, redirect, flash, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from sqlalchemy import or_, and_
from sqlalchemy.sql import func, distinct, asc, desc
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:sa@dsn'
db = SQLAlchemy(app)

app.secret_key = 'abc'  # 设置表单交互密钥
login_manager = LoginManager()  # 实例化登录管理对象
login_manager.init_app(app)  # 初始化应用
login_manager.login_view = 'login'  # 设置用户登录视图函数 endpoint

USERS = [
    {
        "id": 1,
        "name": 'chen',
        "password": generate_password_hash('123')
    },
    {
        "id": 2,
        "name": 'you',
        "password": generate_password_hash('123')
    }
]


def create_user(username, password):
    """创建一个用户"""
    user = {
        "name": username,
        "password": generate_password_hash(password),
        "id": uuid.uuid4()
    }
    USERS.append(user)


def get_user(username):
    """根据用户名获得用户记录"""
    for user in USERS:
        if user.get("name") == username:
            return user
    return None


class User(UserMixin):
    """用户类"""

    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None


@login_manager.user_loader  # 定义获取登录用户的方法
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=('GET', 'POST'))  # 登录
def login():
    if request.method == "POST":
        emsg = None
        user_name = request.form.get('username')
        password = request.form.get("password")
        user_info = get_user(user_name)  # 从用户数据中查找用户记录
        if user_info is None:
            emsg = "用户名或密码密码有误"
        else:
            user = User(user_info)  # 创建用户实体
            if user.verify_password(password):  # 校验密码
                login_user(user)  # 创建用户 Session
                return redirect(request.args.get('next') or url_for('index'))
            else:
                emsg = "用户名或密码有误"
        return render_template('login.html', emsg=emsg)
    else:
        return render_template('login.html')


@app.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


class jxjhb(db.Model):
    __tablename__ = "jxjhb"
    sxh = db.Column(db.Integer)
    xydm = db.Column(db.String(5), primary_key=True)
    zydm = db.Column(db.String(5), primary_key=True)
    rxsj = db.Column(db.String(20), primary_key=True)
    jxxsdm = db.Column(db.String(5), primary_key=True)
    kcdm = db.Column(db.String(10), primary_key=True)
    skxq = db.Column(db.Integer)
    ksxq = db.Column(db.Integer)
    xf = db.Column(db.DECIMAL(5,1))
    jxzxs = db.Column(db.Float)
    jszxs = db.Column(db.Float)
    syzxs = db.Column(db.Float)
    jxzhouxs = db.Column(db.Float)
    jszhouxs = db.Column(db.Float)
    syzhouxs = db.Column(db.Float)



class xsb(db.Model):
    __tablename__ = "xsb"
    xh = db.Column(db.String(12), primary_key=True)
    xm = db.Column(db.String(50))
    xb = db.Column(db.String(2))
    bjdm = db.Column(db.String(10))
    xnbjdm = db.Column(db.String(10))
    xydm = db.Column(db.String(5))
    zydm = db.Column(db.String(15))


class zyb(db.Model):
    __tablename__ = "zyb"
    sxh = db.Column(db.Integer)
    xydm = db.Column(db.String(5), primary_key=True)
    zydm = db.Column(db.String(15), primary_key=True)
    zyqc = db.Column(db.String(50))
    zyjc = db.Column(db.String(50))


class bjb(db.Model):
    __tablename__ = "bjb"
    bjdm = db.Column(db.String(10), primary_key=True)
    bjjc = db.Column(db.String(100))
    bjqc = db.Column(db.String(100))
    xydm = db.Column(db.String(5))
    zydm = db.Column(db.String(15))
    rxsj = db.Column(db.String(20))
    b_zyjc = db.Column(db.String(50))


class jxrwb(db.Model):
    __tablename__ = "jxrwb"
    sxh = db.Column(db.Integer, primary_key=True)
    xqbs = db.Column(db.String(6))
    xydm = db.Column(db.String(5))
    xyjc = db.Column(db.String(80))
    zydm = db.Column(db.String(15))
    zyjc = db.Column(db.String(50))
    bjdm = db.Column(db.String(10))
    bjjc = db.Column(db.String(100))
    rxsj = db.Column(db.String(20))
    skxq = db.Column(db.Integer)
    kcdm = db.Column(db.String(10))
    kcjc = db.Column(db.String(50))
    tName = db.Column(db.String(50))
    ksz=db.Column(db.Integer)
    jsz=db.Column(db.Integer)
    xkrl=db.Column(db.Integer)
    zyptdm=db.Column(db.String(5))
    zyptmc= db.Column(db.String(50))

class pkkb(db.Model):
    __tablename__="pkkb"
    sxh=db.Column(db.Integer, primary_key=True)
    xqbs=db.Column(db.String(6))
    bjdm = db.Column(db.String(10))
    jxrwId = db.Column(db.String(50))
    kcdm = db.Column(db.String(10))
    skxq = db.Column(db.Integer)
    qsjc = db.Column(db.Integer)
    jsjc = db.Column(db.Integer)
    zxz = db.Column(db.Integer)
    jsdm = db.Column(db.String(10))
    skdd = db.Column(db.String(50))
    jxrwsxh= db.Column(db.Integer)
    kcmc = db.Column(db.String(100))
    ksz = db.Column(db.Integer)
    jsz = db.Column(db.Integer)

class jsb(db.Model):
    __tablename__ = "jsb"
    jsdm = db.Column(db.String(10), primary_key=True)
    jxldm = db.Column(db.String(10))
    jsjc = db.Column(db.String(50))
    jsqc = db.Column(db.String(50))
    jslxdm = db.Column(db.String(1))

class jxlb(db.Model):
    __tablename__ = "jxlb"
    jxldm = db.Column(db.String(10), primary_key=True)
    jxljc = db.Column(db.String(16))

class xyb(db.Model):
    __tablename__="xyb"
    xydm=db.Column(db.String(5), primary_key=True)
    xyjc=db.Column(db.String(80))
    xyqc=db.Column(db.String(80))
    xywmc=db.Column(db.String(80))
    xyywjc=db.Column(db.String(80))
    xiaoqudm=db.Column(db.String(6))
    sjxydm=db.Column(db.String(5))

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html", username=current_user.username)


@app.route("/index", methods=['GET', 'POST'])
@login_required
def index_red():
    return redirect(url_for("index"))


@app.route("/jxjhb_form", methods=['GET', 'POST'])
@login_required
def jxjhb_form():
    return render_template("jxjhb_form.html", username=current_user.username, jxjhb=jxjhb.query.limit(200))


@app.route("/xsb_form", methods=['GET', 'POST'])
@login_required
def xsb_form():
    if request.method == "POST":
        xh = request.form.get('xh')  # 需要查询的内容
        xm = request.form.get('xm')
        return render_template("xsb_form.html", username=current_user.username,
                               xsb=xsb.query.filter(xsb.xh.like("%" + xh + "%"), xsb.xm.like("%" + xm + "%")).limit(
                                   200), xh=xh, xm=xm)
    return render_template("xsb_form.html", username=current_user.username, xsb=xsb.query.limit(200))


@app.route("/zyb_form", methods=['GET', 'POST'])
@login_required
def zyb_form():
    return render_template("zyb_form.html", username=current_user.username, zyb=zyb.query.limit(200))


@app.route("/bjb_form", methods=['GET', 'POST'])
@login_required
def bjb_form():
    return render_template("bjb_form.html", username=current_user.username, bjb=bjb.query.limit(200))


@app.route("/jxrwb_form", methods=['GET', 'POST'])
@login_required
def jxrwb_form():
    return render_template("jxrwb_form.html", username=current_user.username, jxrwb=jxrwb.query.limit(200))


class course_info:
    name=""
    time=""
    location=""
    teacher=""
    fre=""

    def __init__(self,name,time,loc,tea,f):
        self.name=name
        self.time=time
        self.location=loc
        self.teacher=tea
        if f==0:
            fre=""
        elif f==1:
            fre="单"
        elif f==2:
            fre="双"


global kcb,title
kcb = [["8:00-8:50", "", "", "", "", "", "", ""],
       ["9:00-9:50", "", "", "", "", "", "", ""],
       ["10:10-11:00", "", "", "", "", "", "", ""],
       ["11:10-12:00", "", "", "", "", "", "", ""],
       ["13:30-14:20", "", "", "", "", "", "", ""],
       ["14:30-15:20", "", "", "", "", "", "", ""],
       ["15:40-16:30", "", "", "", "", "", "", ""],
       ["16:40-17:30", "", "", "", "", "", "", ""],
       ["18:30-19:20", "", "", "", "", "", "", ""],
       ["19:30-20:20", "", "", "", "", "", "", ""],
       ["20:30-21:20", "", "", "", "", "", "", ""]]
title=""

@app.route("/kcb_form", methods=['GET', 'POST'])
@login_required
def kcb_form():
    global kcb,title

    rxsj_list = db.session.query(distinct(jxrwb.rxsj)).order_by(asc(jxrwb.rxsj)).all()
    rxsj_p = p_query(rxsj_list)

    clas = []

    if request.method == "POST":

        submit = request.form.get("search")
        if submit == "查找班级":
            rxsj = eval(request.form.get("rxsj"))
            clas = bjb.query.filter(bjb.rxsj.like(rxsj)).all()
            sem_list=[str(rxsj)+"-1", str(rxsj)+"-2" ,str(rxsj+1)+"-1", str(rxsj+1)+"-2",str(rxsj+2)+"-1", str(rxsj+2)+"-2",str(rxsj+3)+"-1", str(rxsj+3)+"-2"]

            return render_template("kcb_form.html", username=current_user.username, sem_list=list(sem_list), clas_list=clas,
                                   rxsj_list=rxsj_p, sem="", bjb="", kcb=kcb)

        submit = request.form.get("confirm")
        if submit == "确定":
            sem = request.form.get("sem")
            bjdm=str(request.form.get("clas"))
            pkkb_q=pkkb.query.filter(pkkb.bjdm.like(bjdm), pkkb.xqbs.like(sem)).all()



            for r in pkkb_q:
                name=r.kcmc
                time=str(r.ksz)+"-"+str(r.jsz)+"周"
                jxldm=jsb.query.filter(jsb.jsdm.like(r.jsdm)).first().jxldm
                jsjc=jsb.query.filter(jsb.jsdm.like(r.jsdm)).first().jsjc
                loc=jsjc
                tea=jxrwb.query.filter(jxrwb.bjdm.like(bjdm), jxrwb.kcdm.like(r.kcdm)).first().tName
                fre=r.zxz
                kc=course_info(name, time, loc, tea, fre)
                for i in range(r.qsjc-1,r.jsjc):
                    kcb[i][r.skxq]=kc


            title=sem+"学期"+bjb.query.filter(bjb.bjdm.like(bjdm)).first().bjjc+"课程表"
            return render_template("kcb_form.html", username=current_user.username, sem_list=[], clas_list=clas,
                                   rxsj_list=rxsj_p, jxrwb=jxrwb.query.filter(jxrwb.bjdm.like(bjdm),
                                    jxrwb.xqbs.like(sem)).all(), title=title, kcb=kcb, bjb=bjb.query.filter(bjb.bjdm.like(bjdm)).first())




    return render_template("kcb_form.html", username=current_user.username, sem_list=[], clas_list=clas, rxsj_list=rxsj_p, sem="", bjb="", kcb=kcb, title=title)


imp_y = 0

def p_query(l):
    l_p=[]
    for i in l:
        i1 = str(i)
        i2 = i1.lstrip("('")
        i3 = i2.rstrip("'),")
        l_p.append(i3)
    return l_p


@app.route("/generate_jxjhb", methods=['GET', 'POST'])
@login_required
def generate_jxjhb():
    if request.method == "POST":
        submit = request.form.get("generate")
        if submit == "生成":
            imp_y = request.form.get("imp_y")
            t_y = request.form.get("target_y")
            t_jxjhb = jxjhb.query.filter(jxjhb.rxsj.like(imp_y))
            return render_template("generate_jxjhb.html", username=current_user.username, jxjhb=t_jxjhb)
        submit = request.form.get("save")
        if submit == "保存":
            imp_y = request.form.get("imp_y")
            t_jxjhb = jxjhb.query.filter(jxjhb.rxsj.like(imp_y))
            sxh_list = []
            for record in t_jxjhb:
                sxh_list.append(record.sxh)
            for num in sxh_list:

                xydm = request.form.get("xydm_" + str(num))
                zydm = request.form.get("zydm_" + str(num))
                rxsj = request.form.get("rxsj_" + str(num))
                jxxsdm = request.form.get("jxxsdm_" + str(num))
                kcdm = request.form.get("kcdm_" + str(num))
                skxq = request.form.get("skxq_" + str(num))
                ksxq = request.form.get("ksxq_" + str(num))
                s_jxjhb = jxjhb(xydm=xydm, zydm=zydm, rxsj=rxsj, jxxsdm=jxxsdm,
                                kcdm=kcdm, skxq=skxq, ksxq=ksxq)
                try:
                    db.session.add(s_jxjhb)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    flash("添加失败")
            return render_template("generate_jxjhb.html", username=current_user.username)

    return render_template("generate_jxjhb.html", username=current_user.username)

global xqbs, zyqc_list, zy_dict, jxrw_dict
xqbs=""
zyqc_list, zy_dict, jxrw_dict={}, {}, {}


@app.route("/generate_jxrwb", methods=['GET', 'POST'])
@login_required
def generate_jxrwb():
    global xqbs, zyqc_list, zy_dict, jxrw_dict
    xqbs_q = db.session.query(distinct(jxrwb.xqbs)).all()
    sem_list = p_query(xqbs_q)


    if request.method == 'POST':
        submit = request.form.get("query")
        if submit=="确定":
            xqbs=request.form.get("xqbs")
            jxrwb_q=db.session.query(distinct(jxrwb.zydm)).filter(jxrwb.xqbs==xqbs).all()
            zydm_list, zyqc_list=[], []
            for i in jxrwb_q:
                zydm=i[0]
                zydm_list.append(i[0])
                zyqc=zyb.query.filter(zyb.zydm==zydm).first().zyqc
                zyqc_list.append(zyqc)
            zy_dict={}
            jxrw_dict={}
            for zydm in zydm_list:
                jxrwb_q=db.session.query(distinct(jxrwb.rxsj)).filter(jxrwb.zydm==zydm, jxrwb.xqbs==xqbs).all()
                rxsj_list=p_query(jxrwb_q)
                zyqc=zyb.query.filter(zyb.zydm==zydm).first().zyqc
                bjb_q=bjb.query.filter(bjb.zydm==zydm, bjb.rxsj.in_(rxsj_list)).all()
                zy_dict[zyqc]=bjb_q
                for bj in bjb_q:
                    jxrwb_q=jxrwb.query.filter(jxrwb.xqbs==xqbs, jxrwb.bjdm==bj.bjdm).all()
                    jxrw_dict[bj.bjdm]=jxrwb_q
            return render_template("generate_jxrwb.html", username=current_user.username, sem_list=sem_list,
                                   zyqc_list=zyqc_list, zy_dict=zy_dict, jxrw_dict=jxrw_dict, xqbs=xqbs)

        submit = request.form.get("delete")
        if submit=="删除选定项":
            jxrw_list=request.form.getlist("jxrw")
            for sxh in jxrw_list:
                print(sxh)
                db.session.query(jxrwb).filter(jxrwb.sxh==sxh).delete()
            db.session.commit()
            jxrwb_q = db.session.query(distinct(jxrwb.zydm)).filter(jxrwb.xqbs == xqbs).all()
            zydm_list, zyqc_list = [], []
            for i in jxrwb_q:
                zydm = i[0]
                zydm_list.append(i[0])
                zyqc = zyb.query.filter(zyb.zydm == zydm).first().zyqc
                zyqc_list.append(zyqc)
            zy_dict = {}
            jxrw_dict = {}
            for zydm in zydm_list:
                jxrwb_q = db.session.query(distinct(jxrwb.rxsj)).filter(jxrwb.zydm == zydm, jxrwb.xqbs == xqbs).all()
                rxsj_list = p_query(jxrwb_q)
                zyqc = zyb.query.filter(zyb.zydm == zydm).first().zyqc
                bjb_q = bjb.query.filter(bjb.zydm == zydm, bjb.rxsj.in_(rxsj_list)).all()
                zy_dict[zyqc] = bjb_q
                for bj in bjb_q:
                    jxrwb_q = jxrwb.query.filter(jxrwb.xqbs == xqbs, jxrwb.bjdm == bj.bjdm).all()
                    jxrw_dict[bj.bjdm] = jxrwb_q
            return render_template("generate_jxrwb.html", username=current_user.username, sem_list=sem_list,
                                   zyqc_list=zyqc_list, zy_dict=zy_dict, jxrw_dict=jxrw_dict, xqbs=xqbs)

        submit=request.form.get("generate")
        if submit=="从教学计划生成":
            y=eval(xqbs[0:4])
            sem=eval(xqbs[5:6])
            t_y=[y, y-1, y-2, y-3]
            t_sem=[sem, sem+2, sem+4, sem+6]
            jxrwb_list = []
            for i in range(0, 4):
                t_jxjhb = jxjhb.query.filter(jxjhb.rxsj.like(t_y[i]), jxjhb.skxq.like(t_sem[0]))
                t_bjb = bjb.query.filter(bjb.rxsj.like(t_y[i]))

                for record in t_bjb:
                    t_jxjhb = jxjhb.query.filter(jxjhb.rxsj.like(t_y[i]), jxjhb.skxq.like(t_sem[0]),
                                                 jxjhb.xydm.like(record.xydm), jxjhb.zydm.like(record.zydm))
                    for c in t_jxjhb:
                        t_xyb=xyb.query.filter(xyb.xydm.like(c.xydm)).first()
                        t_jxrwb = jxrwb(xqbs=str(y) + "-" + str(sem), xydm=record.xydm, xyjc=t_xyb.xyjc, zydm=record.zydm, bjdm=record.bjdm,
                                        bjjc=record.bjjc, rxsj=t_y[i], skxq=t_sem[i], kcdm=c.kcdm)
                        jxrwb_list.append(t_jxrwb)

            try:
                db.session.add_all(jxrwb_list)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                flash("添加失败")
            jxrwb_q=db.session.query(distinct(jxrwb.zydm)).filter(jxrwb.xqbs==xqbs).all()
            zydm_list, zyqc_list=[], []
            for i in jxrwb_q:
                zydm=i[0]
                zydm_list.append(i[0])
                zyqc=zyb.query.filter(zyb.zydm==zydm).first().zyqc
                zyqc_list.append(zyqc)
            zy_dict={}
            jxrw_dict={}
            for zydm in zydm_list:
                jxrwb_q=db.session.query(distinct(jxrwb.rxsj)).filter(jxrwb.zydm==zydm, jxrwb.xqbs==xqbs).all()
                rxsj_list=p_query(jxrwb_q)
                zyqc=zyb.query.filter(zyb.zydm==zydm).first().zyqc
                bjb_q=bjb.query.filter(bjb.zydm==zydm, bjb.rxsj.in_(rxsj_list)).all()
                zy_dict[zyqc]=bjb_q
                for bj in bjb_q:
                    jxrwb_q=jxrwb.query.filter(jxrwb.xqbs==xqbs, jxrwb.bjdm==bj.bjdm).all()
                    jxrw_dict[bj.bjdm]=jxrwb_q

            return render_template("generate_jxrwb.html", username=current_user.username, sem_list=sem_list,
                                   zyqc_list=zyqc_list, zy_dict=zy_dict, jxrw_dict=jxrw_dict, xqbs=xqbs)

    return render_template("generate_jxrwb.html", username=current_user.username, sem_list=sem_list,
                           zyqc_list=zyqc_list, zy_dict=zy_dict, jxrw_dict=jxrw_dict, xqbs=xqbs)


global title2, kcb2, course, pkkb_q, rxsj, bjb_q, bjjc, pkkb_dict
rxsj=""
title2=""
kcb2 = [["8:00-8:50", "", "", "", "", "", "", ""],
       ["9:00-9:50", "", "", "", "", "", "", ""],
       ["10:10-11:00", "", "", "", "", "", "", ""],
       ["11:10-12:00", "", "", "", "", "", "", ""],
       ["13:30-14:20", "", "", "", "", "", "", ""],
       ["14:30-15:20", "", "", "", "", "", "", ""],
       ["15:40-16:30", "", "", "", "", "", "", ""],
       ["16:40-17:30", "", "", "", "", "", "", ""],
       ["18:30-19:20", "", "", "", "", "", "", ""],
       ["19:30-20:20", "", "", "", "", "", "", ""],
       ["20:30-21:20", "", "", "", "", "", "", ""]]
course=[]
pkkb_q=[]
bjjc=""
bjb_q=[]
pkkb_dict={}

@app.route("/schedule", methods=['GET', 'POST'])
@login_required
def schedule():
    xqbs_q = db.session.query(distinct(jxrwb.xqbs)).all()
    sem_list = p_query(xqbs_q)
    rxsj_list = db.session.query(distinct(jxrwb.rxsj)).order_by(asc(jxrwb.rxsj)).all()
    rxsj_p = p_query(rxsj_list)
    global title2, kcb2, course, pkkb_q, rxsj, xqbs, bjb_q, bjjc, pkkb_dict
    clas = []

    if request.method == "POST":
        submit1 = request.form.get("query1")
        if submit1 == "确定":
            xqbs=request.form.get("xqbs")
            jxrwb_q = db.session.query(distinct(jxrwb.bjdm)).filter(jxrwb.xqbs == xqbs).all()
            bjdm_list=p_query(jxrwb_q)
            bjb_q=bjb.query.filter(bjb.bjdm.in_(bjdm_list)).all()
            return render_template("schedule.html", username=current_user.username, xqbs=xqbs, sem_list=sem_list, clas_list=bjb_q, bjjc=bjjc,
                                   rxsj_list=rxsj_p, title=title, rxsj=rxsj, pkkb_dict=pkkb_dict)

        submit2 = request.form.get("query2")
        if submit2 == "确定":
            bjdm=str(request.form.get("bjdm"))
            bjjc=bjb.query.filter(bjb.bjdm.like(bjdm)).first().bjjc
            pkkb_q=pkkb.query.filter(pkkb.bjdm.like(bjdm), pkkb.xqbs.like(xqbs)).all()
            course=jxrwb.query.filter(jxrwb.bjdm.like(bjdm),
                                    jxrwb.xqbs.like(xqbs)).all()
            pkkb_dict={}
            for kc in course:
                pkkb_q2=pkkb.query.filter(pkkb.bjdm==bjdm, pkkb.xqbs==xqbs, pkkb.kcdm==kc.kcdm).all()
                pkkb_dict[kc.kcdm]=pkkb_q2


            kcb2 = [["8:00-8:50", "", "", "", "", "", "", ""],
                    ["9:00-9:50", "", "", "", "", "", "", ""],
                    ["10:10-11:00", "", "", "", "", "", "", ""],
                    ["11:10-12:00", "", "", "", "", "", "", ""],
                    ["13:30-14:20", "", "", "", "", "", "", ""],
                    ["14:30-15:20", "", "", "", "", "", "", ""],
                    ["15:40-16:30", "", "", "", "", "", "", ""],
                    ["16:40-17:30", "", "", "", "", "", "", ""],
                    ["18:30-19:20", "", "", "", "", "", "", ""],
                    ["19:30-20:20", "", "", "", "", "", "", ""],
                    ["20:30-21:20", "", "", "", "", "", "", ""]]

            for r in pkkb_q:
                name = r.kcmc
                time = str(r.ksz) + "-" + str(r.jsz) + "周"
                jsjc = jsb.query.filter(jsb.jsdm.like(r.jsdm)).first().jsjc
                loc = jsjc
                tea = jxrwb.query.filter(jxrwb.bjdm.like(bjdm), jxrwb.kcdm.like(r.kcdm)).first().tName
                fre = r.zxz
                kc = course_info(name, time, loc, tea, fre)
                for i in range(r.qsjc - 1, r.jsjc):
                    kcb2[i][r.skxq] = kc

            title2 = xqbs + "学期" + bjb.query.filter(bjb.bjdm.like(bjdm)).first().bjjc + "课程表"
            return render_template("schedule.html", username=current_user.username, sem_list=sem_list, xqbs=xqbs, clas_list=bjb_q, bjjc=bjjc,
                                   rxsj_list=rxsj_p, jxrwb=course, title=title2, kcb=kcb2, selected_course=pkkb_q, pkkb_dict=pkkb_dict)

        submit3=request.form.get("query3")



    return render_template("schedule.html", username=current_user.username, xqbs=xqbs, sem_list=sem_list, clas_list=bjb_q, bjjc=bjjc, rxsj_list=rxsj_p, title=title2, kcb=kcb2, jxrwb=course, selected_course=pkkb_q, rxsj=rxsj, pkkb_dict=pkkb_dict)


@app.route("/add_course", methods=["GET","POST"])
@login_required
def add_course():
    if request.method=="POST":
        skxq=request.form.get("skxq")
        qsjc=request.form.get("qsjc")
        jsjc=request.form.get("jsjc")
        fre=request.form.get("fre")
        pkkb_q=pkkb.query.filter(pkkb.xqbs==xqbs, pkkb.bjdm==bjdm, or_(pkkb.zxz==fre, pkkb.zxz==0), or_(and_(pkkb.qsjc<=qsjc, pkkb.jsjc>=jsjc), and_(pkkb.qsjc<=jsjc, pkkb.jsjc>=jsjc, pkkb.qsjc>qsjc), and_(pkkb.qsjc<=qsjc, pkkb.jsjc>=qsjc, pkkb.jsjc<jsjc))).all()
        not_available_teacher=[]
        for t in pkkb_q:
            not_available_teacher.append(jxrwb.query.filter(jxrwb.jxrwId==t.jxrwId).first().workNumber)
        teacher.query.filter(teacher.workNumber.notin_(not_available_teacher))



db.create_all()
app.run()

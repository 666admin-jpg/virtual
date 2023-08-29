#! /usr/bin/python3

from flask import Flask,url_for,render_template,redirect,request,flash
from pathlib import Path
import os
import sys
from markupsafe import escape
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import click


'''
使用： . .venv/bin/activate 启动虚拟环境
使用： deactivate           退出虚拟环境
使用： flask run --debug    运行代码
'''


app = Flask(__name__)



WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份



@app.context_processor
def inject_user():
    user = User.query.first()
    movies = Movie.query.all()
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dict(user=user, movies=movies, date=time_now)



@app.route('/', methods=['GET','POST'])     # 定义网站主页（默认页面）
def index():
    if request.method == 'POST':
        Name0 = request.form.get('name1')
        degree0 = request.form.get('degree1')
        if not Name0 or not degree0 or len(Name0) > 10 or len(degree0) > 2:
            flash('Invalid input.')
            return redirect(url_for('index'))
        degree = Movie(title=Name0,year=degree0)
        db.session.add(degree)
        db.session.commit()
        flash ('添加成功！')
        return redirect(url_for('index'))


    movies = Movie.query.all()
    return render_template('web.html')

@app.route('/<cmd>')    # 定义网站 /* 下任何内容
def hello(cmd):
    return render_template('practice.html', cmd=cmd)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST']) # 编辑内容
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        Name0 = request.form.get('name1')
        degree0 = request.form.get('degree1')

        if not Name0 or not degree0 or len(Name0) > 10 or len(degree0) > 2:
            flash ('修改失败！不允许输入过长的数值')
            return redirect(url_for('edit',movie_id=movie_id))
        
        movie.title = Name0
        movie.year = degree0
        db.session.commit()
        flash('修改成功！')
        return redirect(url_for('index'))

    Name2 = movie.title
    degree2 = movie.year
    return render_template('edit.html',movie=movie,name=Name2,degree=degree2)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('删除成功！')
    return redirect(url_for('index'))  # 重定向回主页


if __name__ == '__main__':
    app.run(port=5000,debug=True,host="127.0.0.1")















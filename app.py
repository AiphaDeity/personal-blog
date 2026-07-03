from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ----- 配置数据库 -----
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ----- 初始化数据库 -----
db = SQLAlchemy(app)

# ========================
# 📄 数据库模型：定义"文章"长什么样
# ========================
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)          # 文章编号，自动递增
    title = db.Column(db.String(100), nullable=False)     # 文章标题，不能为空
    content = db.Column(db.Text, nullable=False)          # 文章内容，不能为空
    created_at = db.Column(db.DateTime, default=db.func.now())  # 发布时间，自动填

    def __repr__(self):
        return f'<Post {self.title}>'

# ========================
# 🛣️ 路由：页面地址
# ========================

# 首页 — 显示所有文章
@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

# 写文章页面
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

# 文章详情页（先占位，后面完善）
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# ========================
# 🚀 启动
# ========================
if __name__ == '__main__':
    app.run(debug=True)
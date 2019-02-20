import random
import tkinter

class RandomBall:
    def __init__(self, canvas, screen_width, screen_height):
        '''
        :param canvas: 画布，呈现内容
        :param screen_width: 屏幕宽度
        :param screen_height: 屏幕高度
        '''
        # 获取画布
        self.canvas = canvas

        # 定义屏幕大小
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 定义球的随机大小
        self.radius = random.randint(30, 150)

        # 球出现的随机位置(修复球在边缘不动bug)
        self.xpos = random.randint(self.radius, int(screen_width)-self.radius)
        self.ypos = random.randint(self.radius, int(screen_height)-self.radius)

        # 球的运动速度
        self.xmove = random.randint(4, 20)
        self.ymove = random.randint(4, 20)

        # 定义球的颜色
        color = lambda: random.randint(0, 255)
        self.color = '#%02x%02x%02x'%(color(), color(), color())

    def create_ball(self):
        x1 = self.xpos - self.radius
        y1 = self.ypos - self.radius
        x2 = self.xpos + self.radius
        y2 = self.ypos + self.radius

        self.item = self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)

    def move_ball(self):
        self.xpos += self.xmove
        self.ypos += self.ymove

        # 球碰壁判断
        if self.xpos + self.radius >= self.screen_width or self.xpos - self.radius <= 0: # 右边缘上边缘
            self.xmove = -self.xmove
        elif self.ypos + self.radius >= self.screen_height or self.ypos - self.radius <= 0: # 下边缘左边缘
            self.ymove = -self.ymove

        # 移动图形
        self.canvas.move(self.item, self.xmove, self.ymove)


class ScreenSaver:
    balls = list()
    def __init__(self):
        self.ball_nums = random.randint(8, 12)
        self.root = tkinter.Tk()
        self.root.overrideredirect(1)
        self.root.attributes("-alpha", 0.4)     # 设置窗口透明度

        # 退出窗口
        self.root.bind('<Motion>', self.quitevent)   # 鼠标事件
        self.root.bind('<Key>', self.quitevent)      # 键盘事件

        # 创建画布
        self.width = self.root.winfo_screenwidth()      # 获取屏幕宽
        self.height = self.root.winfo_screenheight()    # 获取屏幕高
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        self.draw_ball()            # 添加图案
        self.run_screen_saver()     # 运行
        self.root.mainloop()

    # 在画布上画图案
    def draw_ball(self):
        for i in range(self.ball_nums):
            ball = RandomBall(self.canvas, screen_width=self.width, screen_height=self.height)
            ball.create_ball()      # 生成球对象
            self.balls.append(ball) # 添加到容器

    # 运行屏保
    def run_screen_saver(self):
        for ball in self.balls:
            ball.move_ball()
        self.canvas.after(150, self.run_screen_saver)

    def quitevent(self, event):
        self.root.destroy()


if __name__ == '__main__':
    ScreenSaver()

import React from 'react';
import ReactDom from 'react-dom';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { Menu, Icon, Layout } from 'antd';
import Login from './component/login'; // 登陆页
import Reg from './component/reg'; //注册页
import Pub from './component/pub'; // 发布页
import L from './component/list'; // 列表页
import Post from './component/post'; // 详情页
import { LocaleProvider } from 'antd';
import zhCN from 'antd/lib/locale-provider/zh_CN';

import 'antd/lib/menu/style';
import 'antd/lib/icon/style';
import 'antd/lib/layout/style';

const { Header, Content, Footer } = Layout; //上中下

const Home = () => (
  <div>
    <h1>博客项目</h1>
    <ul>
      <li>采用前后端分离开发模式</li>
      <li>前端使用最新的React技术，后端使用Django框架</li>
      <li>使用Restful风格设计服务间API接口</li>
      <li>无session认证技术，强密码技术</li>
      <li>阿里开源Antd组件</li>
      <li>企业级nginx + uWSGI + Django部署</li>
    </ul>
  </div>
);

const About = () => (
  <div>
    <h2>About</h2>
  </div>
);

const App = () => (
  <Router>
    <Layout>
      <Header>
        <Menu mode='horizontal' theme="dark">
          <Menu.Item key="home"><Link to="/"><Icon type="home" />主页</Link></Menu.Item>
          <Menu.Item key="login"><Link to="/login"><Icon type="login" />登录</Link></Menu.Item>
          <Menu.Item key="reg"><Link to="/reg">注册</Link></Menu.Item>
          <Menu.Item key="pub"><Link to="/pub">发布</Link></Menu.Item>
          <Menu.Item key="list"><Link to="/list"><Icon type="bars" />文章列表</Link></Menu.Item>
          <Menu.Item key="about"><Link to="/about">关于</Link></Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '8px 50px' }}>
        <div style={{ background: '#fff', padding: 24, minHeight: 480 }}>
          <Route path="/login" component={Login} />
          <Route path="/reg" component={Reg} />
          <Route exact path="/" component={Home} />
          <Route path="/about" component={About} />
          <Route path="/pub" component={Pub} />
          <Route path="/list" component={L} />
          <Route exact path="/post/:id" component={Post} />
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        React学习©2018-2101
        </Footer>
    </Layout>
  </Router>
);


ReactDom.render(
  <LocaleProvider locale={zhCN}>
    <App />
  </LocaleProvider>, 
  document.getElementById('root'));
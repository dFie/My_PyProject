import axios from 'axios';
import { observable } from 'mobx';
import store from 'store';

export default class PostService {
    constructor() {
        // 创建自定义实例，可以增加请求header
        this.axios = axios.create({
            baseURL: '/api/post/'
        });
    }

    @observable msg = "";
    @observable posts = []; // 博文列表
    @observable pagination = { page: 1, size: 20, pages: 0, count: 0 } //分页信息

    @observable post = {};

    getJwt() {
        return store.get('token', null);
    }

    pub(title, content) {
        console.log(title);

        this.axios.post('pub', {
            title, content
        },
            { headers: { 'Jwt': this.getJwt() } })/* dev server会代理 */
            .then(
                response => { // 此函数要注意this的问题
                    console.log(response.data);
                    console.log(response.status);
                    this.msg = '博文提交成功' //+ 信息显示
                }
            ).catch(
                error => {
                    console.log(error);
                    this.msg = '登陆失败'; //+ 信息显示
                }
            )
    }

    list(search) {
        this.axios.get(search)
            .then(
                response => { // 此函数要注意this的问题
                    console.log(response.data);
                    console.log(response.status);
                    this.posts = response.data.posts;
                    this.pagination = response.data.pagination; //分页信息
                }
            ).catch(
                error => {
                    console.log(error);
                    this.msg = '文章列表加载失败'; //+ 信息显示
                }
            )
    }

    getpost(id) {
        this.axios.get(id)
            .then(
                response => { // 此函数要注意this的问题
                    console.log(response.data);
                    console.log(response.status);
                    this.post = response.data.post;
                }
            ).catch(
                error => {
                    console.log(error);
                    this.msg = '文章加载失败'; //+ 信息显示
                }
            )
    }
}



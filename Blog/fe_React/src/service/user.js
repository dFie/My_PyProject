
import axios from 'axios';
import store from 'store';
import { observable } from 'mobx';

store.addPlugin(require('store/plugins/expire'));

export default class UserService {
    @observable loggedin = false;
    @observable regged = false;

    @observable errMsg = '';

    login(email, password) {
        axios.post('/api/user/login', {
            email : email,
            password : password
          })
          .then(response => {
            console.log(response, '++++++++++++');
            console.log(response.data);
            console.log(response.status);
            
            store.set('token', response.data.token, (new Date()).getTime() + (8*3600*1000))
            this.loggedin = true;
          })
          .catch(error => {
            console.log(error, '------------------');
            console.log(error);
            this.errMsg = "用户名或密码错误";
          });
    }

    reg(name, email, password) {
        axios.post('/api/user/reg', {
            email, password, name
          })
          .then(response => {
            console.log(response, '++++++++++++');
            console.log(response.data);
            console.log(response.status);
            
            store.set('token', response.data.token, (new Date()).getTime() + (8*3600*1000))
            this.regged = true;
          })
          .catch(error => {
            console.log(error);
            this.errMsg = "注册失败，请检查数据";
          });
    }
}

import React from 'react';
import { observer } from 'mobx-react';
import {message} from 'antd';
import { inject } from '../utils';
import { Card } from 'antd';

import PostService from '../service/post';

import 'antd/lib/card/style';
import 'antd/lib/message/style';

const service = new PostService();

@inject({ service })
@observer
export default class L extends React.Component {
    constructor(props) {
        super(props);
        // 匹配
        let {id = -1} = props.match.params; // {id:'3'}
        props.service.getpost(id);
    }
    render() {
        let s = this.props.service;
        if (s.msg) {
            message.info(s.msg, 3, () => setTimeout(() => s.msg='', 1000));
        }
        let post = s.post;
        if (post.title) {
            return <Card title={post.title} bordered={true} style={{width:600}}>
                <p>作者:{post.author}&nbsp;&nbsp;时间:{new Date(post.postdate*1000).toLocaleDateString()}</p>
                <p>{post.content}</p>
            </Card>
        }else
            return (<div></div>);
    }
}
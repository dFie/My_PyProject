import React from 'react';
import { Link, Redirect } from 'react-router-dom';
import { observer } from 'mobx-react';
import { message } from 'antd';
import { inject } from '../utils';
import { Form, Input, Button } from 'antd';
import FormItem from 'antd/lib/form/FormItem'; //不在antd中单独导
import PostService from '../service/post';

import 'antd/lib/message/style';
import 'antd/lib/form/style';
import 'antd/lib/input/style';
import 'antd/lib/button/style';

const { TextArea } = Input;

const service = new PostService();

@inject({ service })
@observer
export default class Pub extends React.Component {
    handleSubmit(event) {
        event.preventDefault();
        console.log(event.target)
        let fm = event.target;
        console.log(fm[0].value);
        console.log(fm[1].value);
        this.props.service.pub(fm[0].value, fm[1].value);
    }

    render() {
        if (this.props.service.msg) {
            message.info(this.props.service.msg, 3,
                () => setTimeout(() => this.props.service.msg= ''), 1000);
        }

        return (
            <Form onSubmit={this.handleSubmit.bind(this)}>
                <FormItem label="标题" labelCol={{ span: 4}} wrapperCol={{ span: 14 }}>
                    <Input placeholder="标题" />
                </FormItem>
                <FormItem label="内容" labelCol={{ span: 4}} wrapperCol={{ span: 14 }}>
                    <TextArea rows={ 10 } />
                </FormItem>
                <FormItem wrapperCol={{ span: 14, offset: 4 }}>
                    <Button type="primary" htmlType="submit">提交</Button>
                </FormItem>
            </Form>
        );
    }
}
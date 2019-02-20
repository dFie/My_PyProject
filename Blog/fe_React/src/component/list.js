import React from 'react';
import { observer } from 'mobx-react';
import { message } from 'antd';
import { inject, parse_qs } from '../utils';
import { List } from 'antd';
import { Link } from 'react-router-dom';

import PostService from '../service/post';

import 'antd/lib/message/style';
import 'antd/lib/list/style';

const service = new PostService();

@inject({ service })
@observer
export default class L extends React.Component {
    constructor(props) {
        super(props);
        // 将查询字符串向后传
        props.service.list(props.location.search);
    }

    handleChange(pageNo, pageSize) {
        console.log(pageNo, pageSize);
        // 不管以前查询字符串是什么，重新拼接  查询字符串  向后传
        let search = '?page=' + pageNo + '&size=' + pageSize;
        this.props.service.list(search);
    }

    geturl(c) {
        let obj = parse_qs(this.props.location.search);
        let {size=20} = obj;
        return '/list?page=' + c + '&size=' + size;
    }

    itemRender(current, type, originalElement) {
        if (current == 0) return originalElement; // 竟然返回0，只能屏蔽它
        if (type === 'page')
            return <Link to={this.geturl(current)}>{current}</Link>;
        if (type === 'next')
            return <Link to={this.geturl(current)} className='ant-pagination-item-link'>&gt;</Link>;
        if (type === 'prev')
            return <Link to={this.geturl(current)} className='ant-pagination-item-link'>&lt;</Link>;
        return originalElement;
    }

    render () {
        let data = this.props.service.posts;

        if (data.length) {
            const pagination = this.props.service.pagination;
            return (
                <List   bordered={true} 
                        dataSource={data} 
                        renderItem={item => (
                        <List.Item>
                            <List.Item.Meta title={<Link to={'/post/' + item.post_id}>{item.title}</Link>} /> 
                        </List.Item>)}
                        pagination={{
                            current:pagination.page,
                            pageSize:pagination.size,
                            total:pagination.count,
                            onChange:this.handleChange.bind(this),
                            itemRender:this.itemRender.bind(this),}}
                />
            );
        } else {
            return (<div></div>);
        }
    }
}
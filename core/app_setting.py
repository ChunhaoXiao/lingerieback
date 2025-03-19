settings = {
    "app_status":{
        "value":"1",
        "description":"是否开启访问",
        "type":"switch"
    },
    "index_hot_num":{
        "value":"5",
        "description":"首页推荐显示数量",
        "type":"input"
    },
    
    "index_recommand_num":{
        "value":"10",
        "description":"首页热门数量",
        "type":"input"
    },
    
    "index_recommand_order":{
        "options":[
            {"label":"按点赞数量排序","value":"like_cnt"},
            {"label":"随机获取","value":"random"}
        ],
        "value":"like_cnt",
        "description":"首页热门排序",
        "type":"radio"
        
    },
    
    "feed_back_status": {
        "value":"1",
        "description":"开启意见反馈",
        "type":"switch"
    },
    "category-list-count":{
        "value":"20",
        "description":"列表页每页数量",
        "type":"input"
    },
    "feedback_max_files":{
        "value":"9",
        "description":"意见反馈最大上传数量",
        "type":"input"
    }
}
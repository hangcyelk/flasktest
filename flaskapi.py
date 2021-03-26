# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 09:32:21 2021

@author: bmeyj
"""

from flask import Flask, jsonify,url_for
from flask import abort
from flask import request

app = Flask(__name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/test/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
#检查tasks内部的元素，是否有元素的id值和参数相匹配
    task = list(filter(lambda t: t['id'] == task_id, tasks))
 #有的话，就返回列表形式包裹的这个元素，没有的话就报错404  
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
    #否则，将这个task以json的格式返回。

@app.route('/test/api/tasks', methods=['POST'])
def create_task():
#如果请求里面没有json数据，或者json数据里面title的内容为空
    if not request.json or not 'title' in request.json:
        abort(400) #返回404错误
    task = {
        'id': tasks[-1]['id'] + 1, #取末尾tasks的id号+1
        'title': request.json['title'], #title必须设置，不能为空。
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task) #完了之后，添加这个task进tasks列表
    return jsonify({'task': task}), 201  #并且返回这个添加的task内容和状态码。

@app.route('/test/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    #检查是否有这个id数据
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    #如果请求中没有附带json数据，则报错400
    if not request.json:
        abort(400)
    #如果title对应的值，不是字符串类型，则报错400
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    #检查done对应的值是否是布尔值
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    #如果上述条件全部通过的话，更新title的值，同时设置默认值
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    #返回修改后的数据
    return jsonify({'task': task[0]})

@app.route('/test/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    #检查是否有这个数据
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    #从tasks列表中删除这个值
    tasks.remove(task[0])
    #返回结果状态，自定义的result
    return jsonify({'result': True})

def make_public_task(task):       
    new_task={}             #新建一个对象，字典类型  
    for key in task:        #遍历字典内部的KEY  
        if key == 'id': #当遍历到id的时候，为新对象增加uri的key，对应的值为完整的uri  
            new_task['uri'] = url_for('get_task',task_id=task['id'],_external=True)  
        else:  
            new_task[key] = task[key]  #其他的key，分别一一对应加入新对象  
    return new_task                            #最后返回新对象数据  


#修改获取合集的路由

@app.route('/test/api/tasks',methods=['GET'])  
def get_tasks():  
    return jsonify({'tasks': list(map(make_public_task,tasks))})  #使用map函数，罗列出所有的数据，返回的数据信息，是经过辅助函数处理的 


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
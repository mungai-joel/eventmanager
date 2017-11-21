from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    return "HOME"

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

EVENTS = {
    "ev1": {"id":1,"name":"caaname","rsvp":"NO", "category":"namecategory"},
     "ev2":{"id":2, "name":"pname", "rsvp":"NO", "category":"namecategory"},
     "ev3": {"id":1,"name":"caaname","rsvp":"YES", "category":"namecategory"},
     "ev4": {"id":1,"name":"caaname","rsvp":"YES", "category":"namecategory"},
     "ev5": {"id":1,"name":"caaname","rsvp":"YES", "category":"namecategory"}
}

parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
    # get an event
    def get(self, ev_id):
        # abort_if_todo_doesnt_exist(todo_id)
        return EVENTS[ev_id]
    
        #delete
    def delete(self, ev_id):
        # abort_if_todo_doesnt_exist(todo_id)
        del EVENTS[ev_id]
        return '', 204

    #Update
    def put(self, ev_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        EVENTS[ev_id] = task
        return task, 201

class FilterOut(Resource):
    def get(self):
        lst = []
        for value in EVENTS:
            #print(value)
            for values in EVENTS[value]:
                #print(values)
                if values == "rsvp" and EVENTS[value][values] == "YES":
                    #print(value)
                    lst.append(values)
                    print(lst)
                    #return lst
                    

class TodoList(Resource):
    def get(self):
        return EVENTS
    
    # Add an event
    def post(self):
        args = parser.parse_args()
        ev_id = int(max(EVENTS.keys()).lstrip('ev')) + 1
        ev_id = 'ev%i' % ev_id
        EVENTS[ev_id] = {'task': args['task']}
        return EVENTS[ev_id], 201

api.add_resource(TodoList, '/events')
api.add_resource(FilterOut, '/events/rsvp')
api.add_resource(Todo, '/events/<ev_id>')

app.run(debug=True)
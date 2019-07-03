from flask import Flask, request

import control.book
import control.video
import control.weather

app = Flask(__name__)
@app.route('/',methods=['GET', 'POST'])
def index():
    return '没有数据'

@app.route('/video/<type>', methods=['GET', 'POST'])
def video(type):
    if type == 'frist':
        return control.video.frist()
    if type == 'detailed':
        return control.video.detailed_func(request.data)
    # 演员详细信息
    if type == 'actor':
        print(request.data)
        return control.video.detailed_actor_func(request.data)
    if type == 'search':
        return control.video.search_func(request.args.get('q'))


@app.route('/book/<type>', methods=['GET', 'POST'])
def book(type):
    if type == 'free':
        return control.book.free_func()
    if type == 'wrap':
        result=control.book.wrap_func()
        print(result)
        return result
    if type == 'week':
        return control.book.week_func()
    if type == 'writer':
        return control.book.writer_func()
    if type == 'detailed':
        return control.book.detailed_func(request.args.get('url'))
    if type == 'detailed_read':
        return control.book.read_func(request.args.get('url'), request.args.get('type'))
    if type == 'detailed_list':
        result=control.book.list_func(request.args.get('url'))
        return result
    if type == 'groom':
        return control.book.groom_func()
    if type == 'search':
        return control.book.search_func(request.args.get('value'))
    else:
        return 'abc'



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    return control.weather.getrealweather(request.data)

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)

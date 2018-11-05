import flask, multiprocessing
web = flask.Flask('', static_folder='.', root_path='/home/runner')

@web.route('/')
def send_html_index(): return web.send_static_file('./data/_index.html')
def run(): web.run(host='0.0.0.0',port=8080,debug=True)
def start_server(): multiprocessing.Process(target=run,daemon=True).start()
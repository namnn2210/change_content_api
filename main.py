from flask import Flask, request, jsonify
from flask_cors import CORS
from api.openai_api import OpenAIAPI
from handle.rewite import do_rewrite
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

openai_obj = OpenAIAPI()

@app.route('/api/content', methods=['POST'])
def rewrite_post():
    # body_sample = {
    #     "title": {
    #         "text":"$2M for One Song or No Payment at All, Health Risks & More",
    #         "config":{    
    #             "rewrite_title": "viết lại tối đa 20 từ"
    #         }
    #     },
    #     "content": {
    #         "text":"",
    #         "config": {
    #             "rewrite_heading": "viết lại tối đa 10 từ",
    #             "rewrite_content": "viết lại",
    #             "rewrite_description":"",
    #         }
    #     },
    #     "option":"",
    #     "n": "5"
    # }
    try:
        final_results = []
        body = request.get_json()
        title = body.get('title')
        content = body.get('content')
        option = body.get('option')
        if not title or not content:
            print('not title or content')
            return jsonify(status=502, message='Missing post params', data=final_results)
        print('start: ', datetime.now())
        result = do_rewrite(api_obj=openai_obj, title=title, content=content, option=option)
        print(result)
        print('end: ', datetime.now()) 
        return jsonify(result)
    except Exception as ex:
        print(str(ex))
        return jsonify(status=500, message=f'Server Error: {str(ex)}', data=final_results)

if __name__ == '__main__':
    app.run(debug=True)
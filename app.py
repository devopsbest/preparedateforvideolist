from flask import Flask,request,jsonify,render_template
from video import push_video_list,get_current_host

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("videolist.html")



@app.route('/trigger', methods=['GET'])
def get_video():
    if request.method == "GET":

        print(request.args)

        memberid = request.args.get("memberid")
        print(memberid)
        userid = request.args.get("userid")
        env = request.args.get("env")


        print(userid)
        print(env)
        message ="error"

        host = get_current_host(env)


        if memberid == "":
            message = "Error! Please input memberid"

        if userid == "":
            message = "Error! Please input userid"

        if env == "":
            messsage = "Error! Please select env"

        # if memberid and env:
        #     pass_whole_progress(env, memberid)
        #     message = "Done"

        push_video_list(host,[memberid],[userid])


        return jsonify({"result": message})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

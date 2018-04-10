import requests
import sys
from flask import Flask, render_template,request
from flask_pure import Pure
import urllib.request

app =  Flask(__name__)
app.config['PURECSS_RESPONSIVE_GRIDS'] = True
app.config['PURECSS_USE_CDN'] = True
app.config['PURECSS_USE_MINIFIED'] = True
Pure(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    status = True
    try:
        hostname = "https://www.eolementhe.cloud"
        response = urllib.request.urlopen(hostname, timeout = 25).getcode()
        
        # print(urllib.request.urlopen(hostname).getcode())
        status = True
    except:
        print("none")
        status = False

    if request.method == 'POST':


        print(request.form['eolementhenet'])

        jenkins_host = "jenkins.eolementhe.top:8080"
        jenkins_user = "admin"
        jenkins_api = "a83129f8e05a64e10dddced9bbb68e4a"

 
        jenkins_job = request.form['eolementhenet']
        action = "build"

        # Now enable or disable the job
        job_url = "http://{0}:{1}@{2}/job/{3}/{4}".format(jenkins_user, jenkins_api, jenkins_host, jenkins_job, action)
        headers = dict()
        headers["Jenkins-Crumb"] ='4d0cb0b07da737b03fb39d6eeea8a4fc'
        print(headers)
        print("{0}ing job {1} at jenkins server {2}".format(action[0:-1], jenkins_job, jenkins_host))
        response = requests.post(job_url, headers=headers)

        print(response)
        if response.status_code == 201:
            print("Job {0} {1}ed successfully on the server {2}".format(jenkins_job, action[0:-1], jenkins_host))
        else:
            print("Something went wrong. Check out the response while {0}ing the job {1}:\nResponse:{2}".format(action,
                                                                                                    jenkins_job, response.content))

        return 'le formulaire a été soumis'
    else:
        return render_template("index.html", status=status)


@app.route('/jenkins', methods=['GET', 'POST'])
def jenkins():
    print(request)
    return render_template('index.html')

    # jenkins_host = "jenkins.eolementhe.top:8080"
    # jenkins_user = "admin"
    # jenkins_api = "a83129f8e05a64e10dddced9bbb68e4a"

    # # Check command line args
    # if len(sys.argv) < 3:
    #     print("Usage: python jenkins_modify_jobs.py job_name action (enable or disable)")
    #     exit()
    # jenkins_job = sys.argv[1]
    # action = sys.argv[2]

    # # First get a CRUMB from Jenkins
    # # url = "http://{0}:{1}@{2}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)".\
    # #     format(jenkins_user,jenkins_api,jenkins_host)

    # # crumb = requests.get(url).content
    # # print(crumb)

    # # Now enable or disable the job
    # job_url = "http://{0}:{1}@{2}/job/{3}/{4}".format(jenkins_user, jenkins_api, jenkins_host, jenkins_job, action)
    # headers = dict()
    # headers["Jenkins-Crumb"] ='4d0cb0b07da737b03fb39d6eeea8a4fc'
    # print(headers)
    # print("{0}ing job {1} at jenkins server {2}".format(action[0:-1], jenkins_job, jenkins_host))
    # response = requests.post(job_url, headers=headers)

    # print(response)
    # if response.status_code == 201:
    #     print("Job {0} {1}ed successfully on the server {2}".format(jenkins_job, action[0:-1], jenkins_host))
    # else:
    #     print("Something went wrong. Check out the response while {0}ing the job {1}:\nResponse:{2}".format(action,
    #                                                                                             jenkins_job, response.content))

if __name__ =='__main__':
    app.run(debug=True)
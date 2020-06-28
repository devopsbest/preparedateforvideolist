import requests
from bs4 import BeautifulSoup
import re

requests.packages.urllib3.disable_warnings()



# memberlist = ["11521266"]
# id1 = ["10000518","10000519","10000520","10000521"]
# id = ["10000548"]
#
# host_uat = "https://ecuat-us.englishtown.cn/"
# host = "https://qa.englishtown.cn/"

def get_current_host(my_host):
    host={
        "uatcn":"https://ecuat-us.englishtown.cn/",
        "uatus": "https://ecuat-us.englishtown.cn/",
        "qacn": "https://qa.englishtown.cn/",
        "qaus": "https://qa.englishtown.com/",
        "stagingcn": "https://staging.englishtown.cn/",
        "stagingus": "https://staging.englishtown.com/"
    }[my_host]
    return host


s = requests.Session()
s.verify = False


def get_token(host):
    token_url = "{}services/oboe2/Areas/ServiceTest/MemberSiteSetting.aspx".format(host)

    page = s.get(token_url)

    soup = BeautifulSoup(page.content, 'lxml')

    target = soup.select('#token')
    print(str(target))
    find_result = re.search('>(.*?)<', str(target))
    if find_result != None:
        print(find_result.group(1))
        return find_result.group(1)


def bind_debug(host,member_id):

    url = '{}services/ecplatform/Tools/StudentSettings/SaveMemberSiteSetting'.format(host)
    data = {'studentId': member_id,
            'siteArea': "ec_dod",
            'key': "eftv.user.debug",
            'value': True
            }

    response = s.post(url=url, data=data)
    assert '"IsSuccess":true' in response.text, response.text

def bind_trial_user(host,id):
    author = "Bearer " + get_token(host)
    url = "{}services/api/dod/test/usersetting?entityType=FreeTrialUser&entityId={}&key=eftv.user.debug&value=True".format(
        host, id)
    header = {
        "Authorization": author,
    }

    response = s.post(url=url, headers=header)

    print(response.status_code)


def trigger_videos(host,memberlist, triallist):
    members = ",".join(memberlist)
    trials = ",".join(triallist)
    debugids = "EtMember;{}|FreeTrialUser;{}".format(members, trials)
    url = "{}services/api/dod/job/schedulednotification".format(host)

    headers = {
        "Content-Type": "application/json"
    }
    json = {
        "resourceType": "EFTV_debug",
        "cultureCode": "zh-cn",
        "partnerCodes": "cool",
        "batchsize": 20,
        "timeZoneId": "china standard time",
        "debugUserIds": debugids
    }

    for i in range(3):
        response = s.post(url=url, headers=headers, json=json)
        print(response.status_code)


def push_video_list(host,memberlist,idlist):

    print("bind for students")
    for x in memberlist:
        bind_debug(host,x)

    print("for trial user bind")
    for x in idlist:
        bind_trial_user(host,x)

    print("start to push")
    trigger_videos(host,memberlist, idlist)

# if __name__ == "__main__":
#
#
#     print("bind for students")
#     for x in memberlist:
#         bind_debug(x)
#
#     print("for trial user bind")
#     for x in id:
#         bind_trial_user(x)
#
#     print("start to push")
#     trigger_videos(memberlist, id)



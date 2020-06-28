import requests
from bs4 import BeautifulSoup
import re

requests.packages.urllib3.disable_warnings()



memberlist = ["11521266"]
id1 = ["10000518","10000519","10000520","10000521"]
id = ["10000548"]

host_uat = "https://ecuat-us..cn/"
host = "https://qa..cn/"

def get_current_host(my_host):
    host={
        "uat_cn":"https://ecuat-us..cn/",
        "uat_us": "https://ecuat-us..cn/",
        "qa_cn": "https://qa..cn/",
        "qa_us": "https://qa..com/",
        "staging_cn": "https://staging..cn/",
        "staging_us": "https://staging..com/"
    }[my_host]
    return host

# import pymssql
#
# if "us" in host:
#
#     _connection_info = ('10.179..72', 'TestUser', 'testuserdev', 'AppServices')
# else:
#     _connection_info = ('10.179..83', 'TestUser', 'testuserdev', 'AppServices')
#
# ecdb_conn_v2 = pymssql.connect(*_connection_info, login_timeout=10)
# ecdb_cur_v2 = ecdb_conn_v2.cursor()
s = requests.Session()
s.verify = False


def get_token():
    token_url = "{}services/oboe2/Areas/ServiceTest/MemberSiteSetting.aspx".format(host)

    page = s.get(token_url)

    # soup = BeautifulSoup(page.content, 'html5lib')
    soup = BeautifulSoup(page.content, 'lxml')

    target = soup.select('#token')
    print(str(target))
    find_result = re.search('>(.*?)<', str(target))
    if find_result != None:
        print(find_result.group(1))
        return find_result.group(1)


def bind_debug(member_id):
    # memberseting_url = "{}services/ecplatform/Tools/StudentSettings?id={}&token=null".format(host, member_id)

    # data = {
    #     "studentId": member_id,
    #     "siteArea": "ec_dod",
    #     "key": "eftv.user.debug",
    #     "value": True,
    # }

    # response = requests.post(url=memberseting_url.format(member_id), data=data, verify=False)
    # print(response.status_code)
    url = '{}services/ecplatform/Tools/StudentSettings/SaveMemberSiteSetting'.format(host)
    data = {'studentId': member_id,
            'siteArea': "ec_dod",
            'key': "eftv.user.debug",
            'value': True
            }

    response = s.post(url=url, data=data)
    assert '"IsSuccess":true' in response.text, response.text

def bind_trial_user(id):
    author = "Bearer " + get_token()
    url = "{}services/api/dod/test/usersetting?entityType=FreeTrialUser&entityId={}&key=eftv.user.debug&value=True".format(
        host, id)
    header = {
        "Authorization": author,
    }

    response = s.post(url=url, headers=header)

    print(response.status_code)


def trigger_videos(memberlist, triallist):
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

# def get_trialuserid():
#     sql = """
#     select top 1 User_id from ECOnlineSale..UserSetting
#     order by InsertDate desc
#
#     """
#
#     ecdb_cur_v2.execute(sql)
#     print(ecdb_cur_v2.fetchall())
#     return ecdb_cur_v2.fetchall()
#
#
# def check_member_tag():
#
#     # 判断时debug tag是否加入
#     sql1="""
#     select * from ET_Main.dbo.membersitesetting
#     where member_id=24118728
#     and KeyCode = 'eftv.user.debug'
#     """
#     ecdb_cur_v2.execute(sql1)
#     print(ecdb_cur_v2.fetchall())
#
#
#
# def trigger_notification(memberid):
#     sql = """
#     DECLARE @delayminutes int
#     DECLARE @memberid int
#     set @delayminutes = 5
#     set @memberid = {} --need to update
#     update AppServices.dbo.PushMessage
#     set TriggerDate = DATEADD(mi,@delayminutes,GETDATE()),LockExpireDate = DATEADD(mi,@delayminutes,GETDATE()),ExpireDate = DATEADD(dd,@delayminutes,GETDATE()),runTimes = 0, isDeleted = 0
#     where PushMessage_id in (select top 1 PushMessage_id from AppServices.dbo.PushMessage where CustomMessageId =@memberid order by PushMessage_id desc)
#     """.format(memberid)
#
#     ecdb_cur_v2.execute(sql)


if __name__ == "__main__":
    #get_trialuserid()

    print("bind for students")
    for x in memberlist:
        bind_debug(x)

    print("for trial user bind")
    for x in id:
        bind_trial_user(x)

    print("start to push")
    trigger_videos(memberlist, id)



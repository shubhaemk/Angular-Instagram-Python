from matplotlib.ticker import FormatStrFormatter
from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import Flask, request
from datetime import datetime
from dateutil import tz
import matplotlib.pyplot as plt
import urllib.request as ur
import subprocess as p
import pandas as pd
import numpy as np
import operator
import time
import json



app = Flask(__name__)
api = Api(app)

uname = ""
pas = ""
user_id = 0
myposts=[]
API = InstagramAPI(uname,pas)

class userData(Resource):
    def get(self):
        global API
        global user_Id
        API.getProfileData()
        js1 = API.LastJson
        user_Id = js1['user']['pk']
        API.getUsernameInfo(user_Id)
        js2 = API.LastJson
        return {'a':js1,'b':js2}

    def put(self):
        data = request.get_json()
        global API
        global uname
        global pas
        uname = data['user']
        pas = data['pas']
        API = InstagramAPI(uname,pas)
        if API.login():
            return 1
class userFeed(Resource):
    def get(self):
        global API
        API.timelineFeed()
        js3 = API.LastJson
        js4 = js3['items']
        return js4
    def put(self):
        data = request.get_json()
        ur.urlretrieve(data['url'], "insta.jpg")
        description = p.check_output("python3 classify_image.py --image_file insta.jpg", shell=True).decode("utf-8")
        dict = {'description':description}
        return dict
class myFeed(Resource):
    def get(self):
        global API
        global user_Id
        global myposts
        has_more_posts = True
        max_id=""
        while has_more_posts:
            API.getSelfUserFeed(maxid=max_id)
            if API.LastJson['more_available'] is not True:
                has_more_posts = False
            max_id = API.LastJson.get('next_max_id','')
            myposts.extend(API.LastJson['items'])
            time.sleep(2)
        f = open("data.json","w")
        json.dump(myposts,f)
        return myposts
class likeAnalytics(Resource):
    def get(self):
        global API
        global myposts
        totalLikes = 0
        likers = []
        m_id = 0
        for i in range(len(myposts)):
            m_id = myposts[i]['id']
            API.getMediaLikers(m_id)
            likers += [API.LastJson]
            time.sleep(2)
        users = []
        for i in likers:
            users += map(lambda x: i['users'][x]['username'],range(len(i['users'])))
            totalLikes += i['user_count']
        users_set = set(users)
        unique_likes = len(users_set)
        avg_likes = (totalLikes/len(myposts))
        l_dict = {}
        for user in users_set:
            l_dict[user] = users.count(user)
        all_pairs = sorted(l_dict.items(), key=operator.itemgetter(1))
        n_users = 10 # top 10 users
        pairs = all_pairs[-n_users:]
        user_array=[]
        likes_array=[]
        for x in pairs:
            user_array.append(x[0])
            likes_array.append(x[1])
        str1 = ','.join(user_array)
        str2 = ','.join(str(e) for e in likes_array)
        p.check_output("python3 LikersGraph.py "+str1+" "+str2, shell=True)
        return {'topLikers':'Graph.png','totalLikes':totalLikes,'uniqueLikes':unique_likes,'avg_likes':avg_likes}
class followAnalytics(Resource):
    def get(self):
        global API
        user_id = API.username_id
        datastore1 = API.getTotalFollowers(user_id)
        datastore2 = API.getTotalFollowings(user_id)
        count=0
        followUsers=[]
        followingUsers=[]
        for x in datastore1:
            for y in datastore2:
                if x['username'] == y['username']:
                    count+=1
        for x in datastore1:
            followingUsers.append(x['username'])
        for x in datastore2:
            followUsers.append(x['username'])
        str1 = ','.join(followUsers)
        str2 = ','.join(followingUsers)
        str3 = str(count)
        p.check_output("python3 FollowersGraph.py "+str1+" "+str2+" "+str3, shell=True)
        return {'followGraph':'Followers.png','followingGraph':'Following.png'}
class commonFollow(Resource):
    def put(self):
        global API
        common=[]
        json_request = request.get_json()
        u_name = str(json_request['u_name'])
        user_id = API.username_id
        following = API.getTotalFollowings(user_id)
        for data in following:
            if u_name == str(data['username']):
                new_id = data['pk']
                break
        new_following = API.getTotalFollowers(new_id)
        for data1 in following:
            for data2 in new_following:
                if data1['username'] == data2['username']:
                    common.append(data1['username'])
        return {'common':common}
class followAccountAnalytics(Resource):
    def get(self):
        global API
        user_id = API.username_id
        datastore1 = API.getTotalFollowers(user_id)
        datastore2 = API.getTotalFollowings(user_id)
        followPrivateCount=0
        followingPrivateCount=0
        for x in datastore1:
            if x['is_private']:
                followingPrivateCount+=1
        for x in datastore2:
            if x['is_private']:
                followPrivateCount+=1
        str1 = str(followPrivateCount)
        str2 = str(len(datastore2))
        str3 = str(followingPrivateCount)
        str4 = str(len(datastore1))
        p.check_output("python3 FollowersPrivateGraph.py "+str1+" "+str2+" "+str3+" "+str4, shell=True)
        return {'followAccountGraph':'FollowersPrivate.png','followingAccountGraph':'FollowingPrivate.png'}
class topPost(Resource):
    def get(self):
        global API
        global user_Id
        global myposts
        has_more_posts = True
        max_id=""
        while has_more_posts:
            API.getSelfUserFeed(maxid=max_id)
            if API.LastJson['more_available'] is not True:
                has_more_posts = False
            max_id = API.LastJson.get('next_max_id','')
            myposts.extend(API.LastJson['items'])
            time.sleep(2)
        maxLike = 0
        maxComment = 0
        for x in myposts:
            if x['like_count'] > maxLike:
                maxLike = x['like_count']
                topLikeUrl = x['image_versions2']['candidates'][0]['url']
            if x['comment_count'] > maxComment:
                maxComment = x['comment_count']
                topCommentUrl = x['image_versions2']['candidates'][0]['url']
        return {'topLikeUrl':topLikeUrl,'likes':maxLike,'topCommentUrl':topCommentUrl,'comments':maxComment}
class mapData(Resource):
    def get(Self):
        global API
        global user_Id
        myPosts = []
        myLocation = []
        locationCount=[]
        uniqueLocationCount  = []
        has_more_posts = True
        max_id=""
        while has_more_posts:
            API.getSelfUserFeed(maxid=max_id)
            if API.LastJson['more_available'] is not True:
                has_more_posts = False
            max_id = API.LastJson.get('next_max_id','')
            myPosts.extend(API.LastJson['items'])
            time.sleep(2)
        for item in myPosts:
            if "location" in item:
                myLocation.append({"locationData":item['location'],"url": item['image_versions2']['candidates'][0]['url']})
        for location in myLocation:
            lat = location['locationData']['lat']
            lng = location['locationData']['lng']
            locationCount.append({"lat":lat,"lng":lng,"count":0,"name":location['locationData']['name'],"url":location['url']})
        size = len(locationCount)
        for x in locationCount:
            if (x not in uniqueLocationCount):
                uniqueLocationCount.append(x)
        for x in uniqueLocationCount:
            for y in locationCount:
                if ((y["lat"] == x["lat"]) and (y["lng"] == x["lng"])):
                    x["count"] = x["count"] + 1
        return uniqueLocationCount
class postFrequency(Resource):
    def get(Self):
        global API
        global user_Id
        myPosts = []
        hourCount = []
        uniqueHourCount = []
        sortedUniqueCount = []
        has_more_posts = True
        max_id=""
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        while has_more_posts:
            API.getSelfUserFeed(maxid=max_id)
            if API.LastJson['more_available'] is not True:
                has_more_posts = False
            max_id = API.LastJson.get('next_max_id','')
            myPosts.extend(API.LastJson['items'])
            time.sleep(2)
        for img in myPosts:
            timestamp = img['taken_at']
            hour = datetime.utcfromtimestamp(timestamp).strftime('%H')
            hour = int(hour) + 4
            hourCount.append({"label":hour,"y":0})
        for x in hourCount:
            if (x not in uniqueHourCount):
                uniqueHourCount.append(x)
        for x in uniqueHourCount:
            for y in hourCount:
                if (y['label'] == x['label']):
                    x['y'] = x['y'] + 1
        sorted_obj = dict(uniqueHourCount)
        sorted_obj = sorted(uniqueHourCount, key=lambda x : int(x['label']), reverse=False)
        return sorted_obj
class logout(Resource):
    def get(Self):
        global API
        global uname
        global pas
        global user_id
        global myposts
        uname = ""
        pas = ""
        user_id = 0
        myposts=[]
        API.logout()
        return {'a':1}

api.add_resource(userData, '/userData')
api.add_resource(userFeed, '/userFeed')
api.add_resource(myFeed, '/myFeed')
api.add_resource(likeAnalytics,'/likeAnalytics')
api.add_resource(followAnalytics,'/followAnalytics')
api.add_resource(followAccountAnalytics,'/followAccountAnalytics')
api.add_resource(topPost,'/topPost')
api.add_resource(logout,'/logout')
api.add_resource(commonFollow,"/common")
api.add_resource(mapData,"/mapData")
api.add_resource(postFrequency,"/postFrequency")
if __name__ == '__main__':
     app.run(host='127.0.0.1',threaded=True)

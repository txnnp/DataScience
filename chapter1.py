from audioop import reverse
from csv import unregister_dialect

users = [
    {'id': 0, 'name': 'Hero'},
    {'id': 1, 'name': 'Dun'},
    {'id': 2, 'name': 'Sue'},
    {'id': 3, 'name': 'Chi'},
    {'id': 4, 'name': 'Thor'},
    {'id': 5, 'name': 'Clive'},
    {'id': 6, 'name': 'Hicks'},
    {'id': 7, 'name': 'Devin'},
    {'id': 8, 'name': 'Kate'},
    {'id': 9, 'name': 'Klein'},
]

friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

friendships = {user['id']: [] for user in users}
for i, j in friendship_pairs:
    friendships[i].append(j)
    friendships[j].append(i)

def number_of_friends(user):
    """ How many friends does user have?"""
    user_id = user['id']
    friend_ids = friendships[user_id]
    return len(friend_ids)

total_connections = sum(number_of_friends(user) for user in users)
print(total_connections)    # 24

num_users = len(users)
print(num_users)            # 10
average_connections = total_connections / num_users
print(average_connections)  # 2.4

# คนที่มีเพื่อนมากที่สุด
num_friends_by_id = [(user['id'], number_of_friends(user)) for user in users]
num_friends_by_id.sort(key=lambda id_and_friends: id_and_friends[1], reverse=True)
print(num_friends_by_id)    # (user_id, num_friends)

# คนที่คุณอาจรู้จัก
def foaf_ids_bad(user):
    """foaf is hort for 'friend of a friend' """
    return [foaf_id 
            for friend_id in friendships[user['id']]
            for foaf_id in friendships[friend_id]]

print(foaf_ids_bad(users[0]))       # [0, 2, 3, 0, 1, 3]

# นับจำนวนเพื่อนร่วมกันและตัดคนที่รู้จักกันเเล้วออกไป
from collections import Counter

def friends_of_friends(user):
    user_id = user['id']
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]       # for each of my friend 
        for foaf_id in friendships[friend_id]       # find their friends
        if foaf_id != user_id                       # who aren't me
        and foaf_id not in friendships[user_id]     # and aren't my friends
    )

print(friends_of_friends(users[3]))                 # Counter({0: 2, 5: 1}) หมายถึง id 3 มีเพื่อนร่วมกับ id 0 2 คน เเละมีเพื่อนร่วมกับ id 5 1 คน

interests = [ 
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"), 
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"), 
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"), 
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"), 
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"), 
    (3, "statistics"), (3, "regression"), (3, "probability"), 
    (4, "machine learning"), (4, "regression"), (4, "decision trees"), 
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"), 
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"), 
    (6, "probability"), (6, "mathematics"), (6, "theory"), 
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"), 
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"), 
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"), 
    (9, "Java"), (9, "MapReduce"), (9, "Big Data") 
]

# ค้นหาคนตามสิ่งที่สนใจ แต่เราต้องรู้สิ่งที่สนใจทั้งหมดเพื่อที่จะสามารถหาคนที่ชอบสิ่งนั้นได้
def data_scientists_who_like(target_interest):
    """Find the ids of all users who like the target interest"""
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]
print(data_scientists_who_like('Python'))

from collections import defaultdict

# สร้างดัชนีจากความสนใจของผู้ใช้
# Keys are interests, values are list of user_ids with that interest
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# ในทางกลับกันดัชนีจากผู้ใช้ไปสู่ความสนใจ
# Keys are user_ids, values are list of interests for that user_id
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

# ตรวจสอบแต่ละความสนใจของผู้ใช้, ในเเต่ละความสนใจให้หาผู้ใช้อื่นที่มีความสนใจเดียวกัน, นับจำนวนผู้ใช้อื่น
def most_common_interests_with(user):
    return Counter(
        interested_user_id
        for interest in interests_by_user_id[user['id']]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user['id']    
    )

print(most_common_interests_with(users[0]))

# รายได้เเละประสบการณ์การทำงาน
salaries_and_tenures = [(83000, 8.7), (88000, 8.1), 
                        (48000, 0.7), (76000, 6), 
                        (69000, 6.5), (76000, 7.5), 
                        (60000, 2.5), (83000, 10), 
                        (48000, 1.9), (63000, 4.2)]

# Keys are years, values are lists of the salaries for each tenure
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)

# Keys are years, each value is average salary for that tenure
average_salary_by_tenure = {
    tenure: sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

# เราจะได้เเค่อายุงานของเเต่ละตนเท่านั้น
print(average_salary_by_tenure)

# จัดกลุ่มอายุงาน
def tenure_bucket(tenure):
    if tenure < 2:
        return 'less than two'
    elif tenure < 5:
        return 'between two and five'
    else:
        return 'more than five'

# จัดกลุ่มรายได้ตามกลุ่มอายุงาน
# Keys are tenure buckets, values are lists of salaries for that bucket
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)
print(salary_by_tenure_bucket)

# คำนวนรายได้เฉลี่ยในเเต่ละกลุ่ม
# Keys are tenure buckets, values are average salary of that bucket
average_salary_by_bucket = {
    tenure_bucket: sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}
print(average_salary_by_bucket)

# การนับคำ
words_and_counts = Counter(word 
                            for user, interest in interests 
                            for word in interest.lower().split())
for word, count in words_and_counts.most_common():
    if count > 1:
        print(word, count)
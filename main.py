import movie
import spider
import sys
# from threading import Thread, Lock


def get_match_str(str1, str2, str3,str4):
    return 'match (node1:' + str1 + ')-[:' + str2 + ']->(node:' + str3 + ' {name:"' + str4 + '"}) return node1'

def sys_init():
    spider.get_movie_url()
    movie.write_to_database()
    print('init done.')

'''
def get_elems_by_input(url_list : list):
    max_thread_num = 8
    running_thread_num = 0
    # thread_lock = Lock()
    for i in url_list:
        if running_thread_num < max_thread_num:
            thread_lock.acquire()
            Thread(target = spider.get_movie_elems(i)).start()
            running_thread_num += 1
            thread_lock.release()
'''

def match_result_count(match_result : dict, match_list : list):
    for match in match_list:
        if match in match_result.keys():
            match_result[match] += 1
        else:
            match_result[match] = 1

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            if len(sys.argv) > 2:
                print('error! too many arguments')
                exit(1)
            sys_init()
            # thread0 = Thread(target = sys_init)
            # thread0.start()

        elif sys.argv[1] == 'clear':
            if len(sys.argv) > 2:
                print('error! too many arguments')
                exit(1)
            movie.graph.delete_all()
            print('delete all nodes and relationships, done.')
            exit(0)
        
        elif sys.argv[1] == '-f':
            if len(sys.argv) == 2:
                print('error, please input file name!')
                exit(1)
            if len(sys.argv) > 3:
                print('error, too many arguments!')
                exit(1)

            url_file = sys.argv[2]
            url_list = open(url_file, 'r').readlines()
            for url in url_list:
                spider.get_movie_elems(url)
            print('get movie elements, done.')
            movie.write_to_database()
            # thread1 = Thread(target = movie.write_to_database)
            # thread1.start()
            print('write to database, done.')

        elif sys.argv[1] == '-s':
            if len(sys.argv) == 2:
                print('error, please input file name!')
                exit(1)
            if len(sys.argv) > 3:
                print('error, too many arguments!')
                exit(1)

            url = sys.argv[2]
            # print(url)
            spider.get_movie_elems(str(url))
            print('get movie infomation, done.')
            movie.write_to_database()
            # thread1 = Thread(target = movie.write_to_database)
            # thread1.start()
    else:
        print('please input argument')
        print('init        :  使用豆瓣电影top250作为默认数据集构建知识图谱')
        print('-f filename :  爬取filename中的url作为数据集加入到数据库中')
        print('-s urlname  :  爬取指定url到数据并保存到数据库中')

    while(True):
        print('**************************************************************************************')
        print('please input query, entry q or exit to exit.')
        print('use ? to represent result you want, use - to represent null')
        print('please input movie_name  movie_year  movie_director  movie_screenwriter  movie_actor  movie_type  movie_country')
        name = 0
        year = 1
        director = 2
        screenwriter = 3
        actor = 4
        typ = 5
        country = 6
        user_str = input()
        if user_str == 'q' or user_str == 'exit':
            exit(0)

        match_str_list = user_str.split()
        # 如果查询电影名字
        if match_str_list[name] == '?':
            if match_str_list[year] != '-':
                match_result1 = movie.graph.run(get_match_str('movie', '拍摄于', 'year', match_str_list[year]))
            else:
                match_result1 = []

            if match_str_list[director] != '-':
                match_result2 = movie.graph.run(get_match_str('movie', '被导演', 'director', match_str_list[director]))
            else:
                match_result2 = []

            if match_str_list[screenwriter] != '-':
                match_result3 = movie.graph.run(get_match_str('movie', '被编剧', 'screenwriter', match_str_list[screenwriter]))
            else:
                match_result3 = []

            if match_str_list[actor] != '-':
                match_result4 = movie.graph.run(get_match_str('movie', '被主演', 'actor', match_str_list[actor]))
            else:
                match_result4 = []

            if match_str_list[typ] != '-':
                match_result5 = movie.graph.run(get_match_str('movie', '属于', 'type', match_str_list[typ]))
            else:
                match_result5 = []

            if match_str_list[country] != '-':
                match_result6 = movie.graph.run(get_match_str('movie', '拍摄于', 'country', match_str_list[country]))
            else:
                match_result6 = []

            match_result = {}

            # 统计不同查询方式活得的结果，按出现次数输出，某种程度上来说这也是最简单的推荐算法
            match_result_count(match_result, match_result1)
            match_result_count(match_result, match_result2)
            match_result_count(match_result, match_result3)
            match_result_count(match_result, match_result4)
            match_result_count(match_result, match_result5)
            match_result_count(match_result, match_result6)

            sorted(match_result.values(), reverse = True)
            for key in match_result.keys():
                print(key['name'])
                

if __name__ == '__main__':
    main()
import pymysql
import datetime
from pandas import Series,DataFrame
from datetime import datetime
conn = pymysql.connect(host='localhost',user='root',password='pslws5210@',db='music',charset='utf8')
cursor=conn.cursor()

def admin_menu(): #관리자 인터페이스
     command=int(input('1. Register new user \n2. Delete user \n3. Register music/album \n4. Delete music \n5. Show User list \n6. Manage user info-\n7. Terminate\nInput : '))
     if command==1: #유저 생성
         create_user()
     elif command==2:#유저 삭제
         Delete_user()
     elif command==3:#음악 등록 (앨범은 부가적)
         Register_music()
     elif command==4:#음악 삭제
         Delete_music()
     elif command==5:#유저목록 다 보이기
         Show_userlist()
     elif command==6:#유저 정보 변경
         manage_user()
     else:
         return

def manage_user():#유저 정보 변경
    sql='select * from user'
    cursor.execute(sql)
    resultset=cursor.fetchall()
    Result=DataFrame(resultset,columns=["Knickname","ID number",'Password','Name','Sex','Phone number','Birth date'])
    print(Result)

    user_id=input("Input user id to manage : ")
    knickname=input("Knickname : ")
    password=input("Password : ")
    Name= input ("Name : ")
    Sex=input("Sex : ")
    phone_number=input("Phone number : ")
    Birth=input("Birth date : ")
    sql = 'update user set knickname=%s,user_password=%s,user_Name=%s,Sex=%s,phone_number=%s,birth_date=%s where user_id = %s'
    cursor.execute(sql,(knickname,password,Name,Sex,phone_number,Birth,user_id))
    conn.commit()

    admin_menu()

def Show_userlist(): # 모든 유저정보를 출력
    sql='select * from user'
    cursor.execute(sql)
    resultset=cursor.fetchall()
    Result=DataFrame(resultset,columns=["Knickname","ID number",'Password','Name','Sex','Phone number','Birth date'])
    print(Result)
    admin_menu()
     
def Delete_user(): # 특정 유저를 제거
    user_id=int(input("Input user_id to delete : "))
    sql1='Delete from streaming where user=%s'
    cursor.execute(sql1,(user_id))
    conn.commit()
    list_id=[]
    sql2='select list_id from playlist where list_owner=%s'
    cursor.execute(sql2,(user_id))
    resultset=cursor.fetchall()
    for value in resultset:
        list_id.append(value[0])

    for value2 in list_id:
        sql3='delete from list_song where list=%s'
        now_list=value2
        cursor.execute(sql3,(now_list))
        conn.commit()
    
    sql4='Delete from playlist where list_owner=%s'
    cursor.execute(sql4,(user_id))
    conn.commit()
    sql5='delete from user where user_id=%s'
    cursor.execute(sql5,(user_id))
    conn.commit()
    print("Delete Completed....")
    admin_menu()

def Register_music(): # 새로운 음원 등록
    input1=input("Is it a song by existing artist in db??  y/n : ")
    if input1=='y' or input1 == 'Y': # 이미 artist 있음 -> 단순 등록
        artist_id=search_artist_admin()
        song_name=input("Song name : ")
        paly_time=input("Play time : ")
        Registration_date=datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        sql1='insert into song(song_name,play_time,artist,Registration_date) VALUES(%s,%s,%s,%s)'
        cursor.execute(sql1,(song_name,paly_time,artist_id,Registration_date))
       
        conn.commit()
        print("Music Registration Completed....")
        admin_menu()
    elif input1=='n' or input1=='N':
        print("Register Artist first....")
        artist_name=input("Input artist name to register : ")
        sql1='insert into artist(artist_name) values(%s)'
        cursor.execute(sql1,(artist_name))
        conn.commit()
        Register_music()

def Delete_music(): # 음원 제거
    song_name=input("Input song name to delete : ")
    sql1='select song_id,song_name,artist_name from song, artist where song_name=%s and artist=artist_id'
    cursor.execute(sql1,(song_name))
    resultset=cursor.fetchall()
    Result=DataFrame(resultset,columns=['song id','song name','artist'])
    print(Result)
    print('\n')
    song_id=input('Input song id to delete : ')
    sql2='delete from album_song where song=%s'
    cursor.execute(sql2,(song_id))
    conn.commit()
    sql3='delete from list_song where song=%s'
    cursor.execute(sql3,(song_id))
    conn.commit()
    sql4='delete from streaming where song=%s'
    cursor.execute(sql4,(song_id))
    conn.commit()
    sql5='delete from song where song_id=%s'
    cursor.execute(sql5,(song_id))
    conn.commit()
    print('Delete Completed....')

    admin_menu()
    
def search_artist_admin(): # 아티스트 검색 (관리자 전용)
    artist_name=input("Input artist name : ")
    sql1='select artist_id from artist where artist_name=%s'
    cursor.execute(sql1,(artist_name))
    result=cursor.fetchall()
    print(result[0][0])
    return result[0][0]

def user_menu(user_id): # 유저 인터페이스
    # 곡 검색, 앨범 검색, 가수 검색, 
     command=int(input('1. Search Song   \n2. Search Album \n3. Search Artist \n4. Show all song list  \n5. Go to my Playlist  \n6. Show ranking chart\n7. Search Composer \nAny other key to terminate\ninput :  '))
     if command==1: # 곡 검색
        search_and_play_song(user_id)

     elif command==2: # 앨범 검색
         search_album(user_id)

     elif command==3: # 가수검색 -> 곡 목록 or 이력 보여주기
         search_artist(user_id)
     
     elif command==4: # 모든 곡 리스트 보여주기
         show_all(user_id)
    
     elif command==5: # 내 플레이리스트 보기
         view_playlist(user_id)

     elif command==6: # 인기순위 보여주기
         show_ranking(user_id)
     
     elif command==7:
         search_composer(user_id)

     else:
         return

def search_song(user_id): #곡 검색 이후, 곡의 id 값을 반환하는 함수
    name=input('input name of Song to search : ')
    sql='select song_name from song where %s=song_name'
    cursor.execute(sql,(name))
    find_song_album=cursor.fetchall()
    song_album_exist=0
    song_id=99999
    id_list=[]
    for row in find_song_album:
        if(name==row[0]):
            song_album_exist=1
            #UPPER(컬럼명) LIKE UPPER(검색명)
            sql="select ar.artist_name,s.song_name, s.play_time, al.album_name, s.song_id from song as s, album as al, album_song as r, artist as ar where %s = s.song_name and s.song_id=r.song and r.album=al.album_id and s.artist=ar.artist_id "
            cursor.execute(sql,(name))
            resultset=cursor.fetchall()
            for row in resultset:
                id_list.append(row[4])
            Result=DataFrame(resultset,columns=['Artist','Music','Playtime','Album','ID'])
            print(Result)
           
            break

    if song_album_exist==0:
        print("Not founed..  \nCheck the capital again \'%s\'"%name)
        command=input("Press 1 to goback menu, Press 0 to terminate : ")
        if command=='1':
            user_menu(user_id)
        else:
            return
    return id_list
            
def search_and_play_song(user_id): # for viewing list and playing music
    name=input('input name of Song to search : ')
    sql='select song_name from song where %s=song_name'
    cursor.execute(sql,(name))
    find_song_album=cursor.fetchall()
    song_album_exist=0
    song_id=[]
    for row in find_song_album:
        if(name==row[0]):
            song_album_exist=1
            #UPPER(컬럼명) LIKE UPPER(검색명)
            sql="select ar.artist_name,s.song_name, s.play_time, al.album_name, s.song_id from song as s, album as al, album_song as r, artist as ar where %s = s.song_name and s.song_id=r.song and r.album=al.album_id and s.artist=ar.artist_id "
            cursor.execute(sql,(name))
            resultset=cursor.fetchall()
            for row in resultset:
                song_id.append(row[4])
            Result=DataFrame(resultset,columns=['Artist','Music','Playtime','Album','ID'])
            print(Result)
           
            break

    if song_album_exist==0:
        print("Not founed..  \nCheck the capital again \'%s\'"%name)
        command=input("Press 1 to goback menu, Press 0 to terminate : ")
        if command=='1':
            user_menu(user_id)
        else:
            return

    elif song_album_exist==1:
        command=input("Press 1 to play, 2 to go menu, any other keys to terminate : ")
        if command=='1':
            play_song=int(input("input index to play: "))
            play_music(user_id,song_id[play_song],name)
        elif command=='2':
            user_menu(user_id)
        else:
            return

def search_album(user_id): # 앨범 검색
    name=input('input name of Album to search : ')
    sql='select album.album_name from  album where %s=album_name'
    cursor.execute(sql,(name))
    find_song_album=cursor.fetchall()
    song_album_exist=0 
    for row in find_song_album:
        if(name==row[0]):
            song_album_exist=1
            sql='select al.album_name, r.track_num, s.song_name,ar.artist_name,s.play_time from song as s, album as al, album_song as r, artist as ar where %s=al.album_name and al.album_id=r.album and r.song=s.song_id and s.artist=ar.artist_id'
            cursor.execute(sql,(name))
            resultset=cursor.fetchall()
            Result=DataFrame(resultset,columns=['Album','Track num','Music','Artist', 'Playtime'])
            print(Result)
            break

    if song_album_exist==0:
        print("Not founed... \nCheck the capital again \'%s\'"%name)
        command=input("Press 1 to goback menu, Press 0 to terminate : ")
        if command=='1':
            user_menu(user_id)
        else:
            return
    elif song_album_exist==1:
        command=input("Press 1 to goback menu, Press 0 to terminate : ")
        if command=='1':
            user_menu(user_id)
        else:
            return

def search_artist(user_id): # 아티스트 검색
    name=input('Search artist : ')
    sql1='select artist.artist_name from artist where %s=artist_name'
    cursor.execute(sql1,(name))
    find_artist=cursor.fetchall()
    artist_exist=0
    for row in find_artist:
        if(name == row[0]):
            artist_exist=1
            sql2='select artist.artist_name,song.song_name from artist,song where %s=artist.artist_name and artist.artist_id=song.artist'
            cursor.execute(sql2,(name))
            resultset2=cursor.fetchall()
            Result=DataFrame(resultset2,columns=['Artist','Music'])
            print(Result)

            command2=input('If you want to view history of \'%s\'  type history/History : '%name)
            if command2=='history' or command2=='History':
                sql3='select artist_name, content from artist,artist_history where %s=artist_name and artist_id=artist'
                cursor.execute(sql3,(name))
                resultset3=cursor.fetchall()
                Result2=DataFrame(resultset3,columns=['Artist','History'])
                print(Result2)
                break

    if artist_exist==0:
        print("No Artist founed...   Check the capital") 
    
    user_menu(user_id)

def search_composer(user_id): # 작곡가 검색
    name=input('Search composer : ')
    sql1='select composer_name from composer where %s=composer_name'
    cursor.execute(sql1,(name))
    find_composer=cursor.fetchall()
    composer_exist=0
    for row in find_composer:
        print(row[0],name)
        if(name == row[0]):
            composer_exist=1
            sql2='select composer_name,song.song_name from composer,song where %s=composer_name and composer_id=composer'
            cursor.execute(sql2,(name))
            resultset2=cursor.fetchall()
            Result=DataFrame(resultset2,columns=['Composer','Music'])
            print(Result)

            command2=input('If you want to view history of \'%s\'  type history/History : '%name)
            if command2=='history' or command2=='History':
                sql3='select composer_name, content from composer,composer_history where %s=composer_name and composer_id=composer'
                cursor.execute(sql3,(name))
                resultset3=cursor.fetchall()
                Result2=DataFrame(resultset3,columns=['Composer','History'])
                print(Result2)
                break

    if composer_exist==0:
        print("No Artist founed...   Check the capital") 
    
    user_menu(user_id)

def play_music(user_id,song_id,song_name): # 음원 재생
    #streamin : sonng user play time
    sql1='select user, song  from streaming where %s=user and %s= song'
    cursor.execute(sql1,(user_id,song_id))
    streaming_history=cursor.fetchall()
    streaming_exist=0
    for streaming in streaming_history:
        print(streaming[0],streaming[1])
        if(user_id==streaming[0] and song_id==streaming[1]): # 이미 기록이 있음
            streaming_exist=1
            sql='UPDATE streaming set play_time=play_time+1 where user=%s and song=%s'
            cursor.execute(sql,(user_id,song_id))
            conn.commit()
            print('Now Playing \'%s\' ..... ' %song_name)
            break
    if streaming_exist==0: # 처음 플레이한 곡
        sql='insert into streaming(song,user,play_time) values (%s,%s,1)'
        cursor.execute(sql,(song_id,user_id))
        conn.commit()
        print('Now Playing \'%s\' ..... \n' %song_name)

    user_menu(user_id)

def create_playlist(user_id): # 새로운 플레이리스트 생성
    #Date=datetime.today()
    Date= datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    name=input('Input list name : ')
    sql='insert into playlist(list_name,list_owner,create_date) values(%s,%s,%s)'
    cursor.execute(sql,(name,user_id,Date))
    conn.commit()
    view_playlist(user_id)

def view_playlist(user_id): # 플레이리스트 목록을 보여줌
    sql='select list_name,create_date,list_id from playlist where %s =list_owner'
    cursor.execute(sql,(user_id))
    resultset=cursor.fetchall()
    Result=DataFrame(resultset,columns=['Name','Create Date','List ID'])
    print(Result)
    print('\n')
    save_list = []
    for value in (resultset):
       save_list.append(value[2])
       
    command=int(input('Index of playlist. See datail \n119. Create another Playlist \n112. Delete Playlist  \n999. Goback menu  : '))
    if command==119:
        create_playlist(user_id)
    elif command==112:
        delete_list=int(input('Type the number of playlist to delete : '))
        delete_playlist(user_id,save_list[delete_list])
    elif command==999:
        user_menu(user_id)
    else:
        view_detail(user_id,save_list[command])

def view_detail(user_id,list_id): # 특정 플레이리스트의 소장 곡들을 모두 자세히 보여줌
    sql='select list_name,song_name,artist_name,play_time,song_id from playlist,list_song,artist,song where %s=list_owner and %s=list_id and %s=list and song=song_id and artist=artist_id order by list_name'
    cursor.execute(sql,(user_id,list_id,list_id))
    resultset=cursor.fetchall()
    Result = DataFrame(resultset,columns=['List name','Music','Artist','Playtime','Song id num'])
    print(Result)
    save_id=[]
    save_name=[]
    for value in (resultset):
       save_id.append(value[4])
       save_name.append(value[1])

    command=int(input('Index number of music. Play/Delete\n119. add music on this list : '))
    if command==119:
        add_music(user_id,list_id)

    else:
        command2=int(input("111. Delete\n112. Play : "))
        if command2==111:
            delete_from_list(user_id,list_id,save_id[command])
        elif command2==112:
            play_music(user_id,save_id[command],save_name[command])

    user_menu(user_id)

def delete_playlist(user_id,list_id): # 플레이리스트를 제거함
    sql1='delete from list_song where list=%s' #To keep Fk constraint, delete referencing table 'list_song' first
    cursor.execute(sql1,(list_id))
    conn.commit()
    sql2='delete from playlist where list_id=%s'
    print('list id : %s'%list_id)
    cursor.execute(sql2,(list_id))
    conn.commit()

    view_playlist(user_id)

def add_music(user_id,playlist_id): # 플레이리스트에 음원 추가
    result = search_song(user_id)
    index = int(input('Index of the song to add : '))
    song_id=result[index]
    check_sql='select count(*) from list_song where %s=list and %s = song '
    cursor.execute(check_sql,(playlist_id,song_id))
    check_result=cursor.fetchall()
    print(check_result[0][0])
    if check_result[0][0]>0:
        print("It is already in your playlist")
        return
    else:
        sql='insert into list_song(list,song) values(%s,%s)'
        cursor.execute(sql,(playlist_id,song_id))
        conn.commit()
        print('List Updated...')
        return

def delete_from_list(user_id,list_id,song_id): # 플레이리스트에서 곡 삭제
    sql='delete from list_song where list=%s and song=%s'
    cursor.execute(sql,(list_id,song_id))
    conn.commit()
    print("Delete completed.")

def show_all(user_id): # DB 내 모든 음원을 보여줌
    sql='select song_name,play_time,artist_name from song,artist where song.artist=artist_id order by artist_name'
    cursor.execute(sql)
    resultset=cursor.fetchall()
    Result=DataFrame(resultset,columns=['Music','Play time','Artist'])
    print(Result)
    user_menu(user_id)

def show_ranking(user_id): # 각 음원들을 플레이 횟수순으로 나열 (인기차트)
    sql='select song_name,artist_name,s.play_time,sum(st.play_time) from streaming as st, song as s, user as u,artist as a where st.song=s.song_id and st.user=u.user_id and a.artist_id=s.artist group by song_name order by sum(st.play_time) desc'
    cursor.execute(sql)
    resultset=cursor.fetchall()
    Result=DataFrame(resultset,columns=['Music','Artist','Play length','Play_time'])
    print(Result)
    print('\n')
    user_menu(user_id)

def create_user(): # USER 회원가입
    ID=input("input ID : ")
    password1=input("Input Password : ")
    password2=input("Input Password again : ")
    if password1!=password2:
        print("Oops!! Password not Match..\n")
        create_user()
    else:
        name=input("Input name : ")
        Sex=input("Input sex : ")
        phone=input("Input phone number : ")
        birth = input("Input birth date : ") 
        sql='insert into user(knickname, user_password, user_name, sex, phone_number, birth_date) values (%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(ID,password1, name, Sex, phone, birth))
        conn.commit()
        print("Account has successfully created.\nLogin now!!")

def start(): # 프로그램 실행 시 제일 처음 실행되는 함수
    user_type=int(input("Choose usertype\n1. User \n2. Admin\n3. Exit \nInput : "))
    print("\n")
    if user_type==1:
        start_command=int(input("1. Create a new Acccount \n2. Login \nInput : "))
        if start_command==1:
            create_user()
            start()
        else:
            user_id=input('User ID : ')
            user_password=input('Password: ')
            sql='select knickname, user_id,user_password from user'
            cursor.execute(sql)
            resultset=cursor.fetchall()
            correct=0
            id_number=0
            for row in resultset:
              #  print(row[0],row[1])
                if(user_id==row[0] and user_password==row[2]):
                    correct=1
                    id_number=row[1]
                    break
            if correct==1:
                user_menu(id_number)
            else:
                print('User ID or Password is not correct.\nPlease check again\n\n')
                start()

    elif user_type==2:
        correct=0
        admin_id=int(input('Admin ID : '))
        admin_password=input('Password: ')
        sql='select admin_id, admin_password, admin_name from admin'
        cursor.execute(sql)
        resultset=cursor.fetchall()
        for row in resultset:
            if(admin_id==row[0] and admin_password==row[1]):
                correct=1
                name=row[2]
        if correct==1:
            print("Welcome %s" %name)
            admin_menu()
        else:
            print('Admin ID or Password is not correct.\nPlease check again\n\n')
            start()   
    else:
        print('Bye')
        return        

if __name__ == "__main__":
    start()




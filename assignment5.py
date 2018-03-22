import os

infile=open("u.item","r",encoding="iso-8859-1")
infile2=open("u.genre","r",encoding="utf-8")
infile3=open("u.data","r",encoding="utf-8")
infile4=open("u.occupation","r",encoding="utf-8")
infile5=open("u.user","r",encoding="utf-8")
infile6=open("stopwords.txt","r",encoding="utf-8")

os.chdir("film")

movie_id=[]
movie_title=[]
imdb_url=[]
other=[]
dict={} #genresi icin duzenleme
best_dict={} #filmin id,isim,url,reviewsi var

#stage1 step2

user_dict={}
user_meslek_dict={}

#stage1 rating user
rating_dict={}

#rating html icin
total_rate=[]
total_user=[]

#stage2_stopwords
stopwords=[]
unknown,Action,Adventure,Animation,Childrens,Comedy,Crime,Documentary,Drama,Fantasy,FilmNoir,Horror,Musical,Mystery,Romance,SciFi,Thriller,War,Western=set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set(),set()

guess_title=[]
guess_reviews=[]


movie_title=[]
movie_reviews=[]

for film in os.listdir(os.getcwd()):
    f = open(film, "r")
    all_file=[]
    all_file_2=[]
    for line in f.readlines():
        aline=line.rstrip("\n").split("\n")
        bline=line.split("\n")
        all_file.append(aline[0])
        all_file_2.append(bline[0])
    movie_title.append(all_file[0].split("(")[0].lower())
    movie_reviews.append(all_file_2[1:len(all_file_2)])

acx=[]
for line in infile.readlines():
    line=line.rstrip("\n").split("|")
    acx.append(line)

for i in movie_title:
    for x in range(len(acx)):
        if i in acx[x][1].lower():
            movie_id.append(acx[x][0])
            imdb_url.append(acx[x][3])
            other.append(acx[x][4:len(line)])

for line in infile2:
    line=line.strip("\n").split("|")
    dict[line[1]]=line[0]

movie_genre=set()
for i in movie_title:
    a=movie_title.index(i)
    genre_finder=set()
    c=0
    cv=other[a].count("1")
    for x in other[a]:
        for ghj in range(cv):
            if x == "1":
                genre_finder.add(dict[str(c)])
            if len(genre_finder) == cv:
                 best_dict[i]=movie_id[a],movie_title[a],imdb_url[a],genre_finder,movie_reviews[a]
        c += 1

# html zamani
# best_dict= id,title,url,genre,reviews



#user zamani

for line in infile4.readlines():
    line=line.rstrip("\n").split("|")
    user_meslek_dict[line[0]]=line[1]


#dict[id]=id-age-gender-occupation-zip
for line in infile5.readlines():
    line=line.rstrip("\n").split("|")
    user_dict[line[0]]=line[0],line[1],line[2],user_meslek_dict[line[3]],line[4]


#rating dict
#dict[userid]=userid,filmid,rating

for line in infile3.readlines():
    line=line.strip("\n").split()
    a=[user_dict[line[0]],line[1],line[2]]
    if not line[1] in rating_dict.keys():
        rating_dict[line[1]]=list(a)
        b=rating_dict[line[1]][0:3]
        rating_dict[line[1]][0]=b
        rating_dict[line[1]].pop(1)
        rating_dict[line[1]].pop(1)
    else:
        rating_dict[line[1]].append(a)


for i in movie_id:
    total=0
    counter=0
    for x in range(len(rating_dict[i])):

        a=int(rating_dict[i][x][2])
        total += a
        counter += 1
    total_user.append(str(counter))
    total_rate.append(str(total/counter))


os.chdir("..")
os.mkdir("filmList")
os.chdir("filmList")

for i in movie_title:
    a=movie_title.index(i)
    idb=movie_id[a]
    outfile=open(movie_id[a]+".html","w")
    outfile.write("""
    <html><head><meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    <title> """+movie_title[a].title()+""" </title>
    </head>
    <body>
    <font face="Times New Roman" font="" size="6" color="red" <b="">"""+movie_title[a].title()+"""</font><br>
    <b>Genre: </b>"""+" ".join(best_dict[str(i)][3])+""" <br>
    <b>IMDB Link: </b><a href=" """+imdb_url[a]+""" ">"""+movie_title[a].title()+"""</a><br>
    <font face="Times New Roman" font="" size="4" color="black"><b>Review:</b><br>{}
    </font><br><br>
    <b>Total User: </b>{} / <b>Total Rate: </b>{}<br>
    <br><b>User who rate the film: </b>
    """.format("".join(movie_reviews[a]),total_user[a],total_rate[a]))
    for xj in range(len(rating_dict[str(idb)])):
        if idb == rating_dict[str(idb)][xj][1]:
            string=("""<br><b>User: </b> {} <b> Rate: </b> {} <br>
                <b>User Detail: </b> <b>Age: </b> {}  <b>Gender:</b> {}  <b>Occupation:</b> {} <b>Zip Code:</b> {}
                </body></html>""".format(rating_dict[str(movie_id[a])][xj][0][0],rating_dict[str(movie_id[a])][xj][2],rating_dict[str(movie_id[a])][xj][0][1],rating_dict[str(movie_id[a])][xj][0][2],rating_dict[str(movie_id[a])][xj][0][3],rating_dict[str(movie_id[a])][xj][0][4]))

            outfile.write(string)
os.chdir("..")



#stage 2#####################

for line in infile6.readlines():
    line=line.strip("\n").split("\n")
    stopwords.append(line)

temiz_set=set()

for i in movie_title:
    a=movie_title.index(i)
    b = "".join(movie_reviews[a])
    movie_reviews[a].clear()
    movie_reviews[a].append(b)


#review.txt

outfile_review=open("reviews.txt","w",encoding="utf-8")

for i in range(len(acx)):
    counter_reviews=0
    for y in movie_title:
        inx=movie_title.index(y)
        if acx[i][0] == movie_id[inx]:
                outfile_review.write("{} {} is found in folder \n".format(movie_id[inx],movie_title[inx].split("(")[0].title()))
                counter_reviews += 1
    if counter_reviews == 0:
        outfile_review.write("{} {} is not found in folder. Look at {}\n".format(acx[i][0],acx[i][1].split("(")[0],acx[i][3]))

def kume_add(arg1,arg2):
    for i in arg1:
        arg2.add(i)
    return arg2


for index_can in movie_title:
    index_adam=movie_title.index(index_can)
    guess_set=set()
    a_set=set()
    b_set=set()
    for j in range(len(stopwords)):
            b_set.add("".join(stopwords[j]))
    for i_guess in movie_reviews[index_adam]:
        a_guess=i_guess.split()
        for k in range(len(a_guess)):
            a_set.add(a_guess[k])
    c_set=a_set.difference(b_set)
    if "Drama" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Drama)
    if "Action" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Action)
    if "Adventure" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Adventure)
    if "Animation" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Animation)
    if "Children's" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Childrens)
    if "Comedy" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Comedy)
    if "Crime" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Crime)
    if "Documentary" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Documentary)
    if "Fantasy" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Fantasy)
    if "Film-Noir" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,FilmNoir)
    if "Horror" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Horror)
    if "Musical" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Musical)
    if "Mystery" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Mystery)
    if "Romance" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Romance)
    if "Sci-Fi" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,SciFi)
    if "Thriller" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Thriller)
    if "War" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,War)
    if "Western" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,Western)
    if "unknown" in best_dict[str(movie_title[index_adam])][3]:
        kume_add(c_set,unknown)


#stage 2
os.chdir("filmGuess")
for guess_film in os.listdir(os.getcwd()):
    f = open(guess_film, "r",encoding="cp1252")
    all_file=[]
    all_file_2=[]
    for line in f.readlines():
        aline=line.rstrip("\n").split("\n")
        bline=line.split("\n")
        all_file.append(aline[0])
        all_file_2.append(bline[0])
    guess_title.append(all_file[0].split("(")[0].upper())
    guess_reviews.append(all_file_2[1:len(all_file_2)])
os.chdir("..")

outfile_guess=open("filmGenre.txt","w",encoding="utf-8")
outfile_guess.write("Guess Genres of Movie based on Movies\n")

def yazici(xyx):

    outfile_guess.write(xyx)
    return outfile_guess

guess_genre=[]
for index_guess in guess_title:
    index_guess_number=guess_title.index(index_guess)
    a_set=set()
    b_set=set()
    for j in range(len(stopwords)):
            b_set.add("".join(stopwords[j]).lower())
    for i_guess in guess_reviews[index_guess_number]:
        a_guess=i_guess.split()
        for k in range(len(a_guess)):
            a_set.add(a_guess[k].lower())
    c_set=a_set.difference(b_set)
    if len(c_set.intersection(unknown)) >= 20:
        guess_genre.append("unknown")
    if len(c_set.intersection(Action)) >= 20:
        guess_genre.append("Action")
    if len(c_set.intersection(Adventure)) >= 20:
        guess_genre.append("Adventure")
    if len(c_set.intersection(Animation)) >= 20:
        guess_genre.append("Animation")
    if len(c_set.intersection(Childrens)) >= 20:
        guess_genre.append("Children's")
    if len(c_set.intersection(Comedy)) >= 20:
        guess_genre.append("Comedy")
    if len(c_set.intersection(Crime)) >= 20:
        guess_genre.append("Crime")
    if len(c_set.intersection(Documentary)) >= 20:
        guess_genre.append("Documentary")
    if len(c_set.intersection(Drama)) >= 20:
        guess_genre.append("Drama")
    if len(c_set.intersection(Fantasy)) >= 20:
        guess_genre.append("Fantasy")
    if len(c_set.intersection(FilmNoir)) >= 20:
        guess_genre.append("Film-Noir")
    if len(c_set.intersection(Horror)) >= 20:
        guess_genre.append("Horror")
    if len(c_set.intersection(Musical)) >= 20:
        guess_genre.append("Musical")
    if len(c_set.intersection(Mystery)) >= 20:
        guess_genre.append("Mystery")
    if len(c_set.intersection(Romance)) >= 20:
        guess_genre.append("Romance")
    if len(c_set.intersection(SciFi)) >= 20:
        guess_genre.append("Sci-Fi")
    if len(c_set.intersection(Thriller)) >= 20:
        guess_genre.append("Thriller")
    if len(c_set.intersection(War)) >= 20:
        guess_genre.append("War")
    if len(c_set.intersection(Western)) >= 20:
        guess_genre.append("Western")
    a=(guess_title[index_guess_number]+": "+" ".join(guess_genre)+"\n")
    yazici(a)
    guess_genre.clear()


outfile_guess.close()
outfile_review.close()
outfile.close()

from flask import Flask, request, render_template, session, redirect, url_for, flash, make_response
import os
import maze_generator
import graph
import time

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY = 'dev')
DB_FILE = "main.db"
import db

FINAL = []

@app.route("/")
def index():
    if not os.path.exists(DB_FILE):
        db.createDatabase()
    resp = make_response(render_template('index.html'))
    resp.headers = {"Access-Control-Allow-Origin": "*"}
    return resp

@app.route("/", methods=['POST'])
def login():
    if not os.path.exists(DB_FILE):
        db.createDatabase()
    con = db.getDatabase()

    username = request.form.get('username')
    error = None
    if username is None:
        error = 'Incorrect username.'

    if error is None:
        session.clear()

        cur = con.cursor()
        cur.execute("SELECT username FROM users WHERE username=?", (username,))
        value = cur.fetchone()
        if not value:
            cur.execute("INSERT INTO users (username) VALUES(?)", (username,))
        con.commit()
        con.close()

        response = make_response(redirect(url_for('maze')))
        response.set_cookie('username', username)
        return response
        
    flash(error)

    return username, 201, {"Access-Control-Allow-Origin": "*"}

@app.route("/maze")
def maze():
    if not os.path.exists(DB_FILE):
        db.createDatabase()
    username = request.cookies.get('username')
    error = 'error'
    con = db.getDatabase()
    cur = con.cursor()
    cur.execute("SELECT username FROM users WHERE username=?", (username,))
    value = cur.fetchone()
    if value is not None:
        value = value[0]
        cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        user_id = int(cur.fetchone()[0])
        #print(user_id, time.time())
        cur.execute("INSERT INTO scores (user_id, start_time) VALUES(?, ?)", (user_id, time.time(),))
    cur.execute("SELECT users.username, time FROM scores JOIN users ON users.user_id = scores.user_id ORDER BY time ASC")
    li = cur.fetchall()
    con.commit()
    con.close()

    if value == username:
        error = None

    if error is not None:
        return redirect(url_for('index'))

    scores = []
    n = 1
    #print(li)
    for i in li:
        if i[1] != None:
            temp = str(n) + ". @" + str(i[0]) + " with score: " + str(round(i[1],2))
            scores.append(temp)
            n += 1

            if n == 10:
                break

    #print(scores)
    if scores == []:
        scores = ["There are currently no top ten scores."]

    maze = maze_generator.make_maze(10, 10)
    maze_list = []
    buttons = []

    string = ""
    for i in maze:
        if i == '\n':
            maze_list.append(string)
            string = ""
        else:
            string += i

    for row in maze_list:
        A = []
        for i in row:
            if i == '█':
                A.append('wall')
            elif i == ' ':
                A.append('path')
        buttons.append(A)

    #print(maze)
    resp = make_response(render_template('maze.html', username = username, scores = scores, buttons = buttons))
    #resp.set_cookie('username', username)
    #resp.headers = {"Access-Control-Allow-Origin": "*"}
    return resp

@app.route("/completemaze", methods=['GET'])
def maze_completed():
    return FINAL[len(FINAL)-1], {"Access-Control-Allow-Origin": "*"}

@app.route("/maze", methods=['POST'])
def maze_posted():
    A_ = request.form['name']
    A = []
    word = ''

    for i in A_:
        if i != ',':
            word += i
        else:
            A.append(word)
            word = ''

    option = A[0]
    A.pop(0)
    username = A[0]
    username = username[1:]
    A.pop(0)
    new = [[]]

    row = 0
    for i in A:
        if i == '\n':
            row += 1
            new.append([])
        else:
            new[row].append(i)
    new.pop(len(new)-1)

    resp = make_response(redirect(url_for('maze')))
    resp.headers = {"Access-Control-Allow-Origin": "*"}
    m = graph.Graph(len(A))

    start = 0
    end = 0
    v = 0
    length = len(new)
    
    if option == 'generate':
        #con = db.getDatabase()
        #cur = con.cursor()
        #cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        #value = cur.fetchone()
        #cur.execute("INSERT user_id, start_time FROM scores (user_id, start_time) VALUES(?, ?)", (value[0],time.time(),))
        #con.close()

        con = db.getDatabase()
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        user_id = int(cur.fetchone()[0])
        cur.execute("SELECT score_id FROM scores WHERE user_id=? ORDER BY score_id DESC LIMIT 1", (user_id,))
        score_id = int(cur.fetchone()[0])
        cur.execute("SELECT start_time, end_time FROM scores WHERE user_id=? ORDER BY score_id DESC LIMIT 1", (user_id,))
        times = cur.fetchall()[0]
        start_time = times[0]
        end_time = times[1]
        if end_time is None:
            cur.execute("DELETE FROM scores WHERE user_id=? AND score_id=?", (user_id, score_id,))
        con.commit()
        con.close()
        
        return resp, 304
    elif option == 'complete':
        for row in range(len(new)-1):
            for i in range(length):
                if new[row][i] != 'wall':
                    if i == 0:
                        start = v
                    else:
                        if i == length-1:
                            end = v
                        if new[row+1][i] != 'wall':
                            m.addEdge(v, v+length)
                            m.addEdge(v+length, v)
                        if new[row][i-1] != 'wall':
                            m.addEdge(v-1, v)
                            m.addEdge(v, v-1)
                v += 1
    elif option == 'check':
        con = db.getDatabase()
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        user_id = int(cur.fetchone()[0])
        cur.execute("SELECT score_id FROM scores WHERE user_id=? ORDER BY score_id DESC LIMIT 1", (user_id,))
        score_id = int(cur.fetchone()[0])
        cur.execute("UPDATE scores SET end_time=? WHERE user_id=? AND score_id=?", (time.time(), user_id, score_id,))
        con.commit()
        con.close()

        for row in range(len(new)-1):
            for i in range(length):
                if new[row][i] != 'wall':
                        if i == 0:
                            start = v
                        else:
                            if i == length-1:
                                end = v
                            if new[row][i] == 'path clicked':
                                if new[row+1][i] != 'wall':
                                    m.addEdge(v, v+length)
                                    m.addEdge(v+length, v)
                                if new[row][i-1] != 'wall':
                                    m.addEdge(v-1, v)
                                    m.addEdge(v, v-1)
                v += 1


    path = m.findPath(start, end)

    if option == 'complete':
        FINAL.append([])

        for i in A:
            if i != '\n':
                FINAL[len(FINAL)-1].append(i)
        
        for i in range(len(FINAL[len(FINAL)-1])):
            for p in path:
                if i == p:
                    FINAL[len(FINAL)-1][i] = 'final'

        con = db.getDatabase()
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        user_id = int(cur.fetchone()[0])
        cur.execute("SELECT score_id FROM scores WHERE user_id=? ORDER BY score_id DESC LIMIT 1", (user_id,))
        score_id = int(cur.fetchone()[0])
        cur.execute("DELETE FROM scores WHERE user_id=? AND score_id=?", (user_id, score_id,))
        con.commit()
        con.close()

        return "success", {"Access-Control-Allow-Origin": "*"}
    elif option == 'check':
        print(path)
        con = db.getDatabase()
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        user_id = int(cur.fetchone()[0])
        cur.execute("SELECT score_id FROM scores WHERE user_id=? ORDER BY score_id DESC LIMIT 1", (user_id,))
        score_id = int(cur.fetchone()[0])
        cur.execute("SELECT start_time, end_time FROM scores WHERE user_id=? ORDER BY score_id DESC LIMIT 1", (user_id,))
        times = cur.fetchall()[0]
        start_time = times[0]
        end_time = times[1]
        if path:
            cur.execute("UPDATE scores SET time=? WHERE user_id=? AND score_id=?", (end_time-start_time, user_id, score_id,))
            con.commit()
            con.close()
            return {'value': "success"}, {"Access-Control-Allow-Origin": "*"}
        else:
            cur.execute("DELETE FROM scores WHERE user_id=? AND score_id=?", (user_id, score_id,))
            con.commit()
            con.close()
            return {'value': "failed"}, {"Access-Control-Allow-Origin": "*"}

def run():
    app.run(port=8080, debug=True)

if __name__ == "__main__":
    run()

# flask --app server run
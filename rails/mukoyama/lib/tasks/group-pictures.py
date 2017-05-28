#! /usr/bin/python3 -u

# rubyでやりたかったが、rubyのループ内でpythonを呼び出すと異様に遅いので再実装

# Returns the similarity of 2 images.

import cv2, datetime, MySQLdb, os, re, sys

DEBUG = False

channels = [0]
histSize = [256]
mask = None
ranges = [0,256]

def compare_hist(p1,p2):
    global channels, histSize, mask, ranges
    i1 = cv2.imread(p1,0)
    i2 = cv2.imread(p2,0)
    h1 = cv2.calcHist([i1], channels, mask, histSize, ranges)
    h2 = cv2.calcHist([i2], channels, mask, histSize, ranges)
    method = cv2.HISTCMP_CORREL
    return cv2.compareHist(h1, h2, method)

def clear(raspi_id):
    db = MySQLdb.connect("localhost","ubuntu","","mukoyama_development")
    cur = db.cursor()
    sql = "delete from picture_groups where raspi_id = %d" % (raspi_id)
    if DEBUG: print(sql)
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()

def filename2seq(name):
    m = re.match("([0-9]{12}).jpg",name.replace("_",""))
    if m == None: return None
    return int(m.group(1))

def seq2filepath(basedir,seq):
  n = str(seq)
  return basedir+"/"+n[0:6]+"_"+n[6:12]+".jpg"

def similar(p1,p2):
  # TODO: アルゴリズム色々切り替えられたら面白そう
  # これは10分単位でまとめる場合
  # p1 / 1000 == p2 / 1000

  # ヒストグラムの類似度
  ret = compare_hist(p1,p2)
  if DEBUG: print(p1+" "+p2+" "+str(ret))
  return ret > 0.95

def update(raspi_id):
    db = MySQLdb.connect("localhost","ubuntu","","mukoyama_development")
    cur = db.cursor()
    cur.execute("select count(1) from picture_groups where raspi_id = %d" % (raspi_id))
    n_before = cur.fetchone()[0]
    cur.execute("select max(head) from picture_groups where raspi_id = %d" % (raspi_id))
    res = cur.fetchone()
    if res[0] == None: start = 0
    else: start = res[0]
    print("start=%d" % (start))
    basedir = "/opt/mukoyama.lmlab.net/data/pictures/%d" % (raspi_id)
    if not os.path.isdir(basedir): raise Exception('%s not found.' % (basedir))
    pictures = []
    for f in sorted(os.listdir(basedir)):
        p = filename2seq(f)
        if p == None or p <= start: continue
        pictures += [p]
    if len(pictures) == 0: return
    print("%d pictures(on %s) will be processed." % (len(pictures),basedir))
    tail = pictures[0]
    n = 0
    ts =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i in range(0,len(pictures) - 1):
        p = pictures[i]
        p_next = pictures[i+1]
        n += 1
        if similar(seq2filepath(basedir,p),seq2filepath(basedir,p_next)): continue
        sql = "insert into picture_groups (raspi_id,head,tail,n,created_at,updated_at) values (%d,%d,%d,%d,'%s','%s')" % (raspi_id,p,tail,n,ts,ts)
        if DEBUG: print(sql)
        cur.execute(sql)
        n = 0
        tail = p_next
    sql = "insert into picture_groups (raspi_id,head,tail,n,created_at,updated_at) values (%d,%d,%d,%d,'%s','%s')" % (raspi_id,pictures[-1],tail,n,ts,ts)
    cur.execute(sql)
    db.commit()
    cur.execute("select count(1) from picture_groups where raspi_id = %d" % (raspi_id))
    n_after = cur.fetchone()[0]
    print("%d rows inserted for raspi_id = %d." % (n_after-n_before,raspi_id))
    cur.close()
    db.close()

if __name__ == "__main__":
    clear(1)
    update(1)
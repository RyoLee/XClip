#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import hashlib
import sqlite3
import sys


def get_md5(s0):
    m = hashlib.md5()
    m.update(bytes(str(s0), encoding="utf-8"))
    return m.hexdigest()


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    un_hash = get_md5(username)
    pw_hash = get_md5(password)
    conn = sqlite3.connect("/config/data.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO USERS(id,name,passowrd,flag) VALUES (?,?,?,1)",
        [un_hash, username, pw_hash],
    )
    conn.commit()
    conn.close()

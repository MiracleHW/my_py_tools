# -*- coding: utf-8 -*-
# File  : sql.py
# Author: huwei
# Date  : 2021/3/24

import pymysql
import os
from dataclasses import asdict


__all__ = ["DbManager","Dbtools"]

class DbManager:
    # 构造函数
    def __init__(self, host, port, user, passwd, db,charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                        charset=self.charset)
        except:
            print("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None, commit=True, ):
        # 连接数据库
        res = self.connectDatabase()
        if not res:
            return False

        if self.conn and self.cur:
            # 正常逻辑，执行sql，提交操作
            rowcount = self.cur.execute(sql, params)
            # print(rowcount)
            if commit:
                self.conn.commit()
            else:
                pass

        return rowcount

    def executemany(self, sql, params=None, commit=True, ):
        # 连接数据库
        res = self.connectDatabase()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.executemany(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except Exception as es:
            print(es)
            print("execute failed: " + sql)
            # logger.error("params: " + str(params))
            self.close()
            return False
        return rowcount

    def get_id(self):
        return self.cur.lastrowid

    # 查询所有数据
    def fetchall(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            print("查询失败")
            return False
        # self.close()
        results = self.cur.fetchall()
        # logger.info("查询成功" + str(results))
        return results

    # 查询一条数据
    def fetchone(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            print("查询失败")
            return False
        # self.close()
        result = self.cur.fetchone()
        # logger.info("查询成功" + str(result))
        return result

    # 增删改数据
    def edit(self, sql, params=None):
        res = self.execute(sql, params, True)
        if not res:
            print("操作失败")
            return False
        self.conn.commit()
        self.close()
        print("操作成功" + str(res))
        return res

class Dbtools():
    def __init__(self,*args,**kargs):
        self.db=DbManager(*args,**kargs)
        if "db" in kargs.keys():
            self.set_db(kargs["db"])

    def set_db(self,db_name):
        sql=f"use {db_name}"
        self.db.execute(sql)

    def build_table(self,target_dir="",recover=False):
        sql=f"select table_name from information_schema.tables where table_schema='{self.db_name}'"
        table_name=self.db.fetchall(sql)

        file_path=os.path.join(target_dir,f"{self.db_name}.py")
        init_file=os.path.join(target_dir,"__init__.py")

        # build __init__.py file
        if len(target_dir)>0 and ( not os.path.exists(init_file) or recover ):
            with open(init_file,"w") as f:
                f.writelines("\n")

        # build {db_name}.py file
        if not os.path.exists(file_path) or recover:
            with open(file_path,"w") as f:
                f.writelines("from dataclasses import dataclass\nfrom typing import Any\n\n")
                for t in table_name:
                    t=t[0]
                    f.writelines("@dataclass\n")
                    f.writelines(f"class {t}():\n")
                    part_name_sql=f"select column_name,column_comment,data_type,column_type from information_schema.columns where table_name='{t}' and TABLE_SCHEMA='{self.db_name}'"
                    part_name=self.db.fetchall(part_name_sql)
                    for p in part_name:
                        f.writelines(f"    {p[0]}: Any=None # {p[1]}\n")
                    f.writelines(f"    table_name='{t}'\n")
                    f.writelines(f"\n")

    def select(self,table,condition=None):
        ins=table()
        ins_dict=asdict(ins)

        keys=list(ins_dict.keys())
        select_str=",".join(keys)

        sql=f"select {select_str} from {ins.table_name}"

        if condition is not None:
            sql+=" where "+condition

        res=self.db.fetchall(sql)
        final=[]
        if res is not False:
            for r in res:
                rdict={k:v for k,v in zip(keys,r)}
                final.append(table(**rdict))
        return final

    def insert(self,data,condition=None):
        data_dict=asdict(data)
        data_keys=list(data_dict.keys())
        data_keys=[x for x in data_keys if data_dict[x] is not None]

        insert_str=",".join([f"`{x}`" for x in data_keys])
        values=[data_dict[x] for x in data_keys]

        sql=f"insert into {data.table_name} ({insert_str}) values("+",".join(["%s"]*len(values))+")"
        if condition is not None:
            sql+=" where "+condition
        return self.db.execute(sql,params=values)

    def update(self,data,condition=None):
        data_dict=asdict(data)

        data_keys = list(data_dict.keys())
        data_keys = [x for x in data_keys if data_dict[x] is not None]

        update_str = ",".join([f"{x}=%s" for x in data_keys])
        values = [data_dict[x] for x in data_keys]
        sql = f"update {data.table_name} set {update_str}"

        if condition is not None:
            sql+=" where "+condition
        return self.db.execute(sql,params=values)

    def fetchall(self,sql,params=None):
        return self.db.fetchall(sql,params)

    def execute(self,sql,params=None):
        return self.db.execute(sql,params)
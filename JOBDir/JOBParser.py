import numpy as np
import json
import os
import psycopg2

class PGConfig:
    def __init__(self,):
        self.config = {}
        self.config["work_mem"] = 4*1024*1024
        self.config["effective_cache_size"] = 16*1024*1024
        self.config["random_page_cost"] = 4
        self.config["cpu_tuple_cost"] = 0.01
        self.config["cpu_index_tuple_cost"] = 0.005
        self.config["cpu_operator_cost"] = 0.0025
        self.config["seq_page_cost"] = 1
        self.config["max_parallel_workers_per_gather"] = 0
        self.config["max_parallel_workers"] = 0
        self.config["parallel_setup_cost"] = 1000
        self.config["parallel_tuple_cost"] = 0.1
        self.config["jit"] = "off"
        self.config["jit_above_cost"] = 100000
        self.config["jit_optimize_above_cost"] = 100000
        self.config["jit_inline_above_cost"] = 100000
        self.config["jit_dump_bitcode"] = "off"
        self.config["jit_expressions"] = "on"
        self.config["jit_profiling_support"] = "off"
        self.config["jit_profiling_save"] = "off"
        self.config["jit_above_cost"] = 100000
        self.config["jit_optimize_above_cost"] = 100000
        self.config["jit_inline_above_cost"] = 100000
        self.config["jit_dump_bitcode"] = "off"
        self.config["jit_expressions"] = "on"
        self.config["jit_profiling_support"] = "off"
        self.config["jit_profiling_save"] = "off"
        self.config["jit_provider"] = "llvmjit"
        self.config["jit_flags"] = "all"
        self.config["jit_debugging_support"] = "off"
        self.config["jit_dump_bitcode"] = "off"
        self.config["jit_above_cost"] = 100000
        self.config["jit_optimize_above_cost"] = 100000
        self.config["jit_inline_above_cost"] = 100000
        self.config["jit_dump_bitcode"] = "off"
        self.config["jit_expressions"] = "on"
        self.config["jit_profiling_support"] = "off"
        
    def __str__(self,):
        return json.dumps(self.config, sort_keys=True, indent=4)
    
    def __getitem__(self, key):
        return self.config[key]
    
    def __setitem__(self, key, value):
        self.config[key] = value

class PGUtils:
    class Expr:
        def __init__(self, expr,list_kind = 0):
            self.expr = expr
        self.list_kind = list_kind
        self.isInt = False
        self.val = 0

        #         print(self.expr)
    def isCol(self,):
        return isinstance(self.expr, dict) and "ColumnRef" in self.expr

    def getValue(self, value_expr):
        if "A_Const" in value_expr:
            value = value_expr["A_Const"]["val"]
            if "String" in value:
                return "'" + value["String"]["str"]+"\'"
            elif "Integer" in value:
                self.isInt = True
                self.val = value["Integer"]["ival"]
                return str(value["Integer"]["ival"])
            else:
                raise "unknown Value in Expr"
        elif "TypeCast" in value_expr:
            if len(value_expr["TypeCast"]['typeName']['TypeName']['names'])==1:
                return value_expr["TypeCast"]['typeName']['TypeName']['names'][0]['String']['str']+" '"+value_expr["TypeCast"]['arg']['A_Const']['val']['String']['str']+"'"
            else:
                if value_expr["TypeCast"]['typeName']['TypeName']['typmods'][0]['A_Const']['val']['Integer']['ival']==2:
                    #                     print(value_expr["TypeCast"]['typeName']['TypeName']['names'][1]['String']['str'])
                    return value_expr["TypeCast"]['typeName']['TypeName']['names'][1]['String']['str']+" '"+value_expr["TypeCast"]['arg']['A_Const']['val']['String']['str']+ "' month"
                else:
                    return value_expr["TypeCast"]['typeName']['TypeName']['names'][1]['String']['str']+" '"+value_expr["TypeCast"]['arg']['A_Const']['val']['String']['str']+ "' year"
        else:
            print(value_expr.keys())
            raise "unknown Value in Expr"
        

    def getAliasName(self,):
        return self.expr["ColumnRef"]["fields"][0]["String"]["str"]

    def getColumnName(self,):
        return self.expr["ColumnRef"]["fields"][1]["String"]["str"]

    def __str__(self,):
        if self.isCol():
            return self.getAliasName()+"."+self.getColumnName()
        elif isinstance(self.expr, dict) and "A_Const" in self.expr:
            return self.getValue(self.expr)
        elif isinstance(self.expr, dict) and "TypeCast" in self.expr:
            return self.getValue(self.expr)
        elif isinstance(self.expr, list):
            if self.list_kind == 6:
                return "("+",\n".join([self.getValue(x) for x in self.expr])+")"
            elif self.list_kind == 10:
                return " AND ".join([self.getValue(x) for x in self.expr])
            else:
                raise "list kind error"

        else:
            raise "No Known type of Expr"


class TargetTable:
    def __init__(self, target):
        """
        {'location': 7, 'name': 'alternative_name', 'val': {'FuncCall': {'funcname': [{'String': {'str': 'min'}}], 'args': [{'ColumnRef': {'fields': [{'String': {'str': 'an'}}, {'String': {'str': 'name'}}], 'location': 11}}], 'location': 7}}}
        """
        self.target = target
    #         print(self.target)

    def getValue(self,):
        columnRef = self.target["val"]["FuncCall"]["args"][0]["ColumnRef"]["fields"]
        return columnRef[0]["String"]["str"]+"."+columnRef[1]["String"]["str"]

    def __str__(self,):
        try:
            return self.target["val"]["FuncCall"]["funcname"][0]["String"]["str"]+"(" + self.getValue() + ")" + " AS " + self.target['name']
        except:
            if "FuncCall" in self.target["val"]:
                return "count(*)"
            else:
                return "*"

class FromTable:
    def __init__(self, from_table):
        """
        {'alias': {'Alias': {'aliasname': 'an'}}, 'location': 168, 'inhOpt': 2, 'relpersistence': 'p', 'relname': 'aka_name'}
        """
        self.from_table = from_table

    def getFullName(self,):
        return self.from_table["relname"]

    def getAliasName(self,):
        return self.from_table["alias"]["Alias"]["aliasname"]

    def __str__(self,):
        return self.getFullName()+" AS "+self.getAliasName()


class Comparison:
    def __init__(self, comparison):
        self.comparison = comparison
        self.column_list = []
        if "A_Expr" in self.comparison:
            self.lexpr = Expr(comparison["A_Expr"]["lexpr"])
            self.kind = comparison["A_Expr"]["kind"]
            if not "A_Expr" in comparison["A_Expr"]["rexpr"]:
                self.rexpr = Expr(comparison["A_Expr"]["rexpr"],self.kind)
            else:
                self.rexpr = Comparison(comparison["A_Expr"]["rexpr"])

            self.aliasname_list = []

            if self.lexpr.isCol():
                self.aliasname_list.append(self.lexpr.getAliasName())
                self.column_list.append(self.lexpr.getColumnName())

            if self.rexpr.isCol():
                self.aliasname_list.append(self.rexpr.getAliasName())
                self.column_list.append(self.rexpr.getColumnName())

            self.comp_kind = 0
        elif "NullTest" in self.comparison:
            self.lexpr = Expr(comparison["NullTest"]["arg"])
            self.kind = comparison["NullTest"]["nulltesttype"]

            self.aliasname_list = []

            if self.lexpr.isCol():
                self.aliasname_list.append(self.lexpr.getAliasName())
                self.column_list.append(self.lexpr.getColumnName())
            self.comp_kind = 1
        else:
            #             "boolop"
            self.kind = comparison["BoolExpr"]["boolop"]
            self.comp_list = [Comparison(x)
                              for x in comparison["BoolExpr"]["args"]]
            self.aliasname_list = []
            for comp in self.comp_list:
                if comp.lexpr.isCol():
                    self.aliasname_list.append(comp.lexpr.getAliasName())
                    self.lexpr = comp.lexpr
                    self.column_list.append(comp.lexpr.getColumnName())
                    break
            self.comp_kind = 2
    def isCol(self,):
        return False
    def __str__(self,):

        if self.comp_kind == 0:
            Op = ""
            if self.kind == 0:
                Op = self.comparison["A_Expr"]["name"][0]["String"]["str"]
            elif self.kind == 7:
                if self.comparison["A_Expr"]["name"][0]["String"]["str"]=="!~~":
                    Op = "not like"
                else:
                    Op = "like"
            elif self.kind == 6:
                Op = "IN"
            elif self.kind == 10:
                Op = "BETWEEN"
            else:
                import json
                print(json.dumps(self.comparison, sort_keys=True, indent=4))
                raise "Operation ERROR"
            return str(self.lexpr)+" "+Op+" "+str(self.rexpr)
        elif self.comp_kind == 1:
            if self.kind == 1:
                return str(self.lexpr)+" IS NOT NULL"
            else:
                return str(self.lexpr)+" IS NULL"
        else:
            res = ""
            for comp in self.comp_list:
                if res == "":
                    res += "( "+str(comp)
                else:
                    if self.kind == 1:
                        res += " OR "
                    else:
                        res += " AND "
                    res += str(comp)
            res += ")"
            return res

class Table:
    def __init__(self, table_tree):
        self.name = table_tree["relation"]["RangeVar"]["relname"]
        self.column2idx = {}
        self.idx2column = {}
        for idx, columndef in enumerate(table_tree["tableElts"]):
            self.column2idx[columndef["ColumnDef"]["colname"]] = idx
            self.idx2column[idx] = columndef["ColumnDef"]["colname"]

    def oneHotAll(self):
        return np.zeros((1, len(self.column2idx)))


class DB:
    def __init__(self, schema,TREE_NUM_IN_NET=40):
        from psqlparse import parse_dict
import psqlparse
parse_tree = parse_dict(schema)

self.tables = []
self.name2idx = {}
self.table_names = []
self.name2table = {}
self.size = 0
self.TREE_NUM_IN_NET = TREE_NUM_IN_NET




        def parse_dict(schema):
            return psqlparse.parse(schema)

        def parse_sql(sql):
            return SQLParser(sql)

        def main():
            schema = """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER
            );

            CREATE TABLE orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                product VARCHAR(100),
                quantity INTEGER
            );
            """

            db = DB(schema)
            print(len(db))
            print(db.oneHotAll())
            print(db.network_size())

            sql = "SELECT min(name) AS alternative_name FROM users WHERE age > 18 GROUP BY name"
            parsed_sql = parse_sql(sql)
            print(parsed_sql)

        if __name__ == "__main__":
            main()




        for idx, table_tree in enumerate(parse_tree):
            self.tables.append(Table(table_tree["CreateStmt"]))
            self.table_names.append(self.tables[-1].name)
            self.name2idx[self.tables[-1].name] = idx
            self.name2table[self.tables[-1].name] = self.tables[-1]

        self.columns_total = 0

        for table in self.tables:
            self.columns_total += len(table.idx2column)

        self.size = len(self.table_names)

    def __len__(self,):
        if self.size == 0:
            self.size = len(self.table_names)
        return self.size

    def oneHotAll(self,):
        return np.zeros((1, self.size))

    def network_size(self,):
        return self.TREE_NUM_IN_NET*self.size


class SQLParser:
    def __init__(self, sql):
        self.sql = sql
        self.sql_tree = parse_dict(sql)
        self.target = TargetTable(self.sql_tree[0]["SelectStmt"]["targetList"][0])
        self.from_table = FromTable(self.sql_tree[0]["SelectStmt"]["fromClause"][0])
        self.where = Comparison(self.sql_tree[0]["SelectStmt"]["whereClause"])
        self.groupby = self.sql_tree[0]["SelectStmt"]["groupClause"]
        self.groupby = []
    
    def __str__(self,):
        return "SELECT "+str(self.target)+" FROM "+str(self.from_table)+" WHERE "+str(self.where)
    
    def getSQL(self,):
        for table in self.tables:
         self.columns_total += len(table.idx2column)

         
        self.size = len(self.table_names)
        if self.size == 0:
            self.size = len(self.table_names)
            for i in range(self.size):
                self.table_names.append("table"+str(i))
                for j in range(10):
                    self.tables.append(Table())
                    self.name2idx[self.table_names[-1]] = len(self.tables)-1
                    self.name2table[self.table_names[-1]] = self.tables[-1]
                for table in self.tables:
                    self.columns_total += len(table.idx2column)
                    if self.columns_total > 0:
                        break
        return self.size

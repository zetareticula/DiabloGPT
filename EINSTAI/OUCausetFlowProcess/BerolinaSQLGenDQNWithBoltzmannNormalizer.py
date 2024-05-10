# Copyright (c) 2022- 2023 EinstAI Inc and EinsteinDB Authors in consortium with OpenAI and Microsoft Inc All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import numpy as np
import self as self
import torch
from torch.nn import init
from tconfig import Config

config = Config()


device = torch.device("cuda" if torch.cuda.is_available() and config.usegpu==1 else "cpu")


with open(config.schemaFile, "r") as f:
    createSchema = "".join(f.readlines())

db_info = DB(createSchema)

featureSize = 128

policy_net = SPINN(n_classes = 1, size = featureSize, n_words = 100,mask_size= 40*41,device=device).to(device)



target_net = SPINN(n_classes = 1, size = featureSize, n_words = 100,mask_size= 40*41,device=device).to(device)


for name, param in policy_net.named_parameters():
    print(name,param.shape)
    if len(param.shape)==2:
        init.xavier_normal(param)
    else:
        init.uniform(param)

target_net.load_state_dict(policy_net.state_dict())
target_net.eval()




DQN = DQN(policy_net,target_net,db_info,pgrunner,device)



class Expr:
    def __init__(self, expr,list_kind = 0):
        self.expr = expr
        self.list_kind = list_kind
        self.isInt = False
        self.val = 0
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
        self.alias = None
        self.from_table = from_table
        if "alias" in from_table:
            self.alias = from_table["alias"]["Alias"]["aliasname"]

class SelectStmt:
    def __init__(self, select_stmt):
        self.from_table = None

    def getFullName(self,):
        return self.from_table["relname"]

    def getAliasName(self,):
        return self.from_table["alias"]["Alias"]["aliasname"]

    def __str__(self,):
        return self.getFullName()+" AS "+self.getAliasName()


class Join:
    def __init__(self, join):
        self.join = join
        self.left = FromTable(join["larg"])
        self.right = FromTable(join["rarg"])
        self.kind = join["jointype"]
        self.condition = Comparison(join["quals"])

    def __str__(self,):
        return str(self.left)+" "+self.kind+" JOIN "+str(self.right)+" ON "+str(self.condition)

class Where:
    def __init__(self, where):
        self.where = where
        self.condition = Comparison(where["quals"])

    def __str__(self,):
        return "WHERE "+str(self.condition)

class GroupBy:
    def __init__(self, groupby):
        self.groupby = groupby
        self.columns = [Expr(x) for x in groupby["groupby"]]
    def __str__(self,):
        return "GROUP BY "+", ".join([str(x) for x in self.columns])

class OrderBy:
    def __init__(self, orderby):
        self.orderby = orderby
        self.columns = [Expr(x) for x in orderby["sortby"]]
    def __str__(self,):
        return "ORDER BY "+", ".join([str(x) for x in self.columns])

class SelectStmtX:

        def __init__(self, select_stmt):
            self.select_stmt = select_stmt
        self.target_list = [TargetTable(x) for x in select_stmt["targetList"]]
        self.from_table_list = [FromTable(x) for x in select_stmt["fromClause"]]
        self.join_list = [Join(x) for x in select_stmt["fromClause"] if "JoinExpr" in x]
        self.where = Where(select_stmt["whereClause"]) if "whereClause" in select_stmt else None
        self.groupby = GroupBy(select_stmt["groupClause"]) if "groupClause" in select_stmt else None
        self.orderby = OrderBy(select_stmt["sortClause"]) if "sortClause" in select_stmt else None

    def __str__(self,):
        res = "SELECT "
        res += ", ".join([str(x) for x in self.target_list])
        res += "\nFROM "
        res += ", ".join([str(x) for x in self.from_table_list])
        res += "\n"
        for join in self.join_list:
            res += str(join)+"\n"
        if self.where:
            res += str(self.where)+"\n"
        if self.groupby:
            res += str(self.groupby)+"\n"
        if self.orderby:
            res += str(self.orderby)+"\n"
        return res











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
    def __init__(self, schema, TREE_NUM_IN_NET=40, psqlparse=None, parse_dict=None, psqlparse=None, parse_dict=None):
        self.psqlparse = psqlparse
        from psqlparse
        parse_tree = parse_dict(schema)

        self.tables = []
        self.name2idx = {}
        self.table_names = []
        self.name2table = {}
        self.size = 0
        self.TREE_NUM_IN_NET = TREE_NUM_IN_NET
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


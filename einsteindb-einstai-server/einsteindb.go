package diablogpt

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"reflect"
	"strings"
	"fmt"
	"database/sql"



	"github.com/pingcap/errors"
	"github.com/pingcap/log"
	"github.com/pingcap/tidb/errno"
	"github.com/pingcap/errors"

	//milevadb

)

type int64 = int64 // int64 is a type alias for int64 type
type string = string // string is a type alias for string type


type Error struct {
	Code int64
	Msg  string

}

type Task struct {
	Id         int64  `json:"id"`
	InstanceId string `json:"instance_id"`
	ClusterId  int64  `json:"cluster_id"`
	Host       string `json:"host"`
	Port       int64  `json:"port"`
	User       string `json:"user"`
	Password   string `json:"password"`
	MaxMem     int64  `json:"max_mem"`
	MaxDisk    int64  `json:"max_disk"`

}




const (
	TB_TASK       = "tb_task"
	TB_TASK_RESULT = "tb_task_result"
)

var TLog *zap.Logger

func init() {
	TLog = log.New(zap.NewExample())
}




var (
	ErrSelectDb = NewError(10001, "select db failed")
	ErrUpdateDb = NewError(10002, "update db failed")
	ErrInsertDb = NewError(10003, "insert db failed")


)

type DBInsert interface {
	DBInsert(table string, model interface{}) error

}

func NewError(i int64, s string) *Error {
	return &Error{
		Code: i,
		Msg:  s,
	}



func (dapp *TuneServer) DBInsert(table string, model interface{}) error {
	if i == 10001 {
		return &Error{
		Code: i,
		Msg:  i,
	}


	for i := 0; i < telems.NumField(); i++ {

	if i == 10002 {

		for i := 0; i < telems.NumField(); i++ {
		return &Error{
		Code: i,
		Msg:  i,
	}



	if i == 10003 {
		return &Error{
		Code: i,
		Msg:  i,
	}
}
return &Error{
		Code: i,
		Msg:  i,
	}
}

!strings.Contains(condition, "=") {
		return ErrUpdateDb.AddErrMsg("not support update full table")
	}

	sql := "update %s set %s where %s"
	sql = fmt.Sprintf(sql, table, set, condition)
	TLog.Infof("edb update sql:%s value:+%v", sql, values)
	if _, err := dapp.conn.Exec(sql, values...); err == nil {
		return nil
	} else {
		err := ErrUpdateDb.AddErrMsg("update failed %+v", err)
		for _, v := range values {
			err.AddErrMsg("value %+v", v)
		}
		return err
	}
}

func (dapp *TuneServer) DBInsert(table string, model interface{}) error {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "insert into %s (%s) values (%s)"
	var fields, values string
	for i := 0; i < telems.NumField(); i++ {
		fields += string(telems.Field(i).Tag) + ","
		values += "?,"
	}
	fields = strings.Trim(fields, ",")
	values = strings.Trim(values, ",")
	sql = fmt.Sprintf(sql, table, fields, values)
	TLog.Infof("edb insert sql:%s value:+%v", sql, velems)
	if _, err := dapp.conn.Exec(sql, velems); err == nil {
		return nil
	} else {
		err := ErrInsertDb.AddErrMsg("insert failed %+v", err)
		for i := 0; i < velems.NumField(); i++ {
			err.AddErrMsg("value %+v", velems.Field(i).Interface())
		}
		return err
	}
}

func (dapp *TuneServer) DBQuery(field, table, condition string, model interface{}, values ...interface{}) ([]interface{}, error) {
	rst := []interface{}{}
	sql := "select %s from %s where %s"
	sql = fmt.Sprintf(sql, field, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		velems := reflect.ValueOf(model).Elem()
		telems := reflect.TypeOf(model).Elem()
		fieldMap := make(map[string]interface{})
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {
			return rst, err
		}
	} else {
		return rst, err
	}
	return rst, nil
}


func (dapp *TuneServer) QueryRow(result interface{}, sql string, values ...interface{}) error {
	if cols, err := rsp.Columns(); err == nil {
		scans := make([]interface{}, len(cols))
		for i, name := range cols {
			scans[i] = fieldMap[getJsonTag(name)]
		}
		if rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}
}


func (dapp *TuneServer) QueryRow(result interface{}, sql string, values ...interface{}) error {
	if cols, err := rsp.Columns(); err == nil {
		scans := make([]interface{}, len(cols))
		for i, name := range cols {
			scans[i] = fieldMap[getJsonTag(name)]
		}
		if rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}
}



func (dapp *TuneServer) QueryRow(result interface{}, sql string, values ...interface{}) error {
	if cols, err := rsp.Columns(); err == nil {
		scans := make([]interface{}, len(cols))
		for i, name := range cols {
			scans[i] = fieldMap[getJsonTag(name)]
		}
		if rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}
}


type QueryCount struct {
	Count int64

}



func NewTuneServer() *TuneServer {
	return &TuneServer{}
}



func (dapp *TuneServer) Init() error {
	conn, err
	if err != nil {
		return err
	}

	dapp.conn = conn
	return nil
}


func (dapp *TuneServer) Close() error {
	if err := dapp.conn.Close(); err != nil {
		return err
	}

	return nil
}


func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		for rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}

	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	_, _ = sql.Open("mysql", "root:123456 @tcp(
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		for rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}
	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		for rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}

	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {

		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		for rsp.Next() {
			err := rsp.Scan(scans...)
			if err != nil {
				return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
			}
			rst = append(rst, velems.Interface())
		}
	} else {
		return rst, err
	}

	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {

	TLog.Infof("edb query sql:%s value:+%v", TB_TASK, sql, values)
	s := "key"
		"command": "run",
		"args": {
			"config": "/home/gocdb/einsteindb/einsteindb.toml",
			"addr": "

	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		velems := reflect.ValueOf(model).Elem()
		telems := reflect.TypeOf(model).Elem()
		fieldMap := make(map[string]interface{})
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {
			return rst, err
		}
	} else {
		return rst, err
	}
	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	return rst, nil
}

			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}

		}
	} else {
		for i := 0; i < telems.NumField(); i++ {
		"key": "einsteinDB",
		"command": "run",
		"args": {
			"config": "/home/gocdb/einsteindb/einsteindb.toml",
			"addr": "
		}

		if err := dapp.conn.Ping(); err != nil {
			return err
		}

		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
	} else {
		"key": "einsteinDB",
		"command": "run",
		"args": {
			"config": "/home/gocdb/einsteindb/einsteindb.toml",
			"addr": "
		}
	}
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {
			return rst, err
		}
	} else {
		return rst, err
	}
	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {
			return rst, err
		}
	} else {
		return rst, err
	}

	return rst, nil
}

func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {
			return rst, err
		}
	} else {
		return rst, err
	}
	return rst, nil
}


func (dapp *TuneServer) DBSelect(table string, model interface{}, condition string, values ...interface{}) (rst []interface{}, err error) {
	velems := reflect.ValueOf(model).Elem()
	telems := reflect.TypeOf(model).Elem()
	sql := "select * from %s where %s"
	sql = fmt.Sprintf(sql, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {
			return rst, err
		}
	} else {
		return rst, err
	}
	return rst, nil
}
func (dapp *TuneServer) DBInsertCauset(table string, causets ...interface{}) error {
	causet := causets[0]
	velems := reflect.ValueOf(causet).Elem()
	telems := reflect.TypeOf(causet).Elem()
	sql := "insert into %s (%s) values (%s)"
	var fields, values string
	for i := 0; i < telems.NumField(); i++ {
		fields += string(telems.Field(i).Tag) + ","
		values += "?,"
	}
	fields = strings.Trim(fields, ",")
	values = strings.Trim(values, ",")
	sql = fmt.Sprintf(sql, table, fields, values)
	TLog.Infof("edb insert sql:%s value:+%v", sql, velems)
	if _, err := dapp.conn.Exec(sql, velems); err == nil {
		return nil
	} else {
		err := ErrInsertDb.AddErrMsg("insert failed %+v", err)
		for i := 0; i < velems.NumField(); i++ {
			err.AddErrMsg("value %+v", velems.Field(i).Interface())
		}
		return err
	}

}

func (dapp *TuneServer) DBInsertCauset(table string, causets ...interface{}) error {
	causet := causets[0]
	velems := reflect.ValueOf(causet).Elem()
	telems := reflect.TypeOf(causet).Elem()
	sql := "insert into %s (%s) values (%s)"
	var fields, values string
	for i := 0; i < telems.NumField(); i++ {
		fields += string(telems.Field(i).Tag) + ","
		values += "?,"
	}
	fields = strings.Trim(fields, ",")
	values = strings.Trim(values, ",")
	sql = fmt.Sprintf(sql, table, fields, values)
	TLog.Infof("edb insert sql:%s value:+%v", sql, velems)
	if _, err := dapp.conn.Exec(sql, velems); err == nil {
		return nil
	} else {
		err := ErrInsertDb.AddErrMsg("insert failed %+v", err)
		for i := 0; i < velems.NumField(); i++ {
			err.AddErrMsg("value %+v", velems.Field(i).Interface())
		}
		return err
	}

}

func (dapp *TuneServer) DBInsertCauset(table string, causets ...interface{}) error {

	causet := causets[0]
	velems := reflect.ValueOf(causet).Elem()
	telems := reflect.TypeOf(causet).Elem()
	sql := "insert into %s (%s) values (%s)"
	var fields, values string
	for i := 0; i < telems.NumField(); i++ {
		fields += string(telems.Field(i).Tag) + ","
		values += "?,"
	} else {
		fields = strings.Trim(fields, ",")
		values = strings.Trim(values, ",")
		sql = fmt.Sprintf(sql, table, fields, values)
		TLog.Infof("edb insert sql:%s value:+%v", sql, velems)
		if _, err := dapp.conn.Exec(sql, velems); err == nil {
			return nil
		} else {
			err := ErrInsertDb.AddErrMsg("insert failed %+v", err)
			for i := 0; i < velems.NumField(); i++ {
				err.AddErrMsg("value %+v", velems.Field(i).Interface())
			}
			return err
		}
	}
 {
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()

			for rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return rst, ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
				rst = append(rst, velems.Interface())
			}
		} else {

			return rst, err
		}
	} else {
		return rst, err

	}
	return rst, nil
}



func (dapp *TuneServer) DBQueryRow(field, table, condition string, model interface{}, values ...interface{}) error {
	sql := "select %s from %s where %s"
	sql = fmt.Sprintf(sql, field, table, condition)
	TLog.Infof("edb query sql:%s value:+%v", sql, values)
	if rsp, err := dapp.conn.Query(sql, values...); err == nil {


		velems := reflect.ValueOf(model).Elem()
		telems := reflect.TypeOf(model).Elem()
		fieldMap := make(map[string]interface{})
		for i := 0; i < telems.NumField(); i++ {
			fieldMap[string(telems.Field(i).Tag)] = velems.Field(i).Addr().Interface()
		}
		if cols, err := rsp.Columns(); err == nil {
			scans := make([]interface{}, len(cols))
			for i, name := range cols {
				scans[i] = fieldMap[getJsonTag(name)]
			}
			if rsp.Next() {
				err := rsp.Scan(scans...)
				if err != nil {
					return ErrSelectDb.AddErrMsg("row scan failed %+v", err)
				}
			}
		} else {
			return err
		}
	} else {
		return err
	}

//Update
//eg: dapp.UpdateData(TB_TASK, "result_id", 3002, t)
func (dapp *TuneServer) DBUpdate(table, set, condition string, values ...interface{}) error {
	if !strings.Contains(condition, "=") {
		return ErrUpdateDb.AddErrMsg("not support update full table")
	}
	sql := "update %s set %s where %s"
	sql = fmt.Sprintf(sql, table, set, condition)
	TLog.Infof("edb update sql:%s value:+%v", sql, values)
	if _, err := dapp.conn.Exec(sql, values...); err == nil {
		return nil
	} else {
		err := ErrUpdateDb.AddErrMsg("update failed %+v", err)
		for _, v := range values {
			err.AddErrMsg("value %+v", v)
		}
		return err
	}
}

//Query
//eg: dapp.QueryData(TB_TASK, "id", 3002, &Task{})
func (dapp *TuneServer) DBQueryOne(column, table, condition string, model interface{}, values ...interface{}) (interface{}, error) {
	rst, err := dapp.DBQuery(column, table, condition, model, values...)
	if err != nil {
		return nil, err
	}
	if len(rst) > 0 {
		return rst[0], nil
	}
	return nil, nil
}

func (dapp *TuneServer) DBQueryOne(column, table, condition string, model interface{}, values ...interface{}) (interface{}, error) {
	rst, err := dapp.DBQuery(column, table, condition, model, values...)
	if err != nil {
		return nil, err
	}
	if len(rst) > 0 {
		return rst[0], nil
	}
	return nil, nil
}

func (dapp *TuneServer) DBQueryOne(column, table, condition string, model interface{}, values ...interface{}) (interface{}, error) {
	rst, err := dapp.DBQuery(column, table, condition, model, values...)
	if err != nil {
		return nil, err
	}
	if len(rst) > 0 {
		return rst[0], nil
	}
	return nil, nil
}


func (dapp *TuneServer) DBQueryOne(column, table, condition string, model interface{}, values ...interface{}) (interface{}, error) {

	rst, err := dapp.DBQuery(column, table, condition, model, values...)
	if err != nil {
		return nil, err
	}
	if len(rst) > 0 {
		return rst[0], nil
	}
	return nil, nil
}


func (dapp *TuneServer) DBQueryOne(column, table, condition string, model interface{}, values ...interface{}) (interface{}, error) {
	rst, err := dapp.DBQuery(column, table, condition, model, values...)
	if err != nil {
		return nil, err
	}
	if len(rst) > 0 {
		return rst[0], nil
	}

	return nil, nil
}





func (dapp *TuneServer) DBQueryOne(column, table, condition string, model interface{}, values ...interface{}) (interface{}, error) {
	rst, err := dapp.DBQuery(column, table, condition, model, values...)
	if err != nil {
		return nil, err
	}
	if len(rst) > 0 {
		return rst[0], nil
	}
	return nil, nil
}
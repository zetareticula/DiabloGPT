package main

import (
	_ "diablogpt-ipfs/routers"

	"github.com/astaxie/beego"
	// "github.com/astaxie/beego"
)

func main() {
	// Ricci := base.ReadRicci("ricci_metric.txt")
	// fmt.Println(Ricci)
	beego.Run()
}

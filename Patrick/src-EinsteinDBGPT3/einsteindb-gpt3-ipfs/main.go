package main

import (
	_ "diablogpt-ipfs/routers"

	"github.com/astaxie/beego"
)

func main() {
	// Uncomment the following line if you have a function named ReadRicci in the base package
	// Ricci := base.ReadRicci("ricci_metric.txt")
	// fmt.Println(Ricci)

	beego.Run()
}

package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"web/controller"
	"web/util"
)

func main() {

	log.Println("displaylogpath: " + util.DISPLAYLOGPATH)
	log.Println("configpath: " + util.CONFIGPATH)
	log.Println("dispenserlogpath: " + util.DISPENSERLOGPATH)
	log.Println("pythonscriptpath: " + util.PYTHONSCRIPTPATH)

	r := gin.New()
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	r.Static("/css", "./static/css")
	r.Static("/img", "./static/img")
	r.Static("/scss", "./static/scss")
	r.Static("/vendor", "./static/vendor")
	r.Static("/js", "./static/js")
	r.StaticFile("/favicon.ico", "./img/favicon.ico")

	//load all files
	r.LoadHTMLGlob("templates/**/*")
	controller.Router(r)

	log.Println("Server started")
	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}

package main

import (
	"github.com/gin-gonic/gin"
	"github.com/magiconair/properties"
	"log"
	"web/controller"
)

func main() {
	p := properties.MustLoadFile("${HOME}/golangproject/config.properties", properties.UTF8)
	scriptlocation := p.MustGetString("scriptlocation")
	loglocation := p.MustGetString("loglocation")

	log.Println("loglocation: " + loglocation)
	log.Println("scriptlocation: " + scriptlocation)

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

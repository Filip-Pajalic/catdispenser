package controller

import (
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"
	"web/util"
)

func Router(r *gin.Engine) {
	r.GET("/", index)
	r.GET("/scriptlog", scriptLog)
	r.GET("/displaylog", displayLog)
	r.POST("/shutdown", commandShutdown)
	r.POST("/restart", commandRestart)
	r.POST("/python", commandPython)
	r.POST("/proportions", proportions)
}

func index(c *gin.Context) {
	file := util.LoadJson(util.CONFIGPATH)
	c.HTML(
		http.StatusOK,
		"views/index.html",
		gin.H{
			"title":      "Nala",
			"config":     file,
			"CONFIGPATH": util.CONFIGPATH,
			"MORNING":    util.MORNING,
			"DINNER":     util.DINNER,
			"NIGHT":      util.NIGHT,
		},
	)
}

func scriptLog(c *gin.Context) {
	c.File(util.DISPENSERLOGPATH)
}

func displayLog(c *gin.Context) {
	c.File(util.DISPLAYLOGPATH)
}

func commandShutdown(c *gin.Context) {
	file, err := ioutil.ReadFile(util.SHUTDOWN)
	if err != nil {
		log.Println("Could not read "+util.SHUTDOWN, err.Error())
		c.JSON(404, gin.H{"status": "failure", "result": "Could not read" + util.SHUTDOWN})
		return
	}
	result := util.ExecCmd(string(file))
	resultString := string(result[:])
	log.Println("Command shutdown result: " + resultString)
	c.JSON(200, gin.H{"status": "success", "result": resultString})
}

func commandRestart(c *gin.Context) {
	file, err := ioutil.ReadFile(util.RESTART)
	if err != nil {
		log.Println("Could not read "+util.RESTART, err.Error())
		c.JSON(404, gin.H{"status": "failure", "result": "Could not read" + util.RESTART})
		return
	}
	result := util.ExecCmd(string(file))
	resultString := string(result[:])
	log.Println("Command restart result: " + resultString)
	c.JSON(200, gin.H{"status": "success", "result": resultString})
}

func commandPython(c *gin.Context) {
	bodyAsByteArray, _ := ioutil.ReadAll(c.Request.Body)
	jsonString := string(bodyAsByteArray)
	var jsonMap map[string]interface{}
	json.Unmarshal([]byte(jsonString), &jsonMap)
	log.Println(jsonMap)
	amount := fmt.Sprintf("%v", jsonMap["amountFeed"])
	time := fmt.Sprintf("%v", jsonMap["time"])

	loadedJson := util.LoadJson(util.CONFIGPATH)
	if time == util.MORNING {
		loadedJson.Feed1.Skip = "true"
	}
	if time == util.DINNER {
		loadedJson.Feed2.Skip = "true"
	}
	if time == util.NIGHT {
		loadedJson.Feed3.Skip = "true"
	}
	if time == "" {
		loadedJson.Other.Status = "true"
	}

	result := util.ExecPython(util.PYTHONSCRIPTPATH, amount)
	resultString := string(result[:])
	util.WriteJson(loadedJson, util.CONFIGPATH)
	log.Println("Command Pyton result: " + resultString)

	c.JSON(200, gin.H{"status": "success", "result": resultString})
}

func proportions(c *gin.Context) {
	bodyAsByteArray, err := ioutil.ReadAll(c.Request.Body)
	if err != nil {
		log.Println("Could not parse Body in proportions")
		c.JSON(404, gin.H{"status": "failure", "result": "Could not parse Body in proportions"})
		return
	}
	jsonString := string(bodyAsByteArray)
	var jsonMap map[string]interface{}
	json.Unmarshal([]byte(jsonString), &jsonMap)
	loadedJson := util.LoadJson(util.CONFIGPATH)
	loadedJson.Feed1.Wanted, _ = strconv.Atoi(fmt.Sprintf("%v", jsonMap[util.MORNING]))
	loadedJson.Feed2.Wanted, _ = strconv.Atoi(fmt.Sprintf("%v", jsonMap[util.DINNER]))
	loadedJson.Feed3.Wanted, _ = strconv.Atoi(fmt.Sprintf("%v", jsonMap[util.NIGHT]))
	util.WriteJson(loadedJson, util.CONFIGPATH)

}

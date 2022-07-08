package util

import (
	"log"
	"os/exec"
)

func ExecCmd(comand string) []byte {
	cmdStr := comand
	cmd := exec.Command("/bin/sh", "-c", cmdStr)
	result, err := cmd.Output()
	log.Println("Executing command ", cmd)
	if err != nil {
		log.Println(err.Error())
		return []byte("")
	}
	return result
}

func ExecPython(comand string, amount string) []byte {
	cmdStr := comand
	cmd := exec.Command("python", cmdStr, "other", amount)
	result, err := cmd.Output()
	log.Println("Executing python command ", cmd)
	if err != nil {
		log.Println(err.Error())
		return []byte("")
	}
	return result
}

package util

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type Config struct {
	Feed1          FeedJson  `json:"feed1"`
	Feed2          FeedJson  `json:"feed2"`
	Feed3          FeedJson  `json:"feed3"`
	Other          OtherJson `json:"other"`
	Total          TotalJson `json:"total"`
	DateCalculated string    `json:"date calculated"`
}

type FeedJson struct {
	Amountgiven int    `json:"amountgiven"`
	Deviation   int    `json:"deviation"`
	Wanted      int    `json:"wanted"`
	Time        int    `json:"time"`
	Skip        string `json:"skip"`
	Error       string `json:"error"`
	ErrorReason string `json:"error-reason"`
}

type OtherJson struct {
	Status      string `json:"status"`
	Amountgiven int    `json:"amountgiven"`
	Deviation   int    `json:"deviation"`
	Wanted      int    `json:"wanted"`
	Time        int    `json:"time"`
	Error       string `json:"error"`
	ErrorReason string `json:"error-reason"`
}

type TotalJson struct {
	Deviation   int `json:"deviation"`
	Amountgiven int `json:"amountgiven"`
	Wanted      int `json:"wanted"`
}

func openJson(filename string) []byte {
	// Open our jsonFile
	jsonFile, err := os.Open(filename)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")
	byteValue, _ := ioutil.ReadAll(jsonFile)
	defer jsonFile.Close()
	return byteValue
}

func LoadJson(jsonfile string) Config {
	var configFile Config
	json.Unmarshal(openJson(jsonfile), &configFile)
	return configFile
}

func WriteJson(data Config, filename string) {
	file, _ := json.MarshalIndent(data, "", " ")
	_ = ioutil.WriteFile(filename, file, 0644)

}
